#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #
# Python: Load up the slots UI in a random position
# Wait for the lever to be pulled
# Do the slots - pick a random outcome and have it happen. 
# play the sounds while this is happening: Thread(play rolling sound), pi does the thing and wait for Thread, then play finished sound 
# Based on the result, Thread(send a code to the arduino and wait), Pi: and play a sound and wait for Thread
# --> Arduino is listening for code, fires all the peripherals
# --> Sends a message back to python when done, goes back to listening
# Once we get the response from the arduino AND the sound is done playing we can do the next thing:
# Either send a command to dispense N coins, followed by wait for done, then reset the screen and send a reset command to the arduino
# fn: Thread(send command and wait), have the pi play sounds

import pygame
from pygame.locals import *
from random import randrange
from sys import argv
from getopt import getopt, GetoptError

##new lucky kitty specific stuff
import serial
from gpiozero import Button

VERSION = "0.1"

# the game###########################
class Game:
    def __init__(self):
        self.wins = None
        self.keys = 1 #wat do, seems like holding down f1 for fn
        self.show = {}
        
        self.screen = screen
        self.xoffsets = [120, 256, 392]#[36, 165, 295]
        self.yoffsets = [46, 174, 302]
        # COMMENT OUT ON OSX FOR TESTING
#         self.handle = Button(4)
        
        self.bsound = pygame.mixer.Sound("data/sounds/CLICK10A.WAV")
        self.oneup = pygame.mixer.Sound("_assets/_sounds/1up16.wav")
        self.cheesy = pygame.mixer.Sound("_assets/_sounds/cheesy16.wav")
        self.coin = pygame.mixer.Sound("_assets/_sounds/coin16.wav")
        self.hth = pygame.mixer.Sound("_assets/_sounds/hth16.wav")
        self.loss = pygame.mixer.Sound("_assets/_sounds/loss16.wav")
        self.nyan = pygame.mixer.Sound("_assets/_sounds/nyan16.wav")
        self.pinchy = pygame.mixer.Sound("_assets/_sounds/pinchy16.wav")
        self.reel = pygame.mixer.Sound("_assets/_sounds/reel16.wav")
        self.rstop = pygame.mixer.Sound("_assets/_sounds/rstop16.wav")
        self.scream = pygame.mixer.Sound("_assets/_sounds/scream16.wav")
        self.jackpot = pygame.mixer.Sound("_assets/_sounds/nyan16.wav")
#         self.background = pygame.image.load("data/img/bg.png")
        
        self.winNyan = b'\x00'
        self.winTentacle = b'\x01'
        self.winCoin = b'\x02'
        self.winFire = b'\x03'
        self.winCheese = b'\x04'
        self.winPinchy = b'\x05'
        self.winJackpot = b'\x06'
        self.cmdLoss = b'\x07'
        self.cmdDone = b'\x09'
        
#         self.rlayer = pygame.image.load("data/img/rlayer.png")
# Maybe change this to just be the one black line across
#         self.windowlayer = pygame.image.load("data/img/windowlayer.png")
        self.imgpaths = ["_assets/_images/png/nyanf.png", "_assets/_images/png/tentf.png", "_assets/_images/png/coinf.png", "_assets/_images/png/firef.png", "_assets/_images/png/cheesef.png", "_assets/_images/png/pinchyf.png", "_assets/_images/png/luckycat.png"]
        self.imgnyan = pygame.image.load(self.imgpaths[0])
        self.imgtent = pygame.image.load(self.imgpaths[1])
        self.imgcoin = pygame.image.load(self.imgpaths[2])
        self.imgfire = pygame.image.load(self.imgpaths[3])
        self.imgcheese = pygame.image.load(self.imgpaths[4])
        self.imgpinchy = pygame.image.load(self.imgpaths[5])
        self.imgjackpot = pygame.image.load(self.imgpaths[6])
        
        self.img = [self.imgnyan, self.imgtent, self.imgcoin, self.imgfire, self.imgcheese, self.imgpinchy, self.imgjackpot]

        # Randomize and update the images without actually doing the roll 
        self.randi()
        self.screen.fill([0, 0, 0])
#         self.screen.blit(self.background, (0, 0))
        self.drawl()
#         self.screen.blit(self.windowlayer, (0, 0))
        pygame.display.update()
        
        # mainloop
        while True:
            # COMMENT OUT ON OSX FOR TESTING
