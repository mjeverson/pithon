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

VERSION = "0.1.2"

# # main menu###########################
# class Menu:
#     def __init__(self):
#         self.screen = screen
#         self.maincolor = [0, 0, 0]
#         self.white = [255, 255, 255]
#         self.bsound = pygame.mixer.Sound("data/sounds/CLICK10A.WAV")
#         self.background = pygame.image.load("data/menubg/menubg.png")
#         self.backgroundadded = pygame.image.load("data/menubg/added.png")
#         self.sav = pygame.image.load("data/menubg/sav.png")
#         self.highscore = (pygame.image.load("data/menubg/highscore.png"))
#         self.menu = ["  New Game  ", "  Settings  ", "  High score  ", "  Exit to Linux "]
#         self.menubg = []
#         self.menubg.append(pygame.image.load("data/menubg/al.png").convert())
#         self.menubg.append(pygame.image.load("data/menubg/ci.png").convert())
#         self.menubg.append(pygame.image.load("data/menubg/he.png").convert())
#         self.menubg.append(pygame.image.load("data/menubg/na.png").convert())
#         self.menubg.append(pygame.image.load("data/menubg/di.png").convert())
#         self.menuall = ""
#         self.selectedmenu = 0
#         self.mid = []
#         # get menu width
#         self.menuid()
#         # all menu in one:
#         self.listmenuall()
#         # mainloop
#         sz = 0
#         szam = 0
#         szamlalo = 0
#         self.showhs = False # show hs in menu
#         while True:
#             for self.event in pygame.event.get():
#                 if self.selectedmenu == 2:
#                     self.showhs = True
#                 else:
#                     self.showhs = False
#                 if self.event.type == pygame.QUIT:
#                     exit()
#                 if self.event.type == pygame.KEYDOWN:
#                     self.bsound.play()
#                     if self.event.key == pygame.K_LEFT:
#                         if self.selectedmenu == 0:
#                             self.selectedmenu = len(self.menu)-1
#                         else:
#                             self.selectedmenu = self.selectedmenu-1
#                     elif self.event.key == pygame.K_RIGHT:
#                         if self.selectedmenu == len(self.menu)-1:
#                             self.selectedmenu = 0
#                         else:
#                             self.selectedmenu = self.selectedmenu+1
#                     elif self.event.key == pygame.K_RETURN:
#                         if self.selectedmenu == 0:
#                             plc = Game()
#                         elif self.selectedmenu == 1:
#                             plc = Settings()
#                         elif self.selectedmenu == 2:
#                             self.selectedmenu = 2 # :)
#                         else:
#                             exit()
#                     if self.event.key == pygame.K_ESCAPE:
#                         exit()
#             # 1st layer: background color
#             self.screen.fill(self.maincolor)
#             self.bg = self.menubg[szam]
#             self.bg.set_alpha(sz)
#             self.screen.blit(self.bg, (0, 0))
#             self.screen.blit(self.backgroundadded, (0, 0))
#             # 2nd layer: menus
#             self.crt_menu()
#             # 3rd layer: transparent image
#             self.screen.blit(self.background, (0, 0))
#             
#             font = pygame.font.Font("data/LiberationSans-Regular.ttf", 15)
#             text_surface = font.render("Balazs Nagy - BFruit - "+VERSION , True, self.white)
#             self.screen.blit(text_surface, (3, 460))
#             
#             if self.showhs == True:
#                 self.screen.blit(self.sav, (0, 60))
#                 self.screen.blit(self.sav, (0, 120))
#                 self.screen.blit(self.highscore, (50, 60))
#                 font=pygame.font.Font("data/LiberationSans-Regular.ttf", 25)
#                 text_surface = font.render(scr, True, self.white)
#                 self.screen.blit(text_surface, (295, 110))
#             
#             szamlalo = szamlalo + 4
#             
#             if szamlalo < 245:
#                 sz = sz + 4
#             if szamlalo > 244:
#                 sz = sz - 4
#                 
#             if szamlalo > 490:
#                 sz = 0
#                 szamlalo = 0
#                 if szam == len(self.menubg)-1:
#                     szam = 0
#                 else:
#                     szam = szam + 1
#             
#             
#             pygame.display.update()
#              
#             
#     def menuid(self):
#         for n in self.menu:
#             font = pygame.font.Font("data/LiberationSans-Regular.ttf", 25)
#             text_surface = font.render(n, True, self.white)
#             self.mid.append(text_surface.get_width())
#             
#     def listmenuall(self):
#         for n in self.menu:
#             self.menuall = self.menuall+n
#             
#     def crt_menu(self):
#         nmb = 0
#         xpos = 0
#         while nmb <= self.selectedmenu:
#             xpos = xpos-self.mid[nmb]
#             nmb = nmb+1
#         xpos = xpos+self.mid[self.selectedmenu]/2
#         # draw menus on screen
#         font = pygame.font.Font("data/LiberationSans-Regular.ttf", 25)
#         text_surface = font.render(self.menuall, True, self.white)
#         self.screen.blit(text_surface, (320+xpos, 15))
# 
# # Settings menu################################
# class Settings:
#     def __init__(self):
#         self.screen = screen
#         self.maincolor = [0, 0, 0]
#         self.white = [255, 255, 255]
#         self.bsound = pygame.mixer.Sound("data/sounds/CLICK10A.WAV")
#         self.background = pygame.image.load("data/menubg/menubg.png")
#         self.backgroundadded = pygame.image.load("data/menubg/added.png")
#         self.sav = pygame.image.load("data/menubg/sav.png")
#         self.menu = ["  Fullscreen  ", "  Back to main  "]
#         self.menubg = []
#         self.menubg.append(pygame.image.load("data/menubg/al.png").convert())
#         self.menubg.append(pygame.image.load("data/menubg/ci.png").convert())
#         self.menubg.append(pygame.image.load("data/menubg/he.png").convert())
#         self.menubg.append(pygame.image.load("data/menubg/na.png").convert())
#         self.menubg.append(pygame.image.load("data/menubg/di.png").convert())
#         self.menuall = ""
#         self.selectedmenu = 0
#         self.mid = []
#         # get menu width
#         self.menuid()
#         # all menu in one:
#         self.listmenuall()
#         # mainloop
#         sz = 0
#         szam = 0
#         szamlalo = 0
#         while True:
#             for self.event in pygame.event.get():
#                 if self.event.type == pygame.QUIT:
#                     exit()
#                 if self.event.type == pygame.KEYDOWN:
#                     self.bsound.play()
#                     if self.event.key == pygame.K_LEFT:
#                         if self.selectedmenu == 0:
#                             self.selectedmenu = len(self.menu)-1
#                         else:
#                             self.selectedmenu = self.selectedmenu-1
#                     elif self.event.key == pygame.K_RIGHT:
#                         if self.selectedmenu == len(self.menu)-1:
#                             self.selectedmenu = 0
#                         else:
#                             self.selectedmenu = self.selectedmenu+1
#                     elif self.event.key == pygame.K_RETURN:
#                         if self.selectedmenu == 0:
#                             pygame.display.toggle_fullscreen()
#                         else:
#                             plc = Menu()
#             # 1st layer: background color
#             self.screen.fill(self.maincolor)
#             self.bg = self.menubg[szam]
#             self.bg.set_alpha(sz)
#             self.screen.blit(self.bg, (0, 0))
#             self.screen.blit(self.backgroundadded, (0, 0))
#             # 2nd layer: menus
#             self.crt_menu()
#             # 3rd layer: transparent image
#             self.screen.blit(self.background, (0, 0))
#             
#             font = pygame.font.Font("data/LiberationSans-Regular.ttf", 15)
#             text_surface = font.render("Balazs Nagy - BFruit - "+VERSION , True, self.white)
#             self.screen.blit(text_surface, (3, 460))
#             
#             szamlalo = szamlalo + 4
#             
#             if szamlalo < 245:
#                 sz = sz + 4
#             if szamlalo > 244:
#                 sz = sz - 4
#                 
#             if szamlalo > 490:
#                 sz = 0
#                 szamlalo = 0
#                 if szam == len(self.menubg)-1:
#                     szam = 0
#                 else:
#                     szam = szam + 1
#             
#             
#             pygame.display.update()
#             
#     def menuid(self):
#         for n in self.menu:
#             font = pygame.font.Font("data/LiberationSans-Regular.ttf", 25)
#             text_surface = font.render(n, True, self.white)
#             self.mid.append(text_surface.get_width())
#             
#     def listmenuall(self):
#         for n in self.menu:
#             self.menuall = self.menuall+n
#             
#     def crt_menu(self):
#         nmb = 0
#         xpos = 0
#         while nmb <= self.selectedmenu:
#             xpos = xpos-self.mid[nmb]
#             nmb = nmb+1
#         xpos = xpos+self.mid[self.selectedmenu]/2
#         # draw menus on screen
#         font = pygame.font.Font("data/LiberationSans-Regular.ttf", 25)
#         text_surface = font.render(self.menuall, True, self.white)
#         self.screen.blit(text_surface, (320+xpos, 15))

