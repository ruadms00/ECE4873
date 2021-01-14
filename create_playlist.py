import time
import threading
import socket
from SpotifyAction import Spotify
from FileManager import File
from LCDControl import LCD
from wifi import Cell
import urllib

mutex = False

wifiNetworks = []
hideNetworks = []

wifiOn = True

spotify = Spotify()
file = File()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)
secretsInitialized = False

lcd = LCD()

def drawPage0():
    global mutex
    global spotify
    if spotify.initialized:
        while mutex:
            time.sleep(.001)
        if lcd.Page == 0:
            mutex = True
            song = spotify.getSongInfo()
            if song:
                if (song['item']['name'] != lcd.songName):
                    lcd.albumURL = song['item']['album']['images'][1]['url']
                    lcd.songName = song['item']['name']
                    lcd.artist = song['item']['artists'][0]['name']
                    lcd.songLength = song['item']['duration_ms'] // 1000
                    lcd.drawSongDetails()
                progress = song['progress_ms'] // 1000
                lcd.updateBar(progress/lcd.songLength)
            mutex = False

def drawPage1():
    global mutex
    while mutex:
        time.sleep(.001)
    if lcd.Page == 1:
        mutex = True
        lcd.drawWifiPage()
        mutex = False
    
def drawPage2():
    global mutex
    global wifiNetworks
    newNetworks = []
    try:
        cells = Cell.all('wlan0')
        for cell in cells:
            if not cell.ssid in newNetworks and not cell.ssid in hideNetworks:
                newNetworks.append(cell.ssid)
            if len(newNetworks) >= 7:
                break
        if set(newNetworks) == set(wifiNetworks):
            return
        wifiNetworks = newNetworks[:]
        while mutex:
            time.sleep(.001)
        if lcd.Page == 2:
            mutex = True
            lcd.drawWifiNetworks(wifiNetworks)
            mutex = False
    except:
        pass
    
def updateLCDInfo():
    global wifiOn
    global lcd
    global mutex
    while True:
        if lcd.Page == 0:
            try:
                urllib.request.urlcleanup()
                url = urllib.request.urlopen("https://www.google.com", timeout=1)
                wifiOn = True
                drawPage0()
            except:
                print('url reach failed')
                wifiOn = False
                while mutex:
                    time.sleep(.001)
                mutex = True
                lcd.updatePage(1)
                mutex = False
                drawPage1()
        elif lcd.Page == 1:
            try:
                urllib.request.urlcleanup()
                url = urllib.request.urlopen("https://www.google.com", timeout=1)
                wifiOn = True
                while mutex:
                    time.sleep(.001)
                mutex = True
                lcd.updatePage(0)
                mutex = False
                drawPage0()
            except:
                print('url reach failed')
                drawPage1()
        elif lcd.Page == 2:
            drawPage2()
        time.sleep(.5) 

        
def initSecrets():
    try:
        s.connect(('76.17.103.152',50007))
        data = 'req:::'
        s.sendall(data.encode())
        string = s.recv(1024).decode()
        args = string.split(':::')
        if len(args) >= 2:
            s.close()
            secretsInitialized = file.writeSecrets(args[0], args[1])
    except:
        secretsInitialized = file.checkSecrets()


if __name__ == '__main__':
    lcdThread = threading.Thread(target=updateLCDInfo)
    lcdThread.start()
    if wifiOn:
        initSecrets()
    while True:
        cmd = lcd.getData()
        if cmd != 0:
            if lcd.Page == 0:
                if spotify.initialized:
                    if cmd == 1:
                        spotify.prevSong()
                    elif cmd == 2:
                        spotify.play()
                    elif cmd == 3:
                        spotify.pause()
                    elif cmd == 4:
                        spotify.nextSong()
                    elif cmd == 5:
                        while mutex:
                            time.sleep(.001)
                        mutex = True
                        wifiNetworks = []
                        lcd.updatePage(2)
                        mutex = False
                    elif cmd > 50:
                        print(cmd)
                        pos = int((cmd - 50) / 280 * lcd.songLength * 1000)
                        print(pos)
                        spotify.updatePosition(pos)
            elif lcd.Page == 1:
                if cmd == 1:
                    while mutex:
                        time.sleep(.001)
                    mutex = True
                    wifiNetworks = []
                    lcd.updatePage(2)
                    mutex = False
            elif lcd.Page == 2:
                if cmd == 11:
                    while mutex:
                        time.sleep(.001)
                    mutex = True
                    if wifiOn:
                        lcd.updatePage(0)
                    else:
                        lcd.updatePage(1)
                    mutex = False
                elif cmd == 8:
                    while mutex:
                        time.sleep(.001)
                    mutex = True
                    lcd.updatePage(3)
                    user = spotify.user_id
                    lcd.drawPasswordPage(user, False)
                    pw = lcd.getPassword(user, False)
                    if type(pw) == str:
                        file.updateUserInfo(user, pw)
                    lcd.updatePage(0)
                    mutex = False
                elif cmd <= len(wifiNetworks):
                    while mutex:
                        time.sleep(.001)
                    mutex = True
                    lcd.updatePage(3)
                    inText = wifiNetworks[cmd-1]
                    lcd.drawPasswordPage(inText)
                    pw = lcd.getPassword(inText)
                    if type(pw) == str:
                        file.updateWifi(inText, pw)
                    elif pw == 1:
                        hideNetworks.append(inText)
                    elif pw == 2:
                        file.removeWifi(inText)
                    lcd.updatePage(0)
                    mutex = False
            time.sleep(1)
        else:
            if not spotify.initialized and wifiOn:
                spotify.initializeVariables()
                time.sleep(.25)
            if not spotify.initialized and wifiOn and not secretsInitialized:
                initSecrets()
        time.sleep(.001)
    