#             if self.handle.is_pressed:
#                 self.playgame()
#                 print("Starting new round!")
#             else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    exit()
                if event.type == pygame.KEYDOWN:
                    self.bsound.play()
                    if event.key == pygame.K_LEFT and self.keys == 1:
                        self.playgame()
                        print("Starting new round!")

    def playgame(self):
        self.randi()
        self.roll(self.img)
        #reused
#         self.screen.blit(self.background, (0, 0))
        self.drawl()
#         self.screen.blit(self.windowlayer, (0, 0))
        #/reused
        pygame.display.update()
        self.winner()

    # Does the actual scrolling thing
    #Todo(mje): Make it so the top and bottom images are partially cut off
    #Todo: Make the images roll slower
    # Make the window border the full size we want it to be,
    # or else draw it manually
    def roll(self, img):
        szam = 0
        self.reel.play(loops=-1)
        
        # toll time
        #Todo: understand what this timing actually is
        rolla = randrange(10, 28)
        rollb = randrange(rolla+1, rolla+5)
        rollc = randrange(rollb+1, rollb+5)
        
        # a column
        rollaf = []
        rollaf.append(img[self.imgpaths.index(self.show[0])-1])
        rollaf.append(img[self.imgpaths.index(self.show[1])-1])
        rollaf.append(img[self.imgpaths.index(self.show[2])-1])
        while szam <= rolla-3:
            rollaf.append(img[randrange(0, 7)])
            szam = szam + 1
        rollaf.append(img[self.imgpaths.index(self.showold[0])-1])
        rollaf.append(img[self.imgpaths.index(self.showold[1])-1])
        rollaf.append(img[self.imgpaths.index(self.showold[2])-1])
        
            
        szam = 0
        
        # b column
        rollbf = []
        rollbf.append(img[self.imgpaths.index(self.show[3])-1])
        rollbf.append(img[self.imgpaths.index(self.show[4])-1])
        rollbf.append(img[self.imgpaths.index(self.show[5])-1])
        while szam <= rollb-3:
            rollbf.append(img[randrange(0, 7)])
            szam = szam +1
        rollbf.append(img[self.imgpaths.index(self.showold[3])-1])
        rollbf.append(img[self.imgpaths.index(self.showold[4])-1])
        rollbf.append(img[self.imgpaths.index(self.showold[5])-1])
            
        szam = 0
        
        # c column
        rollcf = []
        rollcf.append(img[self.imgpaths.index(self.show[6])-1])
        rollcf.append(img[self.imgpaths.index(self.show[7])-1])
        rollcf.append(img[self.imgpaths.index(self.show[8])-1])
        while szam <= rollc-3:
            rollcf.append(img[randrange(0, 7)])
            szam = szam +1

        rollcf.append(img[self.imgpaths.index(self.showold[6])-1])
        rollcf.append(img[self.imgpaths.index(self.showold[7])-1])
        rollcf.append(img[self.imgpaths.index(self.showold[8])-1])
        
        szama = len(rollaf)-1
        szamb = len(rollbf)-1
        szamc = len(rollcf)-1
        
        #TODO: this is probably about where we need to do the slowdown
        while szamc > 2:
            self.screen.fill([0, 0, 0])
