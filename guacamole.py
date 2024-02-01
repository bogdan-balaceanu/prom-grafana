from argparse import ArgumentParser
import json
import sys
import requests

admin_user="guacadmin"
admin_pass="guacadmin"

data_source = "mysql"

base_url = "http://10.10.0.67:8080/guacamole/api/"

def getToken(user,password):
    url = base_url + "tokens"
    obj = {'username': user,
    'password': password
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_json = json.loads(requests.post(url, data=obj, headers=headers).text)
    token = token_json['authToken']
    return token

    
def addUser(username,user_pass):
    token = getToken(admin_user, admin_pass)
    url = base_url + "session/data/" + data_source + "/users"
    params = {'token': token }
    users = json.loads(requests.get(url, params=params).text)
    list_of_users = []
    for user in users:
        list_of_users.append(user)
    if username in list_of_users:
        print("User already exists")
    else:
        #create user
        url = base_url + "session/data/" + data_source + "/users"
        obj = {
                "username": username,
                "password": user_pass,
                "attributes": {
                    "disabled": "",
                    "expired": "",
                    "access-window-start": "",
                    "access-window-end": "",
                    "valid-from": "",
                    "valid-until": "",
                    "timezone": "null",
                    "guac-full-name": "",
                    "guac-organization": "",
                    "guac-organizational-role": ""
                }
            }
        print(requests.post(url,json=obj,params=params).text)
        #Add Privilege to user
        url = base_url + "session/data/" + data_source + "/users/" + username + "/permissions"
        print(url)
        obj = [
                    {
                        "op": "add",
                        "path": "/systemPermissions",
                        "value": "CREATE_CONNECTION"
                    },
                    {
                        "op": "add",
                        "path": "/systemPermissions",
                        "value": "CREATE_CONNECTION_GROUP"
                    }
            ]
        requests.patch(url, json=obj, params=params)
        
    
def addSSHConnection(username,user_pass,ip,connectionGroupIdentifier):
    token = getToken(username, user_pass)
    params = {'token': token }
    url = base_url + "session/data/" + data_source + "/connections"
    obj = {
            "parentIdentifier": connectionGroupIdentifier,
            "name": con_name,
            "protocol": "ssh",
            "parameters": {
                "port": "22",
                "read-only": "",
                "swap-red-blue": "",
                "cursor": "",
                "color-depth": "",
                "clipboard-encoding": "",
                "disable-copy": "",
                "disable-paste": "",
                "dest-port": "",
                "recording-exclude-output": "",
                "recording-exclude-mouse": "",
                "recording-include-keys": "",
                "create-recording-path": "",
                "enable-sftp": "",
                "sftp-port": "",
                "sftp-server-alive-interval": "",
                "enable-audio": "",
                "color-scheme": "",
                "font-size": "",
                "scrollback": "",
                "timezone": "null",
                "server-alive-interval": "",
                "backspace": "",
                "terminal-type": "",
                "create-typescript-path": "",
                "hostname": ip,
                "host-key": "",
                "private-key": "",
                "username": "",
                "password": "",
                "passphrase": "",
                "font-name": "",
                "command": "",
                "locale": "",
                "typescript-path": "",
                "typescript-name": "",
                "recording-path": "",
                "recording-name": "",
                "sftp-root-directory": ""
            },
            "attributes": {
                "max-connections": "",
                "max-connections-per-user": "",
                "weight": "",
                "failover-only": "",
                "guacd-port": "",
                "guacd-encryption": "",
                "guacd-hostname": ""
            }
    }
    requests.post(url, json=obj, params=params).text

def addConnectionGroup(username, user_pass):
    token = getToken(username, user_pass)
    url = base_url + "session/data/" + data_source + "/connectionGroups"
    params = {'token': token }
    connectionGroups = json.loads(requests.get(url, params=params).text)
    #con_name = username
    list_of_connectionGroups = []
    for connectionGroup in connectionGroups:
        list_of_connectionGroups.append(connectionGroups[connectionGroup]['name'])
    if username in list_of_connectionGroups:
        print("ConnectionGroup already exists! ")
        return connectionGroups[connectionGroup]['identifier']
    else:
        print("ConnectionGroup does not exist")
        obj = {
                "parentIdentifier": "ROOT",
                "name": username,
                "type": "ORGANIZATIONAL",
                "attributes": {
                    "max-connections": "",
                    "max-connections-per-user": "",
                    "enable-session-affinity": ""
                }
            }
        connectionGroupIdentifier_json = json.loads(requests.post(url, json=obj, params=params).text)
        return connectionGroupIdentifier_json['identifier']

def addRDPConnection(username,user_pass,ip,connectionGroupIdentifier):
    token = getToken(username, user_pass)
    
    params = {'token': token }
    url = base_url + "session/data/" + data_source + "/connections"
    
    obj = {
        "parentIdentifier": connectionGroupIdentifier,
        "name": con_name,
        "protocol": "rdp",
        "parameters": {
            "port": "3389",
            "read-only": "",
            "swap-red-blue": "",
            "cursor": "",
            "color-depth": "",
            "clipboard-encoding": "",
            "disable-copy": "FALSE",
            "disable-paste": "FALSE",
            "dest-port": "",
            "recording-exclude-output": "",
            "recording-exclude-mouse": "",
            "recording-include-keys": "",
            "create-recording-path": "",
            "enable-sftp": "",
            "sftp-port": "",
            "sftp-server-alive-interval": "",
            "enable-audio": "",
            "security": "nla",
            "disable-auth": "",
            "ignore-cert": "true",
            "gateway-port": "",
            "server-layout": "",
            "timezone": "",
            "console": "",
            "width": "",
            "height": "",
            "dpi": "",
            "resize-method": "",
            "console-audio": "",
            "disable-audio": "",
            "enable-audio-input": "",
            "enable-printing": "",
            "enable-drive": "",
            "create-drive-path": "",
            "enable-wallpaper": "",
            "enable-theming": "",
            "enable-font-smoothing": "",
            "enable-full-window-drag": "",
            "enable-desktop-composition": "",
            "enable-menu-animations": "",
            "disable-bitmap-caching": "",
            "disable-offscreen-caching": "",
            "disable-glyph-caching": "",
            "preconnection-id": "",
            "hostname": ip,
            "username": "",
            "password": "",
            "domain": "",
            "gateway-hostname": "",
            "gateway-username": "",
            "gateway-password": "",
            "gateway-domain": "",
            "initial-program": "",
            "client-name": "",
            "printer-name": "",
            "drive-name": "",
            "drive-path": "",
            "static-channels": "",
            "remote-app": "",
            "remote-app-dir": "",
            "remote-app-args": "",
            "preconnection-blob": "",
            "load-balance-info": "",
            "recording-path": "",
            "recording-name": "",
            "sftp-hostname": "",
            "sftp-host-key": "",
            "sftp-username": "",
            "sftp-password": "",
            "sftp-private-key": "",
            "sftp-passphrase": "",
            "sftp-root-directory": "",
            "sftp-directory": ""
        },
        "attributes": {
            "max-connections": "",
            "max-connections-per-user": "",
            "weight": "",
            "failover-only": "",
            "guacd-port": "",
            "guacd-encryption": "",
            "guacd-hostname": ""
        }
}
    requests.post(url, json=obj, params=params)

def addXRDPConnection(username,user_pass,ip,connectionGroupIdentifier):
    token = getToken(username, user_pass)
    
    params = {'token': token }
    url = base_url + "session/data/" + data_source + "/connections"
    
    obj = {
        "parentIdentifier": connectionGroupIdentifier,
        "name": con_name,
        "protocol": "rdp",
        "parameters": {
            "port": "3389",
            "read-only": "",
            "swap-red-blue": "",
            "cursor": "",
            "color-depth": "",
            "clipboard-encoding": "",
            "disable-copy": "FALSE",
            "disable-paste": "FALSE",
            "dest-port": "",
            "recording-exclude-output": "",
            "recording-exclude-mouse": "",
            "recording-include-keys": "",
            "create-recording-path": "",
            "enable-sftp": "",
            "sftp-port": "",
            "sftp-server-alive-interval": "",
            "enable-audio": "",
            "security": "RDP encyption",
            "disable-auth": "",
            "ignore-cert": "true",
            "gateway-port": "",
            "server-layout": "",
            "timezone": "",
            "console": "",
            "width": "",
            "height": "",
            "dpi": "",
            "resize-method": "",
            "console-audio": "",
            "disable-audio": "",
            "enable-audio-input": "",
            "enable-printing": "",
            "enable-drive": "",
            "create-drive-path": "",
            "enable-wallpaper": "",
            "enable-theming": "",
            "enable-font-smoothing": "",
            "enable-full-window-drag": "",
            "enable-desktop-composition": "",
            "enable-menu-animations": "",
            "disable-bitmap-caching": "",
            "disable-offscreen-caching": "",
            "disable-glyph-caching": "",
            "preconnection-id": "",
            "hostname": ip,
            "username": "root",
            "password": "",
            "domain": "",
            "gateway-hostname": "",
            "gateway-username": "",
            "gateway-password": "",
            "gateway-domain": "",
            "initial-program": "",
            "client-name": "",
            "printer-name": "",
            "drive-name": "",
            "drive-path": "",
            "static-channels": "",
            "remote-app": "",
            "remote-app-dir": "",
            "remote-app-args": "",
            "preconnection-blob": "",
            "load-balance-info": "",
            "recording-path": "",
            "recording-name": "",
            "sftp-hostname": "",
            "sftp-host-key": "",
            "sftp-username": "",
            "sftp-password": "",
            "sftp-private-key": "",
            "sftp-passphrase": "",
            "sftp-root-directory": "",
            "sftp-directory": ""
        },
        "attributes": {
            "max-connections": "",
            "max-connections-per-user": "",
            "weight": "",
            "failover-only": "",
            "guacd-port": "",
            "guacd-encryption": "",
            "guacd-hostname": ""
        }
}
    requests.post(url, json=obj, params=params)

def deleteConGroup(conGroupName):
    token = getToken(admin_user, admin_pass)
    url = base_url + "session/data/" + data_source + "/connectionGroups"
    params = {'token': token }
    connectionGroups = json.loads(requests.get(url, params=params).text)
    #con_name = username
    list_of_connectionGroups = []
    for connectionGroup in connectionGroups:
        list_of_connectionGroups.append(connectionGroups[connectionGroup]['name'])
    if conGroupName in list_of_connectionGroups:
        print("ConnectionGroup already exists! ")
        requests.delete(url + "/" + connectionGroups[connectionGroup]['identifier'],params=params)
    else:
        print("Connection group does not exist!")

def deleteUser(username):
    token = getToken(admin_user, admin_pass)
    url = base_url + "session/data/" + data_source + "/users"
    params = {'token': token }
    users = json.loads(requests.get(url, params=params).text)
    list_of_users = []
    for user in users:
        list_of_users.append(user)
    if username in list_of_users:
        requests.delete(url + "/" + username,params=params)
    else:
        print("User does not exist!")

if __name__=='__main__':
    #standardizare connectionGroupName = userName
    parser = ArgumentParser(description = 'This module is used to automatically add users and connections to guacamole server')
    parser.add_argument('-u', '--user', nargs='+', help = 'Add user module/connectionGroupName', required = False)
    parser.add_argument('-p', '--password', nargs='+', help = 'Add passowrd module', required = False)
    parser.add_argument('-ip', '--ip', nargs='+', help = 'IP', required = False)
    parser.add_argument('-prot', '--protocol', nargs='+', help = 'Add protocol module', required = False)
    parser.add_argument('-con', '--conname', nargs='+', help = 'Add con name module', required = False)
    parser.add_argument('-dc', '--deletecon', nargs='+', help = 'Delete connection group', required = False)
    parser.add_argument('-du', '--deleteuser', nargs='+', help = 'Delete user', required = False)
    #parser.add_argument('-i', '--info', nargs='+', help = 'Information about existing virtual machines in vCenter', required = False)
    args = parser.parse_args()

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-dc" or sys.argv[i] == "--deletecon":
            deleteConGroup(sys.argv[i+1])
            exit()
        if sys.argv[i] == "-du" or sys.argv[i] == "--deleteuser":
            deleteUser(sys.argv[i+1])
            exit()

    if not len(sys.argv) > 4:
        print("The script must be called with all arguments")
        print("Use -d <USERNAME> for giving the username")
        print("Use -p <PASSWORD> for giving the password")
        print("Use -ip <IP> for giving IP address")
        print("Use -prot <PROTOCOL> for giving protocol (ssh/rdp/xrdp)")
        print("Use -con <CONNECTION_NAME> for giving connection name unique per connection_group! Also connection group has same name with username")
        exit()

    username = sys.argv[2]
    user_pass = sys.argv[4]
    ip = sys.argv[6]
    prot = sys.argv[8]
    con_name = sys.argv[10]
    addUser(username,user_pass)
    connectionGroupIdentifier = addConnectionGroup(username,user_pass)
    
    if prot.lower() == "ssh":
        addSSHConnection(username,user_pass,ip, connectionGroupIdentifier)
    else:
        if prot.lower() == "rdp":
            addRDPConnection(username,user_pass,ip, connectionGroupIdentifier)

        else:
            if prot.lower() == "xrdp":
                addXRDPConnection(username,user_pass,ip, connectionGroupIdentifier)

    
    #deleteConnectionGroup(username)
    #deleteUser(username)