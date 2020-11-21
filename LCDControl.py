import requests
import json
import digitalio
import board
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import adafruit_rgb_display.ili9341 as ili9341

class LCD:

    def __init__(self):
        self.FONTSIZE = 18
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
        self.outlineColor = (30,30,30)
        self.bgColor = (50,50,50)
        self.textColor = (0,0,255)
        self.buttonColor = (0,0,255)
        self.barColor = self.textColor
        self.height = self.disp.width 
        self.width = self.disp.height
        self.currentPos = 0
        self.barPos = 190
        self.barHeight = 4
        self.barWidth = 280
        self.songlength = 0
        self.albumURL = ""
        self.songName = ""
        self.artist = ""
        self.largeFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", self.FONTSIZE+6)
        self.medFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", self.FONTSIZE)
        self.smallFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", self.FONTSIZE-6)
        self.drawBg()
        self.drawSongDetails()
        self.drawButtons()
        self.drawBar(0)

    def drawAlbumArt(self):
        img = 0
        if (self.albumURL != ""):
            res = requests.get(self.albumURL)
            img = Image.open(BytesIO(res.content))
            img = img.resize((75, 75), Image.BICUBIC)
        else:
            img = Image.new("RGB", (75, 75))
            draw = ImageDraw.Draw(img)
            draw.rectangle(
                (0, 0, 75, 75),
                fill=self.bgColor
            )
        self.disp.image(img, None, 50, 200)

    def getArtist(self):
        return self.artist

    def getSong(self):
        if (self.songName != ""):
            return self.songName.upper()
        else:
            return ""
        
    def drawBg(self):
        image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,self.width,self.height),fill=0)
        self.disp.image(image)
        
    def drawSongDetails(self):
        image = Image.new("RGB", (self.width, 140))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,self.width,140),fill=0)
        draw.text(
            (130, 60),
            self.getSong(),
            font=self.medFont,
            fill=self.textColor,
        )
        draw.text(
            (130, 85),
            self.getArtist(),
            font=self.smallFont,
            fill=self.textColor,
        )
        self.disp.image(image)
        self.drawAlbumArt()

    def drawButtons(self):
        image = Image.new("RGB", (self.width, 32))
        draw = ImageDraw.Draw(image)
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
        self.disp.image(image, None, 142, 0)
        
    def drawBar(self, perc):
        image = Image.new("RGB", (self.width, 55))
        draw = ImageDraw.Draw(image)
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
        self.disp.image(image, None, 185, 0)
        self.currentPos = perc
    def updateBar(self, perc):
        if (perc != self.currentPos):
            self.drawBar(perc)
