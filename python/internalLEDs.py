import time
from neopixel import *
import argparse
import random

#LED Strip One Setup
STRIP_LEDS = 1188 #Total LEDS For Strip
STRIP_LEDS_PER_STRAND = 108 #LEDS PER BEAM
STRIP_PIN = 18 #LED Pin For Strip 
STRIP_FREQ = 800000
STRIP_DMA = 10
STRIP_BRIGHTNESS = 100 #127
STRIP_INVERT = False
STRIP_CHANNEL = 0
STRIP = Adafruit_NeoPixel(STRIP_LEDS, STRIP_PIN, STRIP_FREQ, STRIP_DMA, STRIP_INVERT, STRIP_BRIGHTNESS, STRIP_CHANNEL)
STRIP.begin()


MASTER_LOOP = False
MOVIE_LIGHT = True
MOVIE_LIGHT_RANGE = 540


def newBrightness():
    """Function used to set the Strip's brightness"""
    STRIP.setBrightness(STRIP_BRIGHTNESS)

def colorwipe(color, wait_ms=1):
    """Lights up the leds from one end to another with the given color"""
    if MOVIE_LIGHT == True:
        for i in range(STRIP.numPixels()):
            STRIP.setPixelColor(i, color)
            STRIP.show()
            time.sleep(wait_ms/1000.0)
    else:
        for i in range(MOVIE_LIGHT_RANGE, STRIP.numPixels()):
            STRIP.setPixelColor(i,color)
            STRIP.show()
            time.sleep(wait_ms/1000.0)

def pulseColor(color, wait_ms=100):
    """Turns on all the leds a select color, then turns them all off, making them flash"""
    if MOVIE_LIGHT == True:
        for i in range(STRIP.numPixels()):
            STRIP.setPixelColor(i, color)
        STRIP.show()
        time.sleep(wait_ms/1000.0)
        for t in range(STRIP.numPixels()):
            STRIP.setPixelColor(t, Color(0,0,0))
        STRIP.show()
        time.sleep(wait_ms/1000.0)
    else:
        for i in range(MOVIE_LIGHT_RANGE, STRIP.numPixels()):
            STRIP.setPixelColor(i, color)
        STRIP.show()
        time.sleep(wait_ms/1000.0)
        for t in range(MOVIE_LIGHT_RANGE, STRIP.numPixels() ):
            STRIP.setPixelColor(t, Color(0,0,0))
        STRIP.show()
        time.sleep(wait_ms/1000.0)

def runRave():
    """Runs the pulseColor function forever until Master Loop is false"""
    while MASTER_LOOP == True:
        pulseColor(Color(0,255,0))

def theaterChase(color,wait_ms=50):
    """Function used to create the theater chase animation"""
    if MOVIE_LIGHT == True:
       for q in range(3):
           for i in range(0, STRIP.numPixels(), 3):
               STRIP.setPixelColor(i+q, color)
           STRIP.show()
           time.sleep(wait_ms/1000.0)
           for i in range(0, STRIP.numPixels(), 3):
               STRIP.setPixelColor(i+q, 0)
    else:
       for q in range(3):
           for i in range(0, STRIP.numPixels() - MOVIE_LIGHT_RANGE, 3):
               STRIP.setPixelColor(MOVIE_LIGHT_RANGE+i+q, color)
           STRIP.show()
           time.sleep(wait_ms/1000.0)
           for i in range(0, STRIP.numPixels() - MOVIE_LIGHT_RANGE, 3):
               STRIP.setPixelColor(MOVIE_LIGHT_RANGE+i+q, 0)
                    
def theaterChaseGreen(wait_ms=50):
    """Function used to create the theater chase animation"""
    if MOVIE_LIGHT == True:
       for q in range(3):
           for i in range(0, STRIP.numPixels(), 3):
               STRIP.setPixelColor(i+q, Color(0,255,0))
           STRIP.show()
           time.sleep(wait_ms/1000.0)
           for i in range(0, STRIP.numPixels(), 3):
               STRIP.setPixelColor(i+q, 0)
    else:
        for q in range(3):
            for i in range(0, STRIP.numPixels() - MOVIE_LIGHT_RANGE, 3):
                STRIP.setPixelColor(MOVIE_LIGHT_RANGE+i+q, Color(0,255,0))
            STRIP.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, STRIP.numPixels() - MOVIE_LIGHT_RANGE, 3):
                STRIP.setPixelColor(MOVIE_LIGHT_RANGE+i+q, 0)
                    
                    
