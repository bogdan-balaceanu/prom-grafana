#!/bin/bash

# The function that prints the help
Help()
{
        echo "The script is used to remove a dashboard for Grafana"
        echo
        echo "SYNTAX: gdc [-n|j|h]"
        echo
        echo "OPTIONS:"
        echo "n         The dashboard name"
        echo "j         The job name"
        echo "h         Prints this menu"
}

Linux()
{

dashBoardName=$name

output=$(ssh root@10.10.0.62 'cd /root/gdc/grafana-import && grafana-import -d "'$dashBoardName'" export && SEARCH_STRING="'$dashBoardName'"; find . -type f -name "*$SEARCH_STRING*" -exec cat {} \; -quit | grep -oP "job=([^,]+)" | grep -oP "(?<=\")[^\"\\\\]+(?=\\\\)" -m 1 | grep -oE "[^[:space:]]+$"')

#ssh root@10.10.0.62 'cd /root/gdc/grafana-import && SEARCH_STRING="'$dashBoardName'"; find . -type f -name "*$SEARCH_STRING*" -print -quit'

ssh root@10.10.0.62 'cd /root/gdc/grafana-import && grep -rl "'$dashBoardName'" . | xargs rm -f'

ssh root@10.10.0.62 'cd /root/gdc/grafana-import && grafana-import -f ATM_VMS -d "'$dashBoardName'" remove'
echo "$dashBoardName deleted from grafana"

jobname=$(echo $output | awk '{print $NF}')

#CLEAR ENTRY IN /etc/prometheus/prometheus.yml
file_path="/etc/prometheus/prometheus.yml"  # Replace with the path to your file
search_string=$jobname       # Replace with your desired search string

# Check if the file exists
if [ ! -f "$file_path" ]; then
    echo "File not found: $file_path"
    exit 1
fi

# Find the line number containing the search string
line_number=$(grep -n "$search_string" "$file_path" | head -n 1 | cut -d ":" -f 1)

# Check if the search string is found in the file
if [ -z "$line_number" ]; then
    echo "String '$search_string' not found in /etc/prometheus/prometheus.yml"
    exit 1
fi

# Delete the lines containing the search string and the next four lines
start_line=$((line_number))
end_line=$((start_line + 4))

sed -i "${start_line},${end_line}d" "$file_path"
echo "Job deleted from /etc/prometheus/prometheus.yml"
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
    echo "Prometheus was not reloaded"
fi

#CLEAR /etc/hosts
#!/bin/bash

file_path="/etc/hosts"  # Replace with the path to your file
search_string=$jobname  # Replace with the string to be deleted

line_number=$(grep -n "$search_string" "$file_path" | head -n 1 | cut -d ":" -f 1)

# Check if the search string is found in the file
if [ -z "$line_number" ]; then
    echo "String '$search_string' not found in /etc/hosts"
    exit 1
fi


# Use sed to delete the line containing the search string
#sed -i '/$search_string/d' $file_path
sed -i "/$jobname/d" "$file_path"

echo "Line containing $jobname deleted from /etc/hosts."

}

while getopts "h:n:j:" option; do
        case $option in
                h) # Displays Help
                        Help
                        exit;;
                n) # Dashboard name
                        name=$OPTARG;;
                j) # Job name
                        jobname=$OPTARG;;
               \?) # Invalid Option
                        echo "Invalid Option"
                        Help
                        exit;;
        esac
done
Linux
