import os, base64, sys

def parameters_control():
    max_argvs = 4
    parameters = sys.argv
    parameter_lenght = len(parameters)-1
    help = f'usage: python3 {parameters[0]} router-address username password state'

    if parameter_lenght != max_argvs:
        sys.exit(help)

    else:
        pass

def user_inputs():

    try:
        ip = sys.argv[1]
        user = sys.argv[2]
        passwd = sys.argv[3]
        state = sys.argv[4]

        if state == '1':
            operation = 'enabled'
#            enable()

        elif state == '2':
            operation = 'disabled'
            state = '0'
#            disable()

        else:
            sys.exit('error: invalid option!')

        return ip, user, passwd, state, operation

    except Exception as err:
        sys.exit(err)


def main(ip,user,passwd,state,operation,path):
    try:

        credentials = user+':'+passwd
        credential_bytes = credentials.encode('ascii')
        credential_encoded = base64.b64encode(credential_bytes)
        cookie = str(credential_encoded)[2:-1]
        request = f"curl 'http://{ip}/cgi?2' -H 'Accept: */*' -H 'Accept-Language: pt-BR,pt;q=0.9' -H 'Connection: keep-alive' -H 'Content-Type: text/plain' -H 'Cookie: Authorization=Basic {cookie}' -H 'Origin: http://{ip}' -H 'Referer: http://{ip}/mainFrame.htm' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53' --data-raw '[LAN_WLAN#1,1,0,0,0,0#0,0,0,0,0,0]0,1\r\nMACAddressControlEnabled={state}\r\n' --compressed --insecure"
        response = os.popen(request).read()

    except Exception as err:
        sys.exit(err)

    response_ok = '[error]0'
    if response == response_ok:
        print(f'{operation} done successfully')

    else:
        print('error: execution terminated without success, try again!')

path = '' # reserved to be used an api
parameters_control()
ip, user, passwd, state, operation = user_inputs()
main(ip,user,passwd,state,operation,path)