def specialTheaterChase(wait_ms=50):
    """Function used to create the theater chase animation"""
    if MOVIE_LIGHT == True:
       for q in range(3):
           for i in range(0, STRIP.numPixels(), 3):
               if i < 540:
                  STRIP.setPixelColor(i+q, Color(255,255,255))
               else:
                  STRIP.setPixelColor(i+q, Color(255,0,0))
           STRIP.show()
           time.sleep(wait_ms/1000.0)
           for i in range(0, STRIP.numPixels(), 3):
               STRIP.setPixelColor(i+q, 0)
    else:
        for q in range(3):
            for i in range(0, STRIP.numPixels() - MOVIE_LIGHT_RANGE, 3):
                STRIP.setPixelColor(MOVIE_LIGHT_RANGE+i+q, color)
            STRIP.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, STRIP.numPixels() - MOVIE_LIGHT_RANGE, 3):
                STRIP.setPixelColor(MOVIE_LIGHT_RANGE+i+q, 0)
                    

def colorWipeBeam(color, wait_ms = 1):
    """Lights up all leds with the given color, but does all beams at the same time"""
    if MOVIE_LIGHT == True:
        for q in range(STRIP_LEDS_PER_STRAND):
            for i in range(0, STRIP.numPixels(), STRIP_LEDS_PER_STRAND):
                STRIP.setPixelColor(i+q, color)
            STRIP.show()
            time.sleep(wait_ms/1000.0)
    else:
        for q in range(STRIP_LEDS_PER_STRAND):
            for i in range(0, STRIP.numPixels(), STRIP_LEDS_PER_STRAND):
                STRIP.setPixelColor(MOVIE_LIGHT_RANGE+i+q, color)
            STRIP.show()
            time.sleep(wait_ms/1000.0)

def staticColor(red,green,blue):
    """Sets all the leds to a given color with the red, green, blue values provided"""
    if MOVIE_LIGHT == True:
        for i in range(STRIP.numPixels()):
            STRIP.setPixelColor(i, Color(red,green,blue))
        STRIP.show()
    else:
        for i in range(MOVIE_LIGHT_RANGE,STRIP.numPixels()):
            STRIP.setPixelColor(i, Color(red,green,blue))
        STRIP.show()

def runColorCycle():
    """Runs a random animation and color forever untill Master Loop is false"""
    while MASTER_LOOP:
        type = random.randint(0,1)
        if type == 0:
            colorWipeBeam(Color(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        if type == 1:
            theaterChase(Color(random.randint(0,255), random.randint(0,255),random.randint(0,255)))
        #colorWipeBeam(Color(255,0,0))
        #colorWipeBeam(Color(0,255,0))
        #colorWipeBeam(Color(0,0,255))
        #colorWipeBeam(Color(114,228,52))
        #colorWipeBeam(Color(52,52,52))
        #colorWipeBeam(Color(255,0,128))
        

def startUp():
    """Function called when the web server first starts to show it is working"""
    colorWipeBeam(Color(255,0,0))
    colorWipeBeam(Color(0,255,0))
    colorWipeBeam(Color(0,0,255))
    colorWipeBeam(Color(0,0,0))
    pulseColor(Color(0,255,0))
    pulseColor(Color(0,255,0))
    pulseColor(Color(0,255,0))
    pulseColor(Color(0,255,0))


def turnOffMovie():
    """Turns off all the leds above the projector"""
    for i in range(0, MOVIE_LIGHT_RANGE):
        STRIP.setPixelColor(i, Color(0,0,0))
    STRIP.show()


def turnOff():
    """Sets all leds to 'off' (Black)"""
    colorWipeBeam(Color(0,0,0))


def runTheater():
    """Runs theater chase forever until Master Loop is false"""
    while MASTER_LOOP:
        theaterChase(Color(255,255,255))
        
def runTheaterGreen():
    """Runs theater chase forever until Master Loop is false"""
    while MASTER_LOOP:
        theaterChaseGreen()


def pong():
    """Runs a animation that represents basic pong graphics"""
    for i in range(34):
        STRIP.setPixelColor(i+36, Color(255,255,255))
        STRIP.setPixelColor(1080 + 36 + i, Color(255,255,255))
        STRIP.show()
    for t in range(3):
        STRIP.setPixelColor(162 , Color(255,255,255))
        STRIP.show()
        time.sleep(1)
        STRIP.setPixelColor(162, Color(0,0,0))
        STRIP.show()
        time.sleep(1)
    STRIP.setPixelColor(162, Color (255,255,255))
    STRIP.show()
    while MASTER_LOOP:
        oldLocation = 162
        for q in range(8):
            STRIP.setPixelColor(oldLocation, Color(0,0,0))
            STRIP.setPixelColor(oldLocation + 108, Color(255,255,255))
            oldLocation = oldLocation + 108
            STRIP.show()
            time.sleep(.7)
        for w in range(8):
            STRIP.setPixelColor(oldLocation, Color(0,0,0))
            STRIP.setPixelColor(oldLocation - 108, Color(255,255,255))
            oldLocation = oldLocation - 108
            STRIP.show()
            time.sleep(0.7)
            
            
def runCanadaDayAnimation():
    while MASTER_LOOP:
        specialTheaterChase()