# the game###########################
class Game:
    def __init__(self):
        self.mut = 0
        self.wins = [0, 0, 0, 0, 0]
        self.keys = 1
        self.credit = 20
        self.bet = 1
        self.lastwin = 0
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
        
        self.randi()
        # Update the images without actually doing the roll 
        self.drawl()
        
#         self.bgsound.play(loops=-1)
        
        # mainloop
        while True:
            self.screen.fill([0, 0, 0])
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
#                     self.bgsound.stop()
                    exit()
                    
                if event.type == pygame.KEYDOWN:
                    self.bsound.play()
                    if event.key == pygame.K_LEFT and self.keys == 1:
#                         if self.credit > 0:
#                             if self.credit - self.bet < 0:
#                                 self.bet = self.credit
#                             self.credit = self.credit - self.bet
                        self.randi()
                        self.check()
                        self.roll(img)
                        self.screen.blit(self.background, (0, 0))
                        self.drawl()
                        self.winner()
#                         elif self.credit == 0 and self.bet == 0:
#                             self.bgsound.stop()
#                             plc = Menu()
                            
#                     if self.credit > 0:
                        if event.key == pygame.K_UP and self.keys == 1:
                            if self.credit - self.bet - 1 >= 0:
                                self.bet = self.bet + 1
                            else:
                                self.bet = 1
                            if self.bet == 11:
                                self.bet = 1
                            
                    else:
                        self.bet = 0
                            
                            
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
                      
