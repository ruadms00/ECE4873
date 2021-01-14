import os
import subprocess

class File:
    
    
    def updateUserInfo(self, user, pw):
        file = open("/etc/default/raspotify", "r")
        contents = file.readlines()
        file.close()
        try:
            index = [idx for idx, s in enumerate(contents) if "OPTIONS=" in s][0]
            contents[index] = "OPTIONS=\"--username {} --password {} --device hw:1,0\"\n".format(user, pw)
            file2 = open("/etc/default/raspotify", "w")
            data = "".join(contents)
            file2.write(data)
            file2.flush()
            os.fsync(file2.fileno())
            file2.close()
            subprocess.call('systemctl restart raspotify', shell=True)
        except:
            print('update info failed')
            
    def writeSecrets(self, token, refresh):
        try:
            with open("secrets.txt", "w+") as file:
                data = token + '\n' + refresh
                file.write(data)
                file.flush()
                os.fsync(file.fileno())
            return True
        except:
            return False

    def checkSecrets(self):
        try:
            with open("secrets.txt", "r") as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    return True
        except:
            print('exception while checking secrets')
        return False

    def updateWifi(self, network, password):
        if network == "":
            return False
        try:
            testNet = "\"" + network + "\""
            file = open("/etc/wpa_supplicant/wpa_supplicant.conf", "r")
            contents = file.readlines()
            file.close()
            index = [idx for idx, s in enumerate(contents) if testNet in s][0]
            if not "\"" + password + "\"" in contents[index+1]:
                contents[index+1] = '\tpsk="{}"\n'.format(password)
                file2 = open("/etc/wpa_supplicant/wpa_supplicant.conf", "w")
                data = "".join(contents)
                file2.write(data)
                file2.flush()
                os.fsync(file2.fileno())
                file2.close()
                subprocess.call('wpa_cli -i wlan0 reconfigure', shell=True)
            return True
        except:
            print('new network not in file')
        try:
            with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a+") as file3:
                config_lines = [
                    '\n',
                    'network={',
                    '\tssid="{}"'.format(network),
                    '\tpsk="{}"'.format(password),
                    '\tkey_mgmt=WPA-PSK',
                    '}'
                ]
                for item in config_lines:
                    file3.write("%s\n" % item)
                file3.flush()
                os.fsync(file3.fileno())
                subprocess.call('wpa_cli -i wlan0 reconfigure', shell=True)
            return True
        except:
            return False

    
    def removeWifi(self, network):
        if network == "":
            return False
        try:
            testNet = "\"" + network + "\""
            file = open("/etc/wpa_supplicant/wpa_supplicant.conf", "r")
            contents = file.readlines()
            file.close()
            index = [idx for idx, s in enumerate(contents) if testNet in s][0]
            del contents[index-2:index+4]
            file2 = open("/etc/wpa_supplicant/wpa_supplicant.conf", "w")
            data = "".join(contents)
            file2.write(data)
            file2.flush()
            os.fsync(file2.fileno())
            file2.close()
            return True
        except:
            return False
        
