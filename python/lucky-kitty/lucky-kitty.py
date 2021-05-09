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
import sys
from sys import argv
from getopt import getopt, GetoptError
import time
import os

##new lucky kitty specific stuff
import serial
import time

# if __name__ == '__main__':
#     ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
#     ser.flush()
    
#     while True:
#         if ser.in_waiting > 0:
#             line = ser.readline().decode('utf-8').rstrip()
#             print(line)

#     while True:
#         ser.write(b"Hello from Raspiberry Pi!\n")
#         line = ser.readline().decode('utf-8').rstrip()
#         print(line)
#         time.sleep(1)
##End lucky kitty serial stuff

VERSION = "0.1"

# the game###########################
class Game:
    def __init__(self):
        self.wins = None
        self.keys = 1 #wat do, seems like holding down f1 for fn
        self.show = []
        
        self.screen = screen
        
        self.bsound = pygame.mixer.Sound("data/sounds/CLICK10A.WAV")
        self.rasound = pygame.mixer.Sound("data/sounds/film_projector.wav")
        self.rbsound = pygame.mixer.Sound("data/sounds/film_projector.wav")
        self.rcsound = pygame.mixer.Sound("data/sounds/film_projector.wav")
#         self.bgsound = pygame.mixer.Sound("data/sounds/background001.wav")
        self.beepsound = pygame.mixer.Sound("data/sounds/beep.wav")
        self.background = pygame.image.load("data/img/bg.png")
#         self.rlayer = pygame.image.load("data/img/rlayer.png")
# Maybe change this to just be the one black line across
        self.windowlayer = pygame.image.load("data/img/windowlayer.png")
        self.imgpaths = ["_assets/_images/png/cheesef.png", "_assets/_images/png/coinf.png", "_assets/_images/png/firef.png", "_assets/_images/png/nyanf.png", "_assets/_images/png/pinchyf.png", "_assets/_images/png/sethf.png", "_assets/_images/png/tentf.png", "data/img/8.png"]
        self.imgone = pygame.image.load(self.imgpaths[0])
        self.imgtwo = pygame.image.load(self.imgpaths[1])
        self.imgthree = pygame.image.load(self.imgpaths[2])
        self.imgfour = pygame.image.load(self.imgpaths[3])
        self.imgfive = pygame.image.load(self.imgpaths[4])
        self.imgsix = pygame.image.load(self.imgpaths[5])
        self.imgseven = pygame.image.load(self.imgpaths[6])
        self.imgeight = pygame.image.load(self.imgpaths[7])
        
        img = []
        img.append(self.imgone)
        img.append(self.imgtwo)
        img.append(self.imgthree)
        img.append(self.imgfour)
        img.append(self.imgfive)
        img.append(self.imgsix)
        img.append(self.imgseven)
        img.append(self.imgeight)
        
        # Randomize and update the images without actually doing the roll 
        self.randi()
        self.drawl()
        
#         self.bgsound.play(loops=-1)
        
        # mainloop
        while True:
            self.screen.fill([0, 0, 0])
#             self.screen.blit(self.background, (0, 0))
            ##todo(mje): OR lever has been pulled

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                    
                if event.type == pygame.KEYDOWN:
                    self.bsound.play()
                    if event.key == pygame.K_LEFT and self.keys == 1:
                        self.randi()
                        self.check()
                        self.roll(img)
                        self.screen.blit(self.background, (0, 0))
                        self.drawl()
                        self.winner()
                        
                    if event.key == pygame.K_F1:
                        if self.keys == 1:
                            self.keys = 0
                            self.menu = "h"
                        elif self.keys == 0:
                            self.keys = 1
                            self.menu = "n"
                            
                    if event.key == pygame.K_RETURN:
                        self.keys = 0
                        self.menu = "e"
                
            self.drawl()
            self.check()
            self.wins = None#[0, 0, 0, 0, 0]
            
