import os, base64, sys

parameter=[] # 3 arguments expected, user pass ip
arguments = [x for x in sys.argv]
help = f'usage: python3 {sys.argv[0]} username password router_ip'
if len(arguments) < 4:
    sys.exit(help)
elif len(arguments) > 4:
    sys.exit(help)
else:
    parameter=[j for j in arguments]


print('show connected devices into network')
user = parameter[1]
passw = parameter[2]
ip = parameter[3]

b=user+':'+passw
cooking=base64.b64encode(b.encode('ascii'))
cooked=str(cooking)
cookie = cooked[2:-1]
print('checking credentials')

request_command = f"curl -i -s -k -X 'POST'     -H 'Host: "+ip+"' -H 'Content-Length: 98' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52' -H 'Content-Type: text/plain' -H 'Accept: */*' -H 'Origin: http://"+ip+"' -H 'Referer: http://"+ip+"/mainFrame.htm' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9,pt;q=0.8,it;q=0.7' -H 'Connection: close'     -b 'Authorization=Basic "+cookie+"'     --data-binary '[LAN_HOST_ENTRY#0,0,0,0,0,0#0,0,0,0,0,0]0,4\x0d\x0aleaseTimeRemaining\x0d\x0aMACAddress\x0d\x0ahostName\x0d\x0aIPAddress\x0d\x0a'     'http://"+ip+"/cgi?5'| egrep 'MAC|host|IP'"
data = os.popen(request_command).read()

#############################

def clients_database(all_data):
    client = ''
    clients_data = []
    for data in all_data:
        if data != '\n':
            client+=data

        else:
            clients_data.append(client)
            client = ''

    clients_number = int(len(clients_data) / 3) # number of connected devices
    print(f'total devices: {clients_number}')
    return clients_number, clients_data

############################

def clients_info(clients_number,clients_data):
    x = 2
    i = 0
    z = 1

    for j in range(clients_number):
        client_mac = clients_data[i][len('MACAddress='):]
        client_name = clients_data[z][len('hostName='):]
        client_ip = clients_data[x][len('IPAddress='):]

        print(f'id: {j+1} device name: {client_name}, ip address: {client_ip}, mac address: {client_mac}')
        i = i + 3
        x = x + 3
        z = z + 3

#############################

def block_client(data, client_id, router_user, router_pass, router_ip):
# del = id*3 ex = 3 -2 = 1, id * 3 -2 = delete user
# delete user
# add client in block list already in block state
#    info = router_user,router_pass,router_ip,' ? '
#    confirm = input(info)
    path = '' # reserved to be used as an api
    state = '1'
    description = "user_blocked_by_netsuite"
    client_mac_address = data[client_id*3][len('MACAddress='):] # client mac address to block (put in black list and then block it)
    add_in_block_list = f"python3 {path}add.py {router_user} {router_pass} {router_ip} {client_mac_address} {state} {description}"
    print(f'command: {add_in_block_list}')
    os.system(f'{add_in_block_list}')

if len(data) < 1:
    print('error: connection error, try again!')

else:
    print('credentials checked correctly!')
    clients_number, clients_data = clients_database(data)
    clients_info(clients_number,clients_data)
    option = input('do you want to block any device? ')
    if option == 'y' or option == 'yes':
        id = int(input('id number: '))-1
        block_client(clients_data,id,user,passw,ip)

    else:
        print('exiting program...')
