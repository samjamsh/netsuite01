import os, base64, sys
parameter=[] # 5 args, user pass ip new-user new-pass
arguments = [x for x in sys.argv]
help = f'usage: python3 {sys.argv[0]} username password router_ip new_username new_password'
if len(arguments) < 6:
    sys.exit(help)
elif len(arguments) > 6:
    sys.exit(help)
else:
    parameter=[j for j in arguments]

print('change the router username and password');
olduser = parameter[1] # current router user
oldpass = parameter[2] # current router pass
olders=olduser+':'+oldpass
byte=olders.encode('ascii')
bytes=base64.b64encode(byte)
hashh=str(bytes)

cookie=hashh[2:-1]
ip = parameter[3]
newuser = parameter[4]
newpass = parameter[5]

cmd="curl -i -s -k -X 'POST' -H 'Host: "+ip+"' -H 'Content-Length: 77' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36' -H 'Content-Type: text/plain' -H 'Accept: */*' -H 'Origin: http://"+ip+"' -H 'Referer: http://"+ip+"/mainFrame.htm' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9' -H 'Connection: close' -b 'Authorization=Basic "+cookie+"' --data-binary '[/cgi/auth#0,0,0,0,0,0#0,0,0,0,0,0]0,3\x0d\x0aoldPwd="+oldpass+"\x0d\x0aname="+newuser+"\x0d\x0apwd="+newpass+"\x0d\x0a' 'http://"+ip+"/cgi?8'"
ans = os.popen(cmd).read();

if '[cgi]0' in ans and '$.ret=0;' in ans and '[error]0' in ans:
    print('credentials changed successfully!');
else:
    print('error, not completed correctly.');
