import os, base64, sys
parameter=[] # expected 4 arguments, user pass ip mac
arguments = [x for x in sys.argv]
help = f'usage: python3 {sys.argv[0]} username password router_ip id state'
if len(arguments) < 6:
    sys.exit(help)
elif len(arguments) > 6:
    sys.exit(help)
else:
    parameter=[j for j in arguments]


print('disable or enable host in block list')
username = parameter[1]
password = parameter[2]
userpass = username+':'+password
bytes = userpass.encode('ascii')
encode = base64.b64encode(bytes)
hashh = str(encode)
cookie = hashh[2:-1]
router_ip = parameter[3] # router address
id = parameter[4] # device id
state = parameter[5] # state (enable/disable)

cmd = "curl 'http://"+ router_ip +"/cgi?2' -H 'Connection: keep-alive' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62' -H 'Content-Type: text/plain' -H 'Accept: */*' -H 'Origin: http://" +router_ip+ "' -H 'Referer: http://"+router_ip+"/mainFrame.htm' -H 'Accept-Language: en-US,en;q=0.9' -H 'Cookie: Authorization=Basic " + cookie + "' --data-raw '[LAN_WLAN_MACTABLEENTRY#1,1,"+id+",0,0,0#0,0,0,0,0,0]0,1\r\nEnabled=" + state + "\r\n' --compressed --insecure"
import os
ans = os.popen(cmd).read()

if '[error]0' in ans:
    if state=='1':
        print('host enabled successfully!');
    else:
        print('host disabled successfully!');
else:
    print('error, not completed correctly.');