#                     if event.key == pygame.K_ESCAPE and self.keys == 1:
#                         self.bgsound.stop()
#                         plc = Menu()
                            
#             self.draw_side()
            
            if self.mut == 1:
                self.drawl()
                self.check()
                self.wins = [0, 0, 0, 0, 0]
            
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
    def roll(self, img):
        szam = 0
        
        
        # toll time
        # TODO: is this how long we scroll for?
        rolla = randrange(5, 14)
        rollb = randrange(rolla+1, rolla+5)
        rollc = randrange(rollb+1, rollb+5)
        
        # a column
        rollaf = []
        #TODO: Need a way to get img index,
        #so img[img.IndexOf(self.show[0]) - 1]
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
            
#             self.draw_side()
#             self.screen.blit(self.rlayer, (37, 48))
            self.screen.blit(self.windowlayer, (0, 0))
            pygame.display.update()
            rollc = rollc - 1
        self.rcsound.stop()
    
#     def draw_side(self):
#         #animation
#         digifont = pygame.font.Font("data/DIGITAL2.ttf",24)
#         text_surface = digifont.render("88888888888", True, [60, 0, 0])
#         self.screen.blit(text_surface, (470, 50))
#         
#         text_surface = digifont.render("F1 FOR HELP", True, [255, 0, 0])
#         self.screen.blit(text_surface, (470, 50))
#         
#         font = pygame.font.Font("data/LiberationSans-Regular.ttf", 15)
#         text_surface = font.render("Bet:", True, [230, 255, 255])
#         self.screen.blit(text_surface, (500, 185))
#         # multip
#         digifont = pygame.font.Font("data/DIGITAL2.ttf",24)
#         text_surface = digifont.render("88", True, [60, 0, 0])
#         self.screen.blit(text_surface, (500, 210))
#         text_surface = digifont.render(str(self.bet), True, [255, 0, 0])
#         self.screen.blit(text_surface, (500, 210))
#         
#         font = pygame.font.Font("data/LiberationSans-Regular.ttf", 15)
#         text_surface = font.render("Winner Paid:", True, [230, 255, 255])
#         self.screen.blit(text_surface, (500, 255))
#         # last win
#         digifont = pygame.font.Font("data/DIGITAL2.ttf",24)
#         text_surface = digifont.render("888", True, [60, 0, 0])
#         self.screen.blit(text_surface, (500, 280))
#         text_surface = digifont.render(str(self.lastwin), True, [255, 0, 0])
#         self.screen.blit(text_surface, (500, 280))
#         
#         font = pygame.font.Font("data/LiberationSans-Regular.ttf", 15)
#         text_surface = font.render("Credit:", True, [230, 255, 255])
#         self.screen.blit(text_surface, (500, 325))
#         # startsum
#         digifont = pygame.font.Font("data/DIGITAL2.ttf",24)
#         text_surface = digifont.render("888888", True, [60, 0, 0])
#         self.screen.blit(text_surface, (500, 350))
#         text_surface = digifont.render(str(self.credit), True, [255, 0, 0])
#         self.screen.blit(text_surface, (500, 350))
    
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
        self.mut = 1
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
#         if self.show[0] == self.show[3] == self.show[6]:
#             pygame.draw.line(self.screen, [246, 226, 0], (36, 111), (423, 111), 8)
#             self.wins[0] = self.show[0]
        if self.show[1] == self.show[4] == self.show[7]:
            pygame.draw.line(self.screen, [246, 226, 0], (36, 239), (423, 239), 8)
            self.wins[1] = self.show[1]
            #TODO: We need to know WHAT's being shown so we know the winstate
