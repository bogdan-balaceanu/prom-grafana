#!/bin/bash

# The function that prints the help
Help()
{
	echo "The script is used to create a dashboard for Grafana"
	echo
	echo "SYNTAX: gdc [-a|n|j|d|c|p|h]"
	echo
	echo "OPTIONS:"
        echo "p               Port of node_exporter/windows_exporter 9100/9182"
	echo "a		IP address of the host"
	echo "n		The dashboard name"
	echo "j		The job name"
	echo "d		The datasource"
	echo "c		Number of CPUs"
	echo "h		Prints this menu"
}

Linux()
{

	if [[ -n $jobname && -n $addr && -n $port ]]
then
    duplicates=$(cat /etc/prometheus/prometheus.yml | grep -c $jobname)
    duplicates_hosts=$(cat /etc/hosts | grep -c $jobname)
        if [[ $duplicates > 0 ]]
        then
                echo "The job name is already used in /etc/prometheus/prometheus.yml"
                exit;
        fi
	if [[ $duplicates_hosts > 0 ]]
        then
                echo "The job name is already used in /etc/hosts"
		echo "Do you want to continue and add the entry? [y/n]"
		read choice
		if [[ $choice == 'n' ]]
		then
			echo "Skip adding entry in /etc/hosts. Exiting..."
			exit;
		fi
        fi
    #All parameters were supplied
    #Adding the entry to hosts
    cat << EOF >> /etc/hosts
$addr $jobname
EOF
    echo "Successfully added the IP in hosts"
    #Adding the job to prometheus
    cat << EOF >> /etc/prometheus/prometheus.yml

  - job_name: $jobname
    scrape_interval: 5s
    static_configs:
      - targets: ['$jobname:$port']
EOF
    sleep 1
    echo
    echo "Successfully added the job in prometheus"
    sleep 1
    promtool check config /etc/prometheus/prometheus.yml
    echo -n "Would you like to reload prometheus?[y/n]: "
    read choice
    if [[ $choice = 'y' ]]
    then
        systemctl reload prometheus
        sleep 1
        echo
        echo "Successfully reloaded prometheus"
        echo
        #systemctl status prometheus
    else
        echo "Prometheus was not restarted"
    fi
else
    #Not all parameters were supplied
    echo "You must supply three parameters: jobname ip address and port number"
    exit
fi


	if [[ -n $addr && -n $name && -n $ds && -n $jobname && $cpu && -n $port ]]
	then
		if [[ $port == "9100" ]]
		then
			cp ./DashBoardTemplates/DashboardLinux.json ./DashBoards/$name.json
		fi
		if [[ $port == "9182" ]]
		then
			cp ./DashBoardTemplates/DashboardWindows.json ./DashBoards/$name.json
		fi
		cd ./DashBoards
		sed -i "s/DataSource/$ds/g" $name.json
		sed -i "s/DashboardName/$name/g" $name.json
		sed -i "s/JobName/$jobname/g" $name.json
		sed -i "s/cpuAlert/$cpu/g" $name.json
		sed -i "s/IP_ADDR/$addr/g" $name.json
		echo "Successfuly created dashboard $name"

		scp $name.json root@10.10.0.62:/root/gdc/grafana-import/imports/$name.json

		ssh root@10.10.0.62 'cd /root/gdc/grafana-import && grafana-import -i /root/gdc/grafana-import/imports/'$name.json' -o -f ATM_VMS && rm /root/gdc/grafana-import/imports/'$name.json''

		rm $name.json
		
		
	else
		echo "You must provide all parameters: -a -n -d and -p"
		Help
		exit
	fi
}

while getopts "h:a:n:j:d:c:p:" option; do
	case $option in
		h) # Displays Help
			Help
			exit;;
		a) # IP Address
			addr=$OPTARG;;
		n) # Dashboard name
			name=$OPTARG;;
		j) # Job name
			jobname=$OPTARG;;
		d) # Datasource
			ds=$OPTARG;;
		c) # CPU
			cpu=$OPTARG;;
		p) # port
			port=$OPTARG;;
	       \?) # Invalid Option
			echo "Invalid Option"
			Help
			exit;;
	esac
done
Linux