#             if self.credit == 0 and self.bet == 0:
#                 font = pygame.font.Font("data/LiberationSans-Regular.ttf", 55)
#                 text_surface = font.render("Game Over", True, [255, 0, 0])
#                 self.screen.blit(text_surface, (70, 190))
            
#             self.screen.blit(self.rlayer, (37, 48))
            self.screen.blit(self.windowlayer, (0, 0))
            
            if self.keys == 0 and self.menu == "h":
                self.helpmenu()
            if self.keys == 0 and self.menu == "e":
                self.endthegame(scr)
            
            pygame.display.update()
    
    # Does the actual scrolling thing?
    #Todo(mje): Make it so the top and bottom images are partially cut off
    # Make the window border the full size we want it to be,
    # or else draw it manually
    def roll(self, img):
        szam = 0
        
        
        # toll time
        # TODO: is this how long we scroll for?
        rolla = randrange(5, 14)
        rollb = randrange(rolla+1, rolla+5)
        rollc = randrange(rollb+1, rollb+5)
        
        # a column
        rollaf = []
        rollaf.append(img[self.imgpaths.index(self.show[0])-1])
        rollaf.append(img[self.imgpaths.index(self.show[1])-1])
        rollaf.append(img[self.imgpaths.index(self.show[2])-1])
        while szam <= rolla-3:
            rollaf.append(img[randrange(0, 8)])
            szam = szam + 1
        self.rasound.play()
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
            rollbf.append(img[randrange(0, 8)])
            szam = szam +1
        self.rbsound.play()
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
            rollcf.append(img[randrange(0, 8)])
            szam = szam +1
        self.rcsound.play()
        rollcf.append(img[self.imgpaths.index(self.showold[6])-1])
        rollcf.append(img[self.imgpaths.index(self.showold[7])-1])
        rollcf.append(img[self.imgpaths.index(self.showold[8])-1])
        
        szama = len(rollaf)-1
        szamb = len(rollbf)-1
        szamc = len(rollcf)-1
        
        while szamc > 2:
            self.screen.fill([0, 0, 0])
            self.screen.blit(self.background, (0, 0))
            
            if szama > 2:
                self.screen.blit(rollaf[len(rollaf)-3], (36, 46))
                self.screen.blit(rollaf[len(rollaf)-2], (36, 174))
                self.screen.blit(rollaf[len(rollaf)-1], (36, 302))
                szama = szama - 1
                del(rollaf[len(rollaf)-1])
            else:
                self.screen.blit(rollaf[len(rollaf)-3], (36, 46))
                self.screen.blit(rollaf[len(rollaf)-2], (36, 174))
                self.screen.blit(rollaf[len(rollaf)-1], (36, 302))
                self.rasound.stop()
                
            if szamb > 2:
                self.screen.blit(rollbf[len(rollbf)-3], (165, 46))
                self.screen.blit(rollbf[len(rollbf)-2], (165, 174))
                self.screen.blit(rollbf[len(rollbf)-1], (165, 302))
                szamb = szamb - 1
                del(rollbf[len(rollbf)-1])
            else:
                self.screen.blit(rollbf[len(rollbf)-3], (165, 46))
                self.screen.blit(rollbf[len(rollbf)-2], (165, 174))
                self.screen.blit(rollbf[len(rollbf)-1], (165, 302))
                self.rbsound.stop()
                
            if szamc > 2:
                self.screen.blit(rollcf[len(rollcf)-3], (295, 46))
                self.screen.blit(rollcf[len(rollcf)-2], (295, 174))
                self.screen.blit(rollcf[len(rollcf)-1], (295, 302))
                szamc = szamc - 1
                del(rollcf[len(rollcf)-1])
            else:
                self.screen.blit(rollcf[len(rollcf)-3], (295, 46))
                self.screen.blit(rollcf[len(rollcf)-2], (295, 174))
                self.screen.blit(rollcf[len(rollcf)-1], (295, 302))
            
            self.screen.blit(self.windowlayer, (0, 0))
            pygame.display.update()
            rollc = rollc - 1
        self.rcsound.stop()
    
    def drawl(self):
        self.screen.blit(pygame.image.load(self.show[0]), (36, 46))
        self.screen.blit(pygame.image.load(self.show[1]), (36, 174))
        self.screen.blit(pygame.image.load(self.show[2]), (36, 302))
        self.screen.blit(pygame.image.load(self.show[3]), (165, 46))
        self.screen.blit(pygame.image.load(self.show[4]), (165, 174))
        self.screen.blit(pygame.image.load(self.show[5]), (165, 302))
        self.screen.blit(pygame.image.load(self.show[6]), (295, 46))
        self.screen.blit(pygame.image.load(self.show[7]), (295, 174))
        self.screen.blit(pygame.image.load(self.show[8]), (295, 302))

    # random images
    #todo(mje): Look at this logic more. is this just randomizing all images at all times?
    # Then comparing? May need a better approach for probabilities
    def randi(self):
        self.showold = []
        if len(self.show) > 1:
            self.showold = self.show
        else:
            self.showold = ["data/img/8.png", "data/img/8.png", "data/img/8.png", "data/img/8.png", "data/img/8.png", "data/img/8.png", "data/img/8.png", "data/img/8.png", "data/img/8.png"]
        ran = {}
        ran[0] = randrange(1, 335)
        ran[1] = randrange(1, 335)
        ran[2] = randrange(1, 335)
        ran[3] = randrange(1, 335)
        ran[4] = randrange(1, 335)
        ran[5] = randrange(1, 335)
        ran[6] = randrange(1, 335)
        ran[7] = randrange(1, 335)
        ran[8] = randrange(1, 335)
        self.show = []
        #todo(mje): Okay so this is where we decide what img to show and what outcome we get with likelihoods
        for n in ran:
            if 1 <= ran[n] <= 5:
                self.show.append(self.imgpaths[7])
            if 6 <= ran[n] <= 15:
                self.show.append(self.imgpaths[6])
            if 16 <= ran[n] <= 30:
                self.show.append(self.imgpaths[5])
            if 31 <= ran[n] <= 50:
                self.show.append(self.imgpaths[4])
            if 51 <= ran[n] <= 120:
                self.show.append(self.imgpaths[3])
            if 121 <= ran[n] <= 180:
                self.show.append(self.imgpaths[2])
            if 181 <= ran[n] <= 253:
                self.show.append(self.imgpaths[1])
            if 254 <= ran[n] <= 334:
                self.show.append(self.imgpaths[0])

    # Checks if any of your lines have won
    def check(self):
        if self.show[1] == self.show[4] == self.show[7]:
            pygame.draw.line(self.screen, [246, 226, 0], (36, 239), (423, 239), 8)
            self.wins = self.show[1]
        else:
            self.wins = None
   
    def winner(self):
        print("WIN STATE:")
        print(self.wins)
        if self.wins is not None:
            self.beepsound.play()
    # dont need
    def endthegame(self, scr):
        scrb = int(scr)
        pygame.draw.line(self.screen, [176, 176, 176], (50, 250), (590, 250), 400)

    #dont need
    def writehs(self, myhsfile):
        writef = open(myhsfile, "w")
        writef.close()
        
# probably dont need
def help():
    print("Lucky Kitty help:")
    print("Options:")
    print("-h, --help        display this help message")
    print("-v, --version     display game version")
    print("Contact: everson.mike@gmail.com")

if __name__ == "__main__":
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
            
    # pygame init, set display
    pygame.init()
    screen = pygame.display.set_mode([640, 480], 0, 24)
    pygame.display.set_caption("Lucky Kitty MkII")
    pygame.mouse.set_visible(False)
    
    plc = Game() #This is how you do a new thing, dont even need the plc
    
    pygame.display.update()
