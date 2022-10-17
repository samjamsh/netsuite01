print('add a host into block/black list')

import os, base64, sys
parameter=[] # waits input of 4 arguments,  username password ip-address mac-address
arguments = [x for x in sys.argv]
help = f'usage: python3 {sys.argv[0]} username password router-ip mac-address state description'
if len(arguments) != 5 :
    sys.exit(help)
else:
    parameter=[argument for argument in arguments]


username = parameter[1] # router username
password = parameter[2] # router password
userpass = username+':'+password
bytes = userpass.encode('ascii')
encode = base64.b64encode(bytes)
hashh = str(encode)
cookie = hashh[2:-1]

ip = parameter[3] # router ip
mac = parameter[4] # target mac address
state = parameter[5] # state
description = parameter[6] # description

cmd="curl 'http://"+ip+"/cgi?3' -H 'Connection: keep-alive' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62' -H 'Content-Type: text/plain' -H 'Accept: */*' -H 'Origin: http://"+ip+"' -H 'Referer: http://"+ip+"/mainFrame.htm' -H 'Accept-Language: en-US,en;q=0.9' -H 'Cookie: Authorization=Basic "+cookie+"' --data-raw '[LAN_WLAN_MACTABLEENTRY#0,0,0,0,0,0#1,1,0,0,0,0]0,4\r\nEnabled="+state+"\r\nDescription="+description+"\r\nMACAddress="+mac+"\r\nHostName=wlan0\r\n' --compressed --insecure"
result = os.popen(cmd).read()

if '[error]0' in result:
    print('host added successfully.')
else:
    print('error: something went wrong, try again!')