#         if self.show[2] == self.show[5] == self.show[8]:
#             pygame.draw.line(self.screen, [246, 226, 0], (36, 367), (423, 367), 8)
#             self.wins[2] = self.show[2]
#         if self.show[0] == self.show[4] == self.show[8]:
#             pygame.draw.line(self.screen, [246, 226, 0], (37, 47), (422, 433), 8)
#             self.wins[3] = self.show[0]
#         if self.show[2] == self.show[4] == self.show[6]:
#             pygame.draw.line(self.screen, [246, 226, 0], (37, 432), (422, 47), 8)
#             self.wins[4] = self.show[2]
            
    def winner(self):
        self.lastwin = 0
        #tODO:self.wins[1] will be the middle line, with the PATH of the image that won
        # probably wanna make it some ENUM or something
        # Also make sure this gets reset
#         for n in self.wins:
#             winsu = self.bet*int(n)
#             winsum = winsu + self.bet
#             if winsum > self.bet:
# #                 self.credit = self.credit + winsum
# #                 self.lastwin = self.lastwin + winsum
#                 self.beepsound.play()
            
#     def helpmenu(self):
#         pygame.draw.line(self.screen, [176, 176, 176], (50, 250), (590, 250), 400)
#         font = pygame.font.Font("data/LiberationSans-Regular.ttf", 15)
#         text_surface = font.render("How to play:", True, [255, 255, 255])
#         self.screen.blit(text_surface, (60, 60))
#         text_surface = font.render("New spin: left arrow", True, [255, 255, 255])
#         self.screen.blit(text_surface, (60, 80))
#         text_surface = font.render("Raise bet: arrow up", True, [255, 255, 255])
#         self.screen.blit(text_surface, (60, 100))
#         text_surface = font.render("To end game to high score press Enter", True, [255, 255, 255])
#         self.screen.blit(text_surface, (60, 120))
#         text_surface = font.render("To close this as game over help press F1", True, [255, 255, 255])
#         self.screen.blit(text_surface, (60, 160))
        
    def endthegame(self, scr):
        scrb = int(scr)
        pygame.draw.line(self.screen, [176, 176, 176], (50, 250), (590, 250), 400)
