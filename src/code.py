import time
import board
import displayio
import busio as io
import pwmio
from digitalio import Direction, DigitalInOut, Pull

from random import seed
from random import randint

import neopixel
import adafruit_framebuf
import adafruit_ssd1306
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect


# Set Pins
PIEZO_PIN = board.D10

# Define a list of tones/music notes to play.
TONE_FREQ = [
    330, # E4
    220, # A3
    139, # C3#
    165  # E3
    ]

ERROR_TONE_FREQ =[
    330,  # E4
    294,  # D4
    262,  # C4
    131,  # C3
    110   # A2
    ]
    
TONE_FREQ_ALT = [
    262, # C4
    294, # D4
    330, # E4
    349, # F4
    392, # G4
    440, # A4
    494, # B4
    523  # C5
    ]

# Set some default values
screenMinX = 2
screenMinY = 2
screenLineHeight = 10

notesPerLevel = 4
currentLevel = 1

RED = (255, 0, 0, 0)
YELLOW = (255, 150, 0, 0)
GREEN = (0, 255, 0, 0)
CYAN = (0, 255, 255, 0)
BLUE = (0, 0, 255, 0)
PURPLE = (180, 0, 255, 0)
BLACK = (0, 0, 0, 0)


# Board NEOPIXEL Init
boardPixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.15)

# Board Button Init
boardButton = DigitalInOut(board.BUTTON)
boardButton.switch_to_input(pull=Pull.UP)

# Game Screen Init
gameI2c = io.I2C(scl=board.RX, sda=board.TX, frequency=1000000) # Fastest frequency
gameOled = adafruit_ssd1306.SSD1306_I2C(128, 32, gameI2c)
gameOled.rotation = 1 # (Portait Mode)

# Game Buzzer
gameBuzzer = pwmio.PWMOut(PIEZO_PIN, duty_cycle=0, frequency=440, variable_frequency=True)

# Game Buttons
gameButton = DigitalInOut(board.MOSI)
gameButton.switch_to_input(pull=Pull.UP)

# Game Pad Tones
simonPadTones = [
    TONE_FREQ[0], TONE_FREQ[1], TONE_FREQ[2], TONE_FREQ[3]
    ]

# Game Pad Buttons
simonPadButtons = [
    DigitalInOut(board.D6), DigitalInOut(board.D7), DigitalInOut(board.D8), DigitalInOut(board.D9)
    ]
for simonPadButton in simonPadButtons: # Init Pad Buttons
    simonPadButton.switch_to_input(pull=Pull.UP)

# Game Pad LEDs
simonPadLeds = [
    DigitalInOut(board.D2), DigitalInOut(board.D3), DigitalInOut(board.D4), DigitalInOut(board.D5)
    ]
for simonPadLed in simonPadLeds: # Init Pad LEDs
    simonPadLed.direction = Direction.OUTPUT
    simonPadLed.value = False

# ---

def testBit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)

# setBit() returns an integer with the bit at 'offset' set to 1.
def setBit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)

# clearBit() returns an integer with the bit at 'offset' cleared.
def clearBit(int_type, offset):
    mask = ~(1 << offset)
    return(int_type & mask)

# toggleBit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.
def toggleBit(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)

# ---

def playTone(frequency, volume=0xEFFF):
    global gameBuzzer

    gameBuzzer.frequency = frequency
    gameBuzzer.duty_cycle = volume

def stopTone():
    global gameBuzzer

    gameBuzzer.duty_cycle = 0

def playPlayList(playlist):
    global simonPadTones

    for idx in playlist:
        padLedOn(idx)
        playTone(simonPadTones[idx])
        time.sleep(0.25)
        padLedOff(idx)
        stopTone()
        time.sleep(0.125)

def playSelection(padIdx):
    global simonPadTones

    for i in range(1, 3):
        playTone(simonPadTones[padIdx])
        padLedOn(padIdx)
        time.sleep(0.1)
        stopTone()
        padLedOff(padIdx)
        time.sleep(0.05)