#             self.screen.blit(self.background, (0, 0))
            
            if szama > 2:
                self.screen.blit(rollaf[len(rollaf)-3], (self.xoffsets[0], self.yoffsets[0]))
                self.screen.blit(rollaf[len(rollaf)-2], (self.xoffsets[0], self.yoffsets[1]))
                self.screen.blit(rollaf[len(rollaf)-1], (self.xoffsets[0], self.yoffsets[2]))
                szama = szama - 1
                del(rollaf[len(rollaf)-1])
            else:
                self.screen.blit(rollaf[len(rollaf)-3], (self.xoffsets[0], self.yoffsets[0]))
                self.screen.blit(rollaf[len(rollaf)-2], (self.xoffsets[0], self.yoffsets[1]))
                self.screen.blit(rollaf[len(rollaf)-1], (self.xoffsets[0], self.yoffsets[2]))
                
            if szamb > 2:
                self.screen.blit(rollbf[len(rollbf)-3], (self.xoffsets[1], self.yoffsets[0]))
                self.screen.blit(rollbf[len(rollbf)-2], (self.xoffsets[1], self.yoffsets[1]))
                self.screen.blit(rollbf[len(rollbf)-1], (self.xoffsets[1], self.yoffsets[2]))
                szamb = szamb - 1
                del(rollbf[len(rollbf)-1])
            else:
                self.screen.blit(rollbf[len(rollbf)-3], (self.xoffsets[1], self.yoffsets[0]))
                self.screen.blit(rollbf[len(rollbf)-2], (self.xoffsets[1], self.yoffsets[1]))
                self.screen.blit(rollbf[len(rollbf)-1], (self.xoffsets[1], self.yoffsets[2]))
                
            if szamc > 2:
                self.screen.blit(rollcf[len(rollcf)-3], (self.xoffsets[2], self.yoffsets[0]))
                self.screen.blit(rollcf[len(rollcf)-2], (self.xoffsets[2], self.yoffsets[1]))
                self.screen.blit(rollcf[len(rollcf)-1], (self.xoffsets[2], self.yoffsets[2]))
                szamc = szamc - 1
                del(rollcf[len(rollcf)-1])
            else:
                self.screen.blit(rollcf[len(rollcf)-3], (self.xoffsets[2], self.yoffsets[0]))
                self.screen.blit(rollcf[len(rollcf)-2], (self.xoffsets[2], self.yoffsets[1]))
                self.screen.blit(rollcf[len(rollcf)-1], (self.xoffsets[2], self.yoffsets[2]))
            
#             self.screen.blit(self.windowlayer, (0, 0))
            pygame.display.update()
            rollc = rollc - 1
        self.reel.stop()
        self.rstop.play()
    
    def drawl(self):
        #blit(image, (x,y to load it in)
        self.screen.blit(pygame.image.load(self.show[0]), (self.xoffsets[0], self.yoffsets[0]))
        self.screen.blit(pygame.image.load(self.show[1]), (self.xoffsets[0], self.yoffsets[1]))
        self.screen.blit(pygame.image.load(self.show[2]), (self.xoffsets[0], self.yoffsets[2]))
        self.screen.blit(pygame.image.load(self.show[3]), (self.xoffsets[1], self.yoffsets[0]))
        self.screen.blit(pygame.image.load(self.show[4]), (self.xoffsets[1], self.yoffsets[1]))
        self.screen.blit(pygame.image.load(self.show[5]), (self.xoffsets[1], self.yoffsets[2]))
        self.screen.blit(pygame.image.load(self.show[6]), (self.xoffsets[2], self.yoffsets[0]))
        self.screen.blit(pygame.image.load(self.show[7]), (self.xoffsets[2], self.yoffsets[1]))
        self.screen.blit(pygame.image.load(self.show[8]), (self.xoffsets[2], self.yoffsets[2]))

    # random images
    #todo(mje): Look at this logic more. is this just randomizing all images at all times?
    # Then comparing? May need a better approach for probabilities
    def randi(self):
        if len(self.show) > 1:
            self.showold = self.show
        else:
            self.showold = []
            
        self.show = {}    
            
        ##todo(mje): do a single roll here and set self.show[1-4-7] to that outcome if its a win? stats are hard
        rand = randrange(1, 100)
        outcome = None
        if 1 <= rand <= 10:
            outcome = self.imgpaths[0]
        elif 11 <= rand <= 20:
            outcome = self.imgpaths[1]
        elif 21 <= rand <= 30:
            outcome = self.imgpaths[2]
        elif 31 <= rand <= 40:
            outcome = self.imgpaths[3]
        elif 41 <= rand <= 50:
            outcome = self.imgpaths[4]
        elif 51 <= rand <= 60:
            outcome = self.imgpaths[5]
        elif 61 <= rand <= 70:
            outcome = self.imgpaths[6]
        
        #todo(mje): Okay so this is where we decide what img to show and what outcome we get with likelihoods
        #DEBUG: Uncomment this line and comment the rest to test a specific outcome
#         outcome = self.imgpaths[3]
        for i in range(9):
            idx = randrange(7)
            self.show[i] = self.imgpaths[idx]
            
            if outcome is None and i == 4 and idx == self.show[1]:
                newIdx = idx % 6
                self.show[i] = self.imgpaths[newIdx]
            elif outcome is not None and i in {1, 4, 7}:
                self.show[i] = outcome
   
    # Checks if any of your lines have won
    def check(self):
        if self.show[1] == self.show[4] == self.show[7]:
            pygame.draw.line(self.screen, [246, 226, 0], (self.xoffsets[0], 239), (self.xoffsets[2] + 128, 239), 8)
            self.wins = self.show[1]
        else:
            self.wins = None
   
    def winner(self):
        while pygame.mixer.get_busy():
            pass
        
        self.check()
        pygame.display.update()
        
        print("WIN STATE:")
        print(self.wins)
            
        #Todo: Flesh out the win code to match the arduino (send-receive-send-receive stuff)