#         if self.credit > scrb:
#             font = pygame.font.Font("data/LiberationSans-Regular.ttf", 15)
#             text_surface = font.render("You have a new high score!!!", True, [255, 255, 255])
#             self.screen.blit(text_surface, (60, 60))
#             text_surface = font.render("Old high score: "+scr, True, [255, 255, 255])
#             self.screen.blit(text_surface, (60, 80))
#             text_surface = font.render("New high score: "+str(self.credit), True, [255, 255, 255])
#             self.screen.blit(text_surface, (60, 100))
#             self.writehs(myhsfile)
#         else:
#             font = pygame.font.Font("data/LiberationSans-Regular.ttf", 15)
#             text_surface = font.render("You ended the game, but you don't have a new high score...", True, [255, 255, 255])
#             self.screen.blit(text_surface, (60, 60))
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:
#                 self.bgsound.stop()
#                 plc = Menu()
    
    def writehs(self, myhsfile):
        writef = open(myhsfile, "w")
        writef.write(str(self.credit))
        writef.close()
        

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
            

    # .settings:
    homedir = os.path.expanduser("~")
    if homedir[0] == "/":
        mydir = homedir+"/.bfruit"
        myhsfile = mydir+"/hs"
    else:
        mydir = homedir+"\Application Data\.bfruit"
        myhsfile = mydir+"\hs"
    if os.path.exists(mydir) == False:
        os.mkdir(mydir)
    if os.path.exists(myhsfile) == False:
        open(myhsfile, "w").close()
    hsf = open(myhsfile, "r+")
    scr = hsf.readline() # high score
    hsf.close()
    if scr == "":
        scr = "1"

    # pygame init, set display
    pygame.init()
    screen = pygame.display.set_mode([640, 480], 0, 24)
    pygame.display.set_caption("Lucky Kitty MkII")
    pygame.mouse.set_visible(False)
    
    # intro
#     border = pygame.image.load("data/intro/border.png").convert()
#     point = pygame.image.load("data/intro/point.png").convert()
#     sun = pygame.image.load("data/intro/sun.png").convert()
    