def playRamp():
    global simonPadTones

    for tone in simonPadTones:
        playTone(tone)
        time.sleep(0.02)
        stopTone()
        time.sleep(0.01)

def playFullRamp():
    global TONE_FREQ

    for tone in TONE_FREQ:
        playTone(tone)
        time.sleep(0.02)
        stopTone()
        time.sleep(0.01)

def playErrorRamp():
    global ERROR_TONE_FREQ

    for tone in ERROR_TONE_FREQ:
        playTone(tone)
        time.sleep(0.02)
        stopTone()
        time.sleep(0.01)

# ---

def padLedOn(idx):
    global simonPadLeds

    simonPadLeds[idx].value = True

def padLedOff(idx):
    global simonPadLeds

    simonPadLeds[idx].value = False

# ---

def stopPad(idx):
    simonPadLeds[idx].value = False


def pixelGood():
    pixelOn = True
    boardPixel.fill(PURPLE)

def pixelNotice():
    pixelOn = True
    boardPixel.fill(CYAN)

def pixelBad():
    pixelOn = True
    boardPixel.fill(RED)

def pixelOff():
    pixelOn = False
    boardPixel.fill(BLACK)

def getSelectedPad():
    global simonPadButtons

    for idx, padButton in enumerate(simonPadButtons):
        if padButton.value == False:
            return idx

    return False

# ---

#def convertStateToIdxList(state):

def updatePadStates():
    global buttonStates
    
    for idx, padButton in enumerate(simonPadButtons):
        if padButton.value == False:
            buttonStates = setBit(buttonStates, idx)
        else:
            buttonStates = clearBit(buttonStates, idx)
    
def processPlayStates(states):
    global simonPadButtons
    global simonPadTones

    count = 0
    for idx, padButton in enumerate(simonPadButtons):
        if testBit(states, idx) > 0:
            count = count + 1
            playTone(simonPadTones[idx])
            padLedOn(idx)
            renderButtonOnScreen(idx)
        else:
            padLedOff(idx)
            renderButtonOffScreen(idx)

    if states == 0 or count > 1: # STOP ALL TONES
        stopTone()
        
    if count > 1:
        raise RuntimeError("Multiple pads pressed.")

# ---

def renderBlankScreen():
    global gameOled

    gameOled.fill(0)
    gameOled.show()

def renderSelectScreen():
    global gameOled
    global screenMinX
    global screenMinY
    global screenLineHeight

    print("Pick a skill level")

    gameOled.fill(1)
    gameOled.text('Pick', screenMinX, screenMinY + (1 * screenLineHeight), 0)
    gameOled.text('skill', screenMinX, screenMinY + (2 * screenLineHeight), 0)
    gameOled.text('level', screenMinX, screenMinY + (3 * screenLineHeight), 0)

    gameOled.text(' G:1 ', screenMinX, screenMinY + (5 * screenLineHeight), 0)
    gameOled.text(' R:2 ', screenMinX, screenMinY + (6 * screenLineHeight), 0)
    gameOled.text(' Y:3 ', screenMinX, screenMinY + (7 * screenLineHeight), 0)
    gameOled.text(' B:4 ', screenMinX, screenMinY + (8 * screenLineHeight), 0)
    gameOled.show()

def renderPlayScreen():
    global gameOled
    global screenMinX
    global screenMinY
    global screenLineHeight

    print("PLAY!")

    gameOled.rect(0, 0, 32, screenLineHeight + 1, 0xFFFFFF, fill=0xFFFFFF)
    gameOled.text('PLAY!', screenMinX, screenMinY + (0 * screenLineHeight), 0)
    gameOled.show()

def renderGameOverScreen():
    global gameOled
    global screenMinX
    global screenMinY
    global screenLineHeight

    print("Game Over!")

    gameOled.rect(0, 0, 32, screenLineHeight + 1, 0xFFFFFF, fill=0xFFFFFF)
    gameOled.text('OVER!', screenMinX, screenMinY + (0 * screenLineHeight), 0)
    gameOled.show()

