import requests
import json
import digitalio
import board
import time
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from adafruit_stmpe610 import Adafruit_STMPE610_I2C
import adafruit_rgb_display.ili9341 as ili9341

class LCD:

    def __init__(self):
        self.FONTSIZE = 15
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = digitalio.DigitalInOut(board.D24)
        BAUDRATE = 24000000
        spi = board.SPI()
        self.disp = ili9341.ILI9341(
            spi,
            rotation=90,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=BAUDRATE,
        )
        self.st = Adafruit_STMPE610_I2C(board.I2C())
        self.outlineColor = (30,30,30)
        self.bgColor = (50,50,50)
        self.textColor = (0,0,255)
        self.buttonColor = (0,0,255)
        self.barColor = self.textColor
        self.height = self.disp.width 
        self.width = self.disp.height
        self.Page = 0
        self.currentPos = 0
        self.barPos = 190
        self.barHeight = 4
        self.barWidth = 280
        self.songlength = 0
        self.charList = "1234567890qwertyuiopasdfghjklzxcvbnm"
        self.secondList = "1234!@#$%^&*()-_=+[]{}\|/;:\'\",.<>?`~"
        self.passText = ""
        self.albumURL = ""
        self.songName = ""
        self.artist = ""
        self.medFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", self.FONTSIZE)
        self.smallFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", self.FONTSIZE-3)
        self.drawStartup()
    
    def clearData(self):
        try:
            while not self.st.buffer_empty:
                ts = self.st.touches
        except:
            print('clear data failed')

    def getPassword(self, inText, buttons = True):
        upperCase = False
        secondKey = False
        passText = ""                                                                                                     
        self.Page = 3
        while True:
            cmd = self.getData(secondKey)
            if type(cmd) == str:
                if upperCase:
                    cmd = cmd.upper()
                passText += cmd
                self.updatePassword(passText)
            elif cmd == 1:
                return 0
            elif cmd == 2:
                upperCase = not upperCase
                self.drawShift(upperCase)
            elif cmd == 3:
                passText = passText[:-1]
                self.updatePassword(passText)
            elif cmd == 4:
                secondKey = not secondKey
                self.drawKeyboard(secondKey, upperCase)
            elif cmd == 5:
                return passText
            elif cmd == 6:
                passText += ' '
                self.updatePassword(passText)
            elif cmd == 7:
                passText = ""
                self.updatePassword(passText)
            elif cmd == 8 and buttons:
                return 1
            elif cmd == 9 and buttons:
                return 2
            if cmd != 0:
                time.sleep(.15)
            time.sleep(.001)
        return passText
    
    def getKeyboardInput(self, x, y, secondKey):
        chars = self.charList
        if secondKey:
            chars = self.secondList
        if y > 190 and y < 216 and x < 80:
            return 2
        elif y > 190 and y < 216 and x > 301:
            return 3
        elif y > 216 and x < 111:
            return 4
        elif y > 216 and x > 270:
            return 5
        elif y > 216 and x > 111 and x < 208:
            return 6
        elif y > 216 and x > 208 and x < 270:
            return 7
        elif y > 117 and y < 138 and x > 34 and x < 344:
            return chars[((x-65)//31+1)]
        elif y > 138 and y < 164 and x > 34 and x < 344:
            return chars[((x-65)//31+1)+10]
        elif y > 164 and y < 190 and x > 49 and x < 332:
            return chars[((x-80)//31+1)+20]
        elif y > 190 and y < 216 and x > 80 and x < 301:
            return chars[((x-111)//31+1)+29]
        return 0
    
    def getData(self, secondKey = False):
        self.clearData()
        time.sleep(.01)
        if self.st.touched:
            while not self.st.buffer_empty:
                ts = self.st.touches
                for point in ts:
                    # perform transformation to get into display coordinate system!
                    y1 = point["y"]
                    x1 = 4096 - point["x"]
                    x1 = 2 * x1 // 30
                    y1 = 8 * y1 // 90
                    x = y1
                    y = x1
                    #print('x ' + str(x) + '    y ' + str(y))
                    if self.Page == 0:
                        if y > 150 and y < 190:
                            if x > 70 and x < 115:
                                return 1
                            elif x > 140 and x < 185:
                                return 2
                            elif x > 210 and x < 250:
                                return 3
                            elif x > 270 and x < 310:
                                return 4
                        if y < 55 and x > 275:
                            return 5
                    elif self.Page == 1:
                        if x > 80 and x < 240 and y > 120 and y < 160:
                            return 1
                    elif self.Page == 2:
                        if y < 55 and x > 275:
                            return 11
                        elif y > 215 and x < 190:
                            return 8
                        elif y > 45 and x < 330:
                            return 2*((y-75)//35)+(x//190)+1
                    elif self.Page == 3:
                        if y < 55 and x > 275:
                            return 1
                        elif y < 80 and y > 55 and x > 265:
                            return 8
                        elif y < 105 and y > 80 and x > 265:
                            return 9
                        else:
                            return self.getKeyboardInput(x, y, secondKey)
        return 0
    
    def updateUserInfo(self, password):
        return 0
    
    def updateWifi(self, network, password):
        if network == "":
            return 0
        testNet = "\"" + network + "\""
        file = open("/etc/wpa_supplicant/wpa_supplicant.conf", "r")
        contents = file.readlines()
        file.close()
        try:
            index = [idx for idx, s in enumerate(contents) if testNet in s][0]
            if not "\"" + password + "\"" in contents[index+1]:
                print('update')
                contents[index+1] = '\tpsk="{}"\n'.format(password)
                file2 = open("/etc/wpa_supplicant/wpa_supplicant.conf", "w")
                data = "".join(contents)
                file2.write(data)
                file2.flush()
                os.fsync(file2.fileno())
                file2.close()
                return 1
            else:
                print('already in file')
                return 0
        except:
            print('not in file')
        print('adding new wpa')
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
        return 2
    
    def removeWifi(self, network):
        if network == "":
            return 0
        testNet = "\"" + network + "\""
        file = open("/etc/wpa_supplicant/wpa_supplicant.conf", "r")
        contents = file.readlines()
        file.close()
        try:
            index = [idx for idx, s in enumerate(contents) if testNet in s][0]
            del contents[index-2:index+4]
            file2 = open("/etc/wpa_supplicant/wpa_supplicant.conf", "w")
            data = "".join(contents)
            file2.write(data)
            file2.flush()
            os.fsync(file2.fileno())
            file2.close()
        except:
            return 1
        return 2
        
    def updatePage(self, newPage):
        self.Page = newPage
        if newPage == 0:
            self.drawStartup()
        elif newPage == 1:
            self.clearLcd()
            self.drawWifiPage()
        elif newPage == 2:
            self.clearLcd()
            self.drawConfig()
        elif newPage == 3:
            self.clearLcd()
            self.drawConfig()
            
    def drawStartup(self):
        self.clearLcd()
        self.drawConfig()
        self.drawButtons()
        self.drawBar(self.currentPos)
        self.drawSongDetails()
    
    def drawWifiPage(self):
        image = Image.new("RGB", (self.width, 140))
        draw = ImageDraw.Draw(image)
        draw.text(
            (100, 90),
            "WiFi Unavailable",
            font=self.medFont,
            fill=self.textColor
        )
        draw.rectangle(
            (80, 120, 240, 160),
            fill=self.bgColor
        )
        draw.text(
            (98, 121),
            "SEE NETWORKS",
            font=self.medFont,
            fill=self.textColor
        )
        self.disp.image(image, None, 0, 0)
    
    def drawWifiNetworks(self, networks):
        img = Image.new("RGB", (self.width, self.height-40))
        draw = ImageDraw.Draw(img)
        draw.text(
            (120, 0),
            "WiFi Selection",
            font=self.medFont,
            fill=self.textColor
        )
        for i, net in enumerate(networks):
            if i < 6:
                draw.rectangle(
                    (10+(i%2)*160, 20+35*(i//2), 150+(i%2)*160, 50+35*(i//2)),
                    fill=self.bgColor
                )
                draw.text(
                    (15+(i%2)*160, 28+35*(i//2)),
                    net[:14],
                    font=self.smallFont,
                    fill=self.textColor
                )
        draw.rectangle(
            (10, 160, 150, 190),
            fill=self.bgColor
        )
        draw.text(
            (23, 168),
            "SPOTIFY CONNECT",
            font=self.smallFont,
            fill=self.textColor
        )
        self.disp.image(img, None, 40, 0)
    
    def drawShift(self, upperCase):
        img = Image.new("RGB", (42, 22))
        draw = ImageDraw.Draw(img)
        if upperCase:
            draw.rectangle(
                (0, 0, 42, 22),
                fill=self.textColor
            )
            draw.text(
                (5, 3),
                "shift",
                font=self.medFont,
                fill=self.bgColor
            )
        else:
            draw.rectangle(
                (0, 0, 42, 22),
                fill=self.bgColor
            )
            draw.text(
                (5, 3),
                "shift",
                font=self.medFont,
                fill=self.textColor
            )
        self.disp.image(img, None, 173, 271)
    
    def drawKeyboard(self, secondKey, upperCase):
        img = Image.new("RGB", (self.width, self.height-95))
        draw = ImageDraw.Draw(img)
        chars = self.charList
        if secondKey:
            chars = self.secondList
        for idx, letter in enumerate(chars):
            x = 0
            y = 0
            if idx < 20:
                x = 7 + (idx%10)*31
                y = 0 + (idx//10)*26
            elif idx < 29:
                x = 22 + (idx%10)*31
                y = 0 + (idx//10)*26
            else:
                x = 53 + ((idx+1)%10)*31
                y = 0 + ((idx+1)//10)*26
            draw.rectangle(
                (x, y, x + 27, y + 22),
                fill=self.bgColor
            )
            draw.text(
                (x+8, y+3),
                letter,
                font=self.medFont,
                fill=self.textColor
            )
        draw.rectangle(
            (270, 78, 313, 100),
            fill=self.bgColor
        )
        draw.text(
            (273, 81),
            "bksp",
            font=self.medFont,
            fill=self.textColor
        )
        draw.rectangle(
            (84, 104, 173, 126),
            fill=self.bgColor
        )
        draw.rectangle(
            (239, 104, 313, 126),
            fill=self.bgColor
        )
        draw.text(
            (250, 107),
            "submit",
            font=self.medFont,
            fill=self.textColor
        )
        if secondKey:
            draw.rectangle(
                (7, 104, 80, 126),
                fill=self.textColor
            )
            draw.text(
                (29, 107),
                "!#1",
                font=self.medFont,
                fill=self.bgColor
            )
        else:
            draw.rectangle(
                (7, 104, 80, 126),
                fill=self.bgColor
            )
            draw.text(
                (29, 107),
                "!#1",
                font=self.medFont,
                fill=self.textColor
            )
        if upperCase:
            draw.rectangle(
                (7, 78, 49, 100),
                fill=self.textColor
            )
            draw.text(
                (12, 81),
                "shift",
                font=self.medFont,
                fill=self.bgColor
            )
        else:
            draw.rectangle(
                (7, 78, 49, 100),
                fill=self.bgColor
            )
            draw.text(
                (12, 81),
                "shift",
                font=self.medFont,
                fill=self.textColor
            )
        draw.rectangle(
            (177, 104, 235, 126),
            fill=self.bgColor
        )
        draw.text(
            (188, 107),
            "clear",
            font=self.medFont,
            fill=self.textColor
        )
        self.disp.image(img, None, 95, 0)
                
                
    def updatePassword(self, passText):
        img = Image.new("RGB", (self.width-80, 25))
        draw = ImageDraw.Draw(img)
        draw.text(
            (10, 0),
            "Password: {}".format(passText[-12:]),
            font=self.medFont,
            fill=self.textColor
        )
        self.disp.image(img, None, 60, 80)
    
    def drawPasswordPage(self, network, buttons = True):
        img = Image.new("RGB", (self.width, self.height-40))
        draw = ImageDraw.Draw(img)
        if buttons:
            draw.text(
                (10, 0),
                "Connect To: {}".format(network),
                font=self.medFont,
                fill=self.textColor
            )
            draw.rectangle(
                (240, 5, 310, 25),
                fill=self.bgColor
            )
            draw.text(
                (262, 8),
                "HIDE",
                font=self.smallFont,
                fill=self.textColor
            ) 
            draw.rectangle(
                (240, 30, 310, 50),
                fill=self.bgColor
            )
            draw.text(
                (250, 33),
                "FORGET",
                font=self.smallFont,
                fill=self.textColor
            )
        else:
            draw.text(
                (10, 0),
                "Username: {}".format(network),
                font=self.medFont,
                fill=self.textColor
            )
        self.disp.image(img, None, 40, 0)
        self.drawKeyboard(False, False)
        self.updatePassword("")
    
    def drawAlbumArt(self):
        img = 0
        if (self.albumURL != ""):
            try:
                res = requests.get(self.albumURL)
                img = Image.open(BytesIO(res.content))
                img = img.resize((75, 75), Image.BICUBIC)
            except:
                img = Image.new("RGB", (75, 75))
                draw = ImageDraw.Draw(img)
                draw.rectangle(
                    (0, 0, 75, 75),
                    fill=self.bgColor
                )
        else:
            img = Image.new("RGB", (75, 75))
            draw = ImageDraw.Draw(img)
            draw.rectangle(
                (0, 0, 75, 75),
                fill=self.bgColor
            )
        if self.Page == 0:
            self.disp.image(img, None, 50, 200)

    def getArtist(self):
        return self.artist

    def getSong(self):
        if (self.songName != ""):
            return self.songName.upper()
        else:
            return ""
        
    def drawConfig(self):
        img = Image.new("RGB", (100, 40))
        draw = ImageDraw.Draw(img)
        if self.Page == 0:
            draw.rectangle(
                (30, 10, 90, 40),
                fill=self.bgColor
            )
            draw.text(
                (37, 17),
                "CONFIG",
                font=self.smallFont,
                fill=self.textColor
            )
        elif self.Page == 2:
            draw.rectangle(
                (30, 10, 90, 40),
                fill=self.bgColor
            )
            draw.text(
                (42, 17),
                "HOME",
                font=self.smallFont,
                fill=self.textColor
            )
        elif self.Page == 3:
            draw.rectangle(
                (30, 10, 90, 40),
                fill=self.bgColor
            )
            draw.text(
                (44, 17),
                "BACK",
                font=self.smallFont,
                fill=self.textColor
            )
        self.disp.image(img, None, 0, 0)
        
    def clearLcd(self):
        img = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0,0,self.width,self.height),fill=0)
        self.disp.image(img)
        
    def drawSongDetails(self):
        img = Image.new("RGB", (self.width, 100))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0,0,self.width,100),fill=0)
        draw.text(
            (130, 25),
            self.getSong()[0:22],
            font=self.medFont,
            fill=self.textColor,
        )
        draw.text(
            (130, 45),
            self.getArtist(),
            font=self.smallFont,
            fill=self.textColor,
        )
        self.disp.image(img, None, 40, 0)
        self.drawAlbumArt()

    def drawButtons(self):
        img = Image.new("RGB", (self.width, 32))
        draw = ImageDraw.Draw(img)
        #previous button
        draw.ellipse(
            (49, 0, 79, 30),
            outline=self.outlineColor,
            fill=self.bgColor
        )
        draw.polygon(((55, 15),(63, 22),(63, 8)), fill=self.buttonColor)
        draw.polygon(((63, 15),(71, 22),(71, 8)), fill=self.buttonColor)
        #next button
        draw.ellipse(
            (241, 0, 271, 30),
            outline=self.outlineColor,
            fill=self.bgColor
        )
        draw.polygon(((265, 15),(257, 22),(257, 8)), fill=self.buttonColor)
        draw.polygon(((257, 15),(249, 22),(249, 8)), fill=self.buttonColor)
        #play button
        draw.ellipse(
            (113, 0, 143, 30),
            outline=self.outlineColor,
            fill=self.bgColor
        )
        draw.polygon(((125, 22),(125, 8),(133, 15)), fill=self.buttonColor)
        #pause button
        draw.ellipse(
            (177, 0, 207, 30),
            outline=self.outlineColor,
            fill=self.bgColor
        )
        draw.rectangle(
            (185, 8, 190, 22),
            fill=self.buttonColor
        )
        draw.rectangle(
            (194, 8, 199, 22),
            fill=self.buttonColor
        )
        self.disp.image(img, None, 142, 0)
        
    def drawBar(self, perc):
        img = Image.new("RGB", (self.width, 55))
        draw = ImageDraw.Draw(img)
        draw.ellipse(
            (15+int(280*self.currentPos), 2, 25+int(280*self.currentPos), 12),
            outline=(0,0,0),
            fill=(0,0,0)
        )
        draw.rectangle(
            (20, 5, 300, 9),
            fill=self.barColor
        )
        draw.ellipse(
            (15+int(280*perc), 2, 25+int(280*perc), 12),
            outline=self.barColor,
            fill=(0,0,0)
        )
        self.disp.image(img, None, 185, 0)
        self.currentPos = perc
        
    def updateBar(self, perc):
        if (perc != self.currentPos):
            self.drawBar(perc)
