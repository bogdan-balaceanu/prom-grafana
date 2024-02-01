import argparse
import subprocess
import re
import ipaddress
import time
import random
import nmap
import sys
import argparse


parser = argparse.ArgumentParser(description = 'This module is for automatically generate malitious traffic for a range of IP\'s')
parser.add_argument('-ips','--ips', type=str, help='Range-ul de IP-uri catre care se va trimite trafic, ex: 10.10.0.60-65')
parser.add_argument('-iface','--iface', type=str, help='Interfata de spoof, ex: eth0 / ens160')
args = parser.parse_args()

if not args.ips or not args.iface:
    print("Scriptul nu a fost rulat cu argumentul -ips or -iface")
    parser.print_help()
    sys.exit(1)


range_of_ips = args.ips
interface_of_spoof = args.iface


input_string = args.ips

# Regular expression pattern to match the format
pattern = r'^(\d+\.\d+\.\d+\.\d+)-(\d+)$'

# Use regular expression to check the format
match = re.match(pattern, input_string)

if match:
    start_ip = match.group(1)
    end_octet = int(match.group(2))

    # Validate if the end octet is greater than the last octet of the start IP
    last_octet_start_ip = int(start_ip.split(".")[-1])
    if end_octet >= last_octet_start_ip:
        print("Valid format.")
    else:
        print("Invalid format: End octet should be greater than the last octet of the start IP.")
        exit()
else:
    print("Invalid format.")
    exit()

# Use regular expression to separate IP address and number after hyphen
match = re.match(r'(\d+\.\d+\.\d+\.\d+)-(\d+)', str(input_string))
if match:
    start_ip = match.group(1)
    
    #print(start_ip)
else:
    print("Invalid input format")

# Use regular expression to separate IP address and number after hyphen
match = re.match(r'(\d+\.\d+\.\d+\.)\d+-(\d+)', str(input_string))

if match:
    ip_prefix = match.group(1)
    number_after_hyphen = match.group(2)
    
    # Concatenate the IP prefix and the number after hyphen
    end_ip = f"{ip_prefix}{number_after_hyphen}"

    #print(end_ip)
else:
    print("Invalid input format")



# Iterate over the range of IP addresses
list_of_ips = []
current_ip = ipaddress.IPv4Address(start_ip)
while current_ip <= ipaddress.IPv4Address(end_ip):
    #print(str(current_ip))
    list_of_ips.append(str(current_ip))
    current_ip += 1

#print(list_of_ips)

list_of_options = [
        "-sn -n -PE", #ping scan, disable port scan, never do dns resolution, icmp echo
        "-p 80 --traceroute", # scan port 80 and trace hop path to each host
        "-p 22,80,443,3389,8080 -sV -O", #scan each port, probeaza porturile deschise pt a det service/version info (-sV), enable OS detection (-O)
        "-p 80 --script http-headers", # info despre http-headers
        "-p 80 --script http-enum",#info despre foldere interesante
        "-p 80 --script http-title", #more info
        "-p 8080 --script http-headers",# aceleasi lucruri dar pe 8080
        "-p 8080 --script http-enum",
        "-p 8080 --script http-title",
        "-sV -O -sC",# merge cu -S; script scan: --script=default (-sC)  probe open ports to deterine service/version info(-sV); enable OS detection (-O)
        "-sC -sV", # mergecu -S; alea fara os detection
        "-sV -p-", #merge -S; scan all ports
        "-T4 -v", # verbosity level increased (-v); 
        "-v", #syn stealth scan + verbose level
        "--top-ports 110" #scan first 110 most common ports
      ]

#lista cu spoof mac
spoof_tehnique_list = ["-Pn --spoof-mac 0","-Pn --spoof-mac Cisco", "-Pn --spoof-mac Vmware"]
spoof_decoy_fake_list = []
x = random.randint(0, 100)
while 1:
    random_target_ip = random.choice(list_of_ips)
    list_of_ips.remove(random_target_ip)
    random_fake_source_ip = random.choice(list_of_ips)
    decoys_string = "-D "
    for decoy in list_of_ips:
        decoys_string = decoys_string + decoy + ","
    decoys_string = decoys_string[:-1]
    list_of_ips.append(random_target_ip)
    random_option = random.choice(list_of_options)

    spoof_ip_string = "-Pn -e " + interface_of_spoof + " -S " + random_fake_source_ip #Treat all hosts as onliné,skip hosts discovery (-Pn)
    spoof_tehnique = random.choice(spoof_tehnique_list)
    #print(spoof_tehnique)
    spoof_decoys_fake_list = []
    if x % 2  == 0:
        spoof_decoy_fake_list.append(spoof_ip_string)
        spoof_decoy_fake_list.append(decoys_string)
        #print(spoof_decoy_fake_list)
        spoof_tehnique = random.choice(spoof_decoy_fake_list)
        
        #spoof_decoys_fake_list.remove(spoof_ip_string)
        #spoof_decoys_fake_list.remove(decoys_string)
    else:
        spoof_tehnique = random.choice(spoof_tehnique_list)
    
    cmd = "nmap " + random_option + " " + spoof_tehnique + " " + random_target_ip
    print("\n\n\n\nexecuting " + cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for the process to finish and get the output and errors
    output, error = process.communicate()

    # Decode the output and error messages
    output = output.decode("utf-8")
    error = error.decode("utf-8")

    # Print the output and error messages
    print("Output:", output)
    print("Error:", error)
    
    # Get the return code of the process
    return_code = process.returncode
    print("Return Code:", return_code)

    x = x + 1

    time.sleep(5)
 