def renderButtonOffScreen(idx):
    if (idx == 0): # GREEN
        gameOled.rect(0, 13, 15, 15, 0x000000, fill=0xFFFFFF)
    elif (idx == 1): # RED
        gameOled.rect(17, 13, 32, 15, 0x000000, fill=0xFFFFFF)
    elif (idx == 2): # YELLOW
        gameOled.rect(0, 30, 15, 15, 0x000000, fill=0xFFFFFF)
    elif (idx == 3): # BLUE
        gameOled.rect(17, 30, 32, 15, 0x000000, fill=0xFFFFFF)

    gameOled.show()

def renderButtonOnScreen(idx):
    if (idx == 0): # GREEN
        gameOled.rect(0, 13, 15, 15, 0xFFFFFF, fill=0xFFFFFF)
    elif (idx == 1): # RED
        gameOled.rect(17, 13, 32, 15, 0xFFFFFF, fill=0xFFFFFF)
    elif (idx == 2): # YELLOW
        gameOled.rect(0, 30, 15, 15, 0xFFFFFF, fill=0xFFFFFF)
    elif (idx == 3): # BLUE
        gameOled.rect(17, 30, 32, 15, 0xFFFFFF, fill=0xFFFFFF)

    gameOled.show()

def renderLevelPointsScreen():
    global gameOled
    global screenMinX
    global screenMinY
    global screenLineHeight

    global gameLevel
    global gameScore

    #print("Level: {} | Score: {}".format(gameLevel, gameScore))

    gameOled.rotation = 0 # (Landscape Mode)
    gameOled.text('Lvl: {}'.format(gameLevel), screenMinX, screenMinY + (0 * screenLineHeight), 1)
    gameOled.text('Pts: {}'.format(gameScore), screenMinX, screenMinY + (1 * screenLineHeight), 1)
    gameOled.show()
    gameOled.rotation = 1 # (Portait Mode)
    
# ---
            
def getUserSkillLevel():
    global simonPadTones

    selectedPad = True
    while selectedPad is True:
        padIdx = getSelectedPad()
        if padIdx is not False:
            selectedPad = padIdx + 1
            playSelection(padIdx)
            
    return selectedPad

def playGameLevel(lvl = 1):
    global prevButtonStates
    global buttonStates
    global boardButton
    global gameButton
    global gameLevel
    
    gameLevel = lvl
    
    levelPlayList = buildLevelPlayList(gameLevel)
    print(levelPlayList)
 
    endGame = False
    while not endGame:
        updatePadStates()
        
        if prevButtonStates != buttonStates:
            prevButtonStates = buttonStates
            print("Pad State: {}".format(buttonStates))

            processPlayStates(buttonStates)

        if not boardButton.value or not gameButton.value:
            if not boardButton.value:
                pixelBad()
                playPlayList(levelPlayList)
                raise RuntimeError("Forced test error.")
            else:
                pixelOff()
                endGame = True
        
        renderLevelPointsScreen()

def finishedGameLevel(message):
    global prevButtonStates
    global buttonStates
    global boardButton
    global gameButton
    
    print(message)
    
    renderGameOverScreen()
    playErrorRamp()
    
    time.sleep(0.5)
    
    endGame = False
    while not endGame:
            
        if not boardButton.value or not gameButton.value:
            pixelOff()
            endGame = True
        
def buildLevelPlayList(level):
    seed(level)
    
    playlist = []
    for _ in range(notesPerLevel * level * skillLevel):
        playlist.append(randint(0, 3))

    playFullRamp()
    return playlist

# ---
# ---

while True:
    pixelOn = False
    
    gameLevel = 1
    gameScore = 0
    
    buttonStates = 0
    prevButtonStates = 0
    
    processPlayStates(buttonStates)

    pixelNotice()
    playRamp()
    renderSelectScreen()
    skillLevel = getUserSkillLevel()
    renderBlankScreen()
    print("Skill Level: {}".format(skillLevel))

    pixelGood()
    renderPlayScreen()
    
    for idx in range(0, 4):
        renderButtonOffScreen(idx)

    try:
        playGameLevel()
    except Exception as err:
        finishedGameLevel(err)
 