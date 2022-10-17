import os, base64, sys
print('show hosts in block/black list')

parameter=[] # 4 arguments to receive from user, router-user router-pass router-ip target-id
arguments = [x for x in sys.argv]
help = f'usage: python3 {sys.argv[0]} username password router_ip target_id'
if len(arguments) < 5:
    sys.exit(help)
elif len(arguments) > 5:
    sys.exit(help)
else:
    parameter=[j for j in arguments]

username = parameter[1]
password = parameter[2]
ip = parameter[3]
host_id = parameter[4]
userpass = username+':'+password
bytes = userpass.encode('ascii')
encode = base64.b64encode(bytes)
hashh = str(encode)
hashh = hashh[2:-1]
cookie = hashh

cmd="curl -i -s -k -X 'POST' -H 'Host: "+ip+"' -H 'Content-Length: 97' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36' -H 'Content-Type: text/plain' -H 'Accept: */*' -H 'Origin: http://"+ip+"' -H 'Referer: http://"+ip+"/mainFrame.htm' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9' -H 'Connection: close' -b 'Authorization=Basic "+cookie+"' --data-binary '[LAN_WLAN_MACTABLEENTRY#0,0,0,0,0,0#1,1,0,0,0,0]0,4\x0d\x0aEnabled\x0d\x0aMACAddress\x0d\x0aDescription\x0d\x0aHostName\x0d\x0a' 'http://"+ip+"/cgi?6'"
act=os.popen(cmd)
actr = act.readlines()

if '[error]0' in actr:
    print('password checked successfully')
else:
    sys.exit('error: password may be incorrect')


a=host_id
if '[1,1,'+a+',0,0,0]0' in actr:
    print("address found")

else:
    sys.exit('address not found')


for x in actr:
    if '[1' in x:
        id = x[5:-9]
        print(f'id: {id}')
    elif 'enabled=' in x:
        state = x[7:]
        if '0' in state:
            print('state: disabled')
        elif '1' in state:
            print('state: enabled')
        else:
            print(f'unknown state: {state}')

    elif 'MACAddress=' in x:
        print(x,end='')
    elif 'description=' in x:
            print(x,end='')
    elif 'hostName=' in x:
        print(x)
    else:
        pass