#     szam = 0
#     while szam < 256:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 exit()
#             if event.type == pygame.KEYDOWN:
#                 plc = Menu()
#     screen.fill([0, 0, 0])
#         border.set_alpha(szam)
#         point.set_alpha(szam)
#         screen.blit(border, (160, 120))
#         screen.blit(point, (185, 150))
#         screen.blit(point, (185, 180))
#         screen.blit(point, (185, 210))
#         screen.blit(point, (185, 240))
#         screen.blit(point, (185, 270))
#         screen.blit(point, (215, 150))
#         screen.blit(point, (215, 180))
#         screen.blit(point, (215, 210))
#         screen.blit(point, (215, 240))
#         screen.blit(point, (215, 270))
#         screen.blit(point, (245, 150))
#         screen.blit(point, (245, 180))
#         screen.blit(point, (245, 210))
#         screen.blit(point, (245, 240))
#         screen.blit(point, (245, 270))
#         screen.blit(point, (275, 150))
#         screen.blit(point, (275, 180))
#         screen.blit(point, (275, 210))
#         screen.blit(point, (275, 240))
#         screen.blit(point, (275, 270))
#         screen.blit(point, (305, 150))
#         screen.blit(point, (305, 180))
#         screen.blit(point, (305, 210))
#         screen.blit(point, (305, 240))
#         screen.blit(point, (305, 270))
#         screen.blit(point, (335, 150))
#         screen.blit(point, (335, 180))
#         screen.blit(point, (335, 210))
#         screen.blit(point, (335, 240))
#         screen.blit(point, (335, 270))
#         screen.blit(point, (365, 150))
#         screen.blit(point, (365, 180))
#         screen.blit(point, (365, 210))
#         screen.blit(point, (365, 240))
#         screen.blit(point, (365, 270))
#         screen.blit(point, (395, 150))
#         screen.blit(point, (395, 180))
#         screen.blit(point, (395, 210))
#         screen.blit(point, (395, 240))
#         screen.blit(point, (395, 270))
#         screen.blit(point, (425, 150))
#         screen.blit(point, (425, 180))
#         screen.blit(point, (425, 210))
#         screen.blit(point, (425, 240))
#         screen.blit(point, (425, 270))
#         szam = szam + 4
#     pygame.display.update()
#     
    starttime = time.perf_counter()
    
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 exit()
#             if event.type == pygame.KEYDOWN:
#                 plc = Menu()
#                 
#         screen.blit(border, (160, 120))
#         
#         screen.blit(point, (185, 150))
#         screen.blit(point, (185, 180))
#         screen.blit(point, (185, 210))
#         screen.blit(point, (185, 240))
#         if time.perf_counter() - starttime < 1:
#             screen.blit(point, (185, 270))
#         if time.perf_counter() - starttime < 1.2:
#             screen.blit(point, (215, 150))
#         screen.blit(point, (215, 180))
#         if time.perf_counter() - starttime < 1.15:
#             screen.blit(point, (215, 210))
#         if time.perf_counter() - starttime < 1.2:
#             screen.blit(point, (215, 240))
#         if time.perf_counter() - starttime < 1.23:
#             screen.blit(point, (215, 270))
#         if time.perf_counter() - starttime < 1.18:
#             screen.blit(point, (245, 150))
#         if time.perf_counter() - starttime < 1.2:
#             screen.blit(point, (245, 180))
#         screen.blit(point, (245, 210))
#         if time.perf_counter() - starttime < 1.43:
#             screen.blit(point, (245, 240))
#         if time.perf_counter() - starttime < 1.5:
#             screen.blit(point, (245, 270))
#         screen.blit(point, (275, 150))
#         screen.blit(point, (275, 180))
#         screen.blit(point, (275, 210))
#         screen.blit(point, (275, 240))
#         if time.perf_counter() - starttime < 1.22:
#             screen.blit(point, (275, 270))
#         if time.perf_counter() - starttime < 1.41:
#             screen.blit(point, (305, 150))
#         if time.perf_counter() - starttime < 1.34:
#             screen.blit(point, (305, 180))
#         if time.perf_counter() - starttime < 1.4:
#             screen.blit(point, (305, 210))
#         if time.perf_counter() - starttime < 1.36:
#             screen.blit(point, (305, 240))
#         if time.perf_counter() - starttime < 1.1:
#             screen.blit(point, (305, 270))
#         screen.blit(point, (335, 150))
#         screen.blit(point, (335, 180))
#         screen.blit(point, (335, 210))
#         screen.blit(point, (335, 240))
#         screen.blit(point, (335, 270))
#         screen.blit(point, (365, 150))
#         if time.perf_counter() - starttime < 1.13:
#             screen.blit(point, (365, 180))
#         screen.blit(point, (365, 210))
#         if time.perf_counter() - starttime < 1.4:
#             screen.blit(point, (365, 240))
#         screen.blit(point, (365, 270))
#         screen.blit(point, (395, 150))
#         if time.perf_counter() - starttime < 1.31:
#             screen.blit(point, (395, 180))
#         screen.blit(point, (395, 210))
#         if time.perf_counter() - starttime < 1.25:
#             screen.blit(point, (395, 240))
#         screen.blit(point, (395, 270))
#         if time.perf_counter() - starttime < 1.43:
#             screen.blit(point, (425, 150))
#         screen.blit(point, (425, 180))
#         if time.perf_counter() - starttime < 2.0:
#             screen.blit(point, (425, 210))
#         screen.blit(point, (425, 240))
#         if time.perf_counter() - starttime < 2.4:
#             screen.blit(point, (425, 270))
#             
#         if time.perf_counter() - starttime > 3:
#             font = pygame.font.Font("data/LiberationSans-Regular.ttf", 25)
#             text_surface = font.render("nXBalazs" , True, [255, 255, 255])
#             screen.blit(text_surface, (190, 273))
#         if time.perf_counter() - starttime > 3.5:
#             font = pygame.font.Font("data/LiberationSans-Regular.ttf", 25)
#             text_surface = font.render("games" , True, [255, 255, 255])
#             screen.blit(text_surface, (280, 310))
#         if 5 > time.perf_counter() - starttime > 4:
#             szamsun = 0
#             while szamsun < 100:
#                 sun.set_alpha(szamsun)
#                 screen.blit(sun, (0, 0))
#                 szamsun = szamsun + 1
#                 pygame.display.update()
#         if time.perf_counter() - starttime > 1:
    plc = Game() #This is how you do a new thing, dont even need the plc
    
    pygame.display.update()