#         if self.wins is not None:
#             index = self.imgpaths.index(self.wins)
#             if index == 0:
#                 self.nyan.play()
#                 self.sendandwait(self.winNyan)
#                 self.sendandwait(self.cmdDone) #maybe a reset instead, no need to wait?
#             elif index == 1:
#                 self.scream.play()
#                 self.sendandwait(self.winTentacle)
#                 self.sendandwait(self.cmdDone)
#             elif index == 2:
#                 self.coin.play()
#                 self.sendandwait(self.winCoin)
#                 self.oneup.play()
#                 
#                 while pygame.mixer.get_busy():
#                     pass
#                 
#                 self.sendandwait(self.cmdDone)
#             elif index == 3:
#                 self.hth.play()
#                 self.sendandwait(self.winFire)
#                 self.sendandwait(self.cmdDone)
#             elif index == 4:
#                 self.cheesy.play()
#                 self.sendandwait(self.winCheese)
#                 self.sendandwait(self.cmdDone)
#             elif index == 5:
#                 self.pinchy.play()
#                 self.sendandwait(self.winPinchy)
#                 self.sendandwait(self.cmdDone)
#             elif index == 6:
#                 self.jackpot.play()
#                 # Do all the lights and fire
#                 self.sendandwait(self.winJackpot) 
#                 
#                 ser.write(self.cmdDone)
#                 # play the coin sound and dispense a coin 5 times
#                 for _ in range(5):
#                     self.coin.play()
#                     while pygame.mixer.get_busy():
#                         pass
# 
#                 self.oneup.play()
#                 while pygame.mixer.get_busy():
#                     pass
# 
#                 self.sendandwait(self.cmdDone)
#         else:
#             self.loss.play()
#             self.sendandwait(self.cmdLoss)
#             self.sendandwait(self.cmdDone)
            
        print("Finished doing WINstate!")
    
    # Sends a command and waits for both thread and play to stop, eg. #b"Hello from Raspiberry Pi!\n"
    def sendandwait(self, cmd):
        ser.write(cmd)
        #TODO(mje): Might need to make sure we're flushing our buffer whenever we send something here
        while pygame.mixer.get_busy():
            pass
        
        while not (ser.in_waiting > 0):
            pass
            
        byte = ser.read(1);
        if not byte == self.cmdDone:
            print("Got an unexpected command")
        print("Arduino finished!")
        print(byte)
        
def help():
    print("Lucky Kitty help:")
    print("Options:")
    print("-h, --help        display this help message")
    print("-v, --version     display game version")
    print("-f, --fullscreen  run in fullscreen mode")
    print("-p, --pi          run in raspberry pi mode")
    print("Contact: everson.mike@gmail.com")

if __name__ == "__main__":
    fullscreen = False
    pi = False
    
    try:
        long = ["help", "version"]
        opts = getopt(argv[1:], "hv", long)[0]
    except GetoptError:
        help()
        exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            exit()
        if opt in ("-v", "--version"):
            print("Lucky Kitty - version: "+ VERSION)
            exit()
        if opt in ("-f", "--fullscreen"):
            fullscreen = True
        if opt in ("-p", "--pi"):
            pi = True
         
    # Setup serial communication
    #TODO(MJE): How will this work when we boot up the pi cold, will we need to wait?
    # COMMENT OUT ON OSX FOR TESTING
#     if pi
#     ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
#     else        
#         ser = serial.Serial('/dev/cu.usbserial-A603GDYX', 9600, timeout=5)
#     ser.flush()
            
    # pygame init, set display
    pygame.init()
    
    if not fullscreen:
        screen = pygame.display.set_mode([640, 480], 0, 24)
    else:
        screen = pygame.display.set_mode([640, 480], pygame.FULLSCREEN)

    pygame.display.set_caption("Lucky Kitty MkII")
    pygame.mouse.set_visible(False)
    
    plc = Game() 
    pygame.display.update()
