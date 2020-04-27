import time
from neopixel import *
import argparse
import random

#LED Strip One Setup
STRIP_LEDS = 472 #Total LEDS For Strip
STRIP_PIN = 13 #LED Pin For Strip
STRIP_FREQ = 800000
STRIP_DMA = 10 #Possible change, maybe switch to 5?
STRIP_BRIGHTNESS = 127
STRIP_INVERT = False
STRIP_CHANNEL = 1
STRIP = Adafruit_NeoPixel(STRIP_LEDS, STRIP_PIN, STRIP_FREQ, STRIP_DMA, STRIP_INVERT, STRIP_BRIGHTNESS, STRIP_CHANNEL)
STRIP.begin()

#Master loop varible to keep patterns running
MASTER_LOOP = False


def newBrightness():
    """Function used to set the Strip's brightness"""
    STRIP.setBrightness(STRIP_BRIGHTNESS)

def colorwipe(color, wait_ms=1):
    """Lights up the leds from one end to another with the given color"""
    for i in range(STRIP.numPixels()):
        STRIP.setPixelColor(i, color)
        STRIP.show()
        time.sleep(wait_ms/1000.0)

def revColorWipe(color, wait_ms=1):
    """Lights up the leds like colorwipe, but in reverse"""
    for i in range(STRIP.numPixels()):
        STRIP.setPixelColor(STRIP.numPixels() - i, color)
        STRIP.show()
        time.sleep(wait_ms/1000.0)


def pulseColor(color, wait_ms=100):
    """Turns on all the leds a select color, then turns them all off, making them flash"""
    for i in range(STRIP.numPixels()):
        STRIP.setPixelColor(i, color)
    STRIP.show()
    time.sleep(wait_ms/1000.0)
    for t in range(STRIP.numPixels()):
        STRIP.setPixelColor(t, Color(0,0,0))
    STRIP.show()
    time.sleep(wait_ms/1000.0)
    
def runRave():
    """Runs the pulseColor function forever until Master Loop is false"""
    while MASTER_LOOP == True:
        pulseColor(Color(0,255,0))

def theaterChase(color,wait_ms=50, times=20):
    """Function used to create the theater chase animation"""
    for j in range(times):
        for q in range(3):
            for i in range(0, STRIP.numPixels(), 3):
                STRIP.setPixelColor(i+q, color)
            STRIP.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, STRIP.numPixels(), 3):
                STRIP.setPixelColor(i+q, Color(0,0,0))
                
def theaterChaseGreen(wait_ms=50, times=20):
    """Function used to create the theater chase animation"""
    for j in range(times):
        for q in range(3):
            for i in range(0, STRIP.numPixels(), 3):
                STRIP.setPixelColor(i+q, Color(0,255,0))
            STRIP.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, STRIP.numPixels(), 3):
                STRIP.setPixelColor(i+q, Color(0,0,0))

def staticColor(red,green,blue):
    """Sets all the leds to a given color with the red, green, blue values provided"""
    for i in range(STRIP.numPixels()):
        STRIP.setPixelColor(i, Color(red,green,blue))
    STRIP.show()

def runColorCycle():
    """Runs a random animation and color forever untill Master Loop is false"""
    while MASTER_LOOP:
        type = random.randint(0,1)
        if type == 0:
            colorwipe(Color(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        if type == 1:
            theaterChase(Color(random.randint(0,255), random.randint(0,255),random.randint(0,255)))
        

def startUp():
    """Function called when the web server first starts to show it is working"""
    colorwipe(Color(255,0,0))
    revColorWipe(Color(0,255,0))
    colorwipe(Color(0,0,255))
    revColorWipe(Color(0,0,0))
    pulseColor(Color(0,255,0))
    pulseColor(Color(0,255,0))
    pulseColor(Color(0,255,0))
    pulseColor(Color(0,255,0))


def turnOff():
    """Sets all leds to 'off' (Black)"""
    colorwipe(Color(0,0,0))

def runCanadaDayAnimation():
    """Runs two theater chase animations, one red and one white"""
    while MASTER_LOOP:
        theaterChase(Color(255,255,255))
        theaterChase(Color(255,0,0))

def runTheater():
    """Runs theater chase forever until Master Loop is false"""
    while MASTER_LOOP:
        theaterChase(Color(255,255,255))
        

def runTheaterGreen():
    """Runs theater chase forever until Master Loop is false"""
    while MASTER_LOOP:
        theaterChaseGreen()

