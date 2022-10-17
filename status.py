import os, sys, base64

try:
    if len(sys.argv) == 4:

        router = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        userpass = username+':'+password
        bytes = userpass.encode('ascii')
        encode = base64.b64encode(bytes)
        hashh = str(encode)
        cookie = hashh[2:-1]

    else:
        sys.exit(f'usage: {sys.argv[0]} router-address username password')

except Exception as err:
    sys.exit(err)


def request(router,cookies):

    request = f"curl 'http://{router}/cgi?5&5' -H 'Accept: */*' -H 'Accept-Language: pt-BR,pt;q=0.9' -H 'Connection: keep-alive' -H 'Content-Type: text/plain' -H 'Cookie: Authorization=Basic {cookies}' -H 'Origin: http://{router}' -H 'Referer: http://{router}/mainFrame.htm' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49' --data-raw '[LAN_WLAN#0,0,0,0,0,0#0,0,0,0,0,0]0,6\r\nname\r\nStatus\r\nX_TP_MACAddressControlRule\r\nMACAddressControlEnabled\r\nSSID\r\nX_TP_Band\r\n[LAN_WLAN_MSSIDENTRY#0,0,0,0,0,0#0,0,0,0,0,0]1,7\r\nEnable\r\nName\r\nSSID\r\nSSIDAdvertisementEnable\r\nBeaconType\r\nWPAEncryptionModes\r\nIEEE11iEncryptionModes\r\n' --compressed --insecure"
    response = os.popen(request).read()

    response_ok = '[error]0'
    ok_code_lenght = len(response_ok)

    response_lenght = len(response)

    code_check = response[response_lenght - ok_code_lenght:]

    result = (code_check == response_ok)

    if result is True:

        def data_customization(response,option):
            lines = []
            status_on = 'MACAddressControlEnabled=1\n'
            status_off = 'MACAddressControlEnabled=0\n'
            line = ''
            for char in response:
                line += char
                if char == '\n':
                    lines.append(line)
                    line = ''
            status_state = lines[4]
            status_up = status_state == status_on
            status_down = status_state == status_off

            if option == 'status':
                return status_up,status_down

            elif option == 'all':

                for each_line in lines:
                    print(each_line,end='')

            else:
                sys.exit(f'') # reserved to future

        up,down = data_customization(response,'status')
        if up == True and down == False:
            print('state: Enabled')

        else:
            print('state: Disabled')

    else:
        sys.exit(f'error! try again')


request(router,cookie)
