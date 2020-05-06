pygame.init() """dont need"""

import pygame
from pygame import mixer
import time, os
from pygame.locals import *
import math
import json
import textwrap

#STORY DATA - NEED
with open('maindialogue.json') as f:
  dialogue_json = json.load(f)

#CONSTANTS - NEED
clock = pygame.time.Clock()
FPS = 120

#textbox - INITIALLIZED - COME BACK
textbox = pygame.transform.scale(pygame.image.load('Images/textbox.png').convert_alpha(), (600,210))

#INITALIZED - COME BACK
def font_size(font='Fonts/bignoodletoo.ttf' , size=25):
    return pygame.font.Font(font, size)

#screen size - SET
screen = pygame.display.set_mode((800, 600)) #create the screen w and h 

#window icon and title
pygame.display.set_caption("Mercy Dating Sim") #Title of game
icon = pygame.image.load('Images/heart.png') #Icon
pygame.display.set_icon(icon) 

#love interest
mc = "Unknown"

#love interest - INITIALIZED - COME BACk
love_interest = {
    "mainscreen": {"main":[pygame.image.load('Images/Mercy.png'),-150, 210]},
    "Mercy":{"Default": [pygame.image.load('Images/Mercy.png'), 170, 40], 
            "Normal": [pygame.transform.scale(pygame.image.load('Images/normalmercy.png').convert_alpha(), (600,500)),350, 40],
            "Angry": [pygame.image.load("Images/MercyAngry.png"), 170, 40], 
            "Action": [pygame.image.load('Images/othermercy.png'), 170, 30],
            "Badass": [pygame.transform.scale(pygame.image.load('Images/pngwave (1).png').convert_alpha(), (400,300)),350, 100]},
    mc:{"Default":[pygame.image.load("Images/transparent.png"), 0,0]},
    "????": {"Default": [pygame.image.load("Images/transparent.png"),0,0]},
    "Nava": {"Default": [pygame.transform.scale(pygame.image.load('Images/nava.png').convert_alpha(), (370,600)), 350, 40]}
    } 

def love_screen_location(love,emotion):
    "Shows where the love interest will be on screen, changes with the size of the image, c is the direction it will go if any"
    if love not in love_interest:
        screen.blit(love_interest["????"]["Default"][0], (love_interest["????"]["Default"][1],love_interest["????"]["Default"][2]))
    else:
        screen.blit(love_interest[love][emotion][0], (love_interest[love][emotion][1], love_interest[love][emotion][2]))


#blit onscreen
def newImage(x,y,loadedimage):
    "new image load, use the dictionary"
    screen.blit(loadedimage, (x, y))


    def convo_text(bg, mcs, emo, txt, char):
    txting = []

    for x in txt:
        txting.append(x)
        pygame.draw.rect(screen, (255, 255,255),(153,448,470, 50))
        txts = txt_font.render("".join(txting), True, (0, 0, 0))
        screen.blit(txts,(160, 450))    
            pygame.time.wait(10) #unhash when done editing
            w= "b"


def Gameloop():
    clock.tick(FPS)
    game_intro()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                mousepos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        for i in dialogue_json:
            action_json(i)
        print(Progress_dictionary)
        running = False
        pygame.display.update()


#Start Game
Gameloop()

def while_wait(right):
    wait = True
    while wait == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and right == "right":
                    wait = False
            if event.type == pygame.QUIT:
                quit()

def newGameButton(x,y, imageget, text = None, tx = None, ty= None, size = 35):
    "new button maker"
    newGameButton = button_dictionary[imageget]
    x_len = newGameButton.get_width()
    y_len = newGameButton.get_height()
    screen.blit(newGameButton, (x,y)) 
    if text != None:
        txt_font = font_size('Fonts/bignoodletoo.ttf', size)
        variable = txt_font.render(text, True, (255, 255,255))
        screen.blit(variable, (tx, ty))
    mos_x, mos_y = pygame.mouse.get_pos()
    if mos_x > x and (mos_x < x + x_len):
        x_inside = True
    else:
        x_inside = False
    if mos_y > y and (mos_y < y + y_len):
        y_inside = True
    else:
        y_inside = False
    if x_inside and y_inside:
        return True

def show_title(): 
    title = font_size('Fonts/bignoodletoo.ttf', 46).render("Mercy  Dating  Sim!", True, (255,255,255))
    temp_surface = pygame.Surface(title.get_size())
    temp_surface.fill((210, 145, 188))
    screen.blit(temp_surface, (220+40, 70))
    screen.blit(title, (220+40, 70))

def mousepos(mousex, mousey):
    "shows mouse position for refrence"
    mouserect = pygame.Rect(mousex, mousey, 10, 10)
    print(mouserect)

def optionSlide(bg, msg1, msg2, msg3, char, emo):
    wait = True
    while wait == True:
        txt_font = font_size('Fonts/PlayfairDisplay-Regular.ttf',20)
        txt = txt_font.render(msg1, True, (0, 0, 0))
        txt2 = txt_font.render(msg2, True, (0, 0, 0))
        txt3 = txt_font.render(msg3, True, (0, 0, 0))
        newImage(0, 0, bg)
        love_screen_location(char, emo) #sam thing as befire ehh
        a = newGameButton(50, 120,"text_button")
        b = newGameButton(50, 220,"text_button")
        c = newGameButton(50, 320,"text_button")
        screen.blit(txt, (70, 140))
        screen.blit(txt2, (70, 240))
        screen.blit(txt3, (70, 340))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONUP and a == True:
                return 1
            elif event.type == pygame.MOUSEBUTTONUP and b == True:
                return 2
            elif event.type == pygame.MOUSEBUTTONUP and c == True:
                return 3

# function inputHandler(state){
# 	document.addEventListener("keydown", event => {
# 		switch((event.keyCode == 39) || (event.keyCode >= 65 && event.keyCode <= 90)){
# 			case 39:
# 				if(state["intro"] == "off"){
# 					update(state, 39);
# 				}
# 				break;
# 			default:
# 				if (state["special"]["ENTER NAME"] == "on"){
# 					console.log("booyah");
		# }


# 

#progress - NEED
Progress_dictionary = {"Mercy":{"Pre": 0}}

def gameSlide(bg, char, emo, msg):
    global mc
    "basic slide"
    maincharacter = char
    if char == "Unknown":
        maincharacter = mc
    newImage(0, 0, bg)
    love_screen_location(char, emo)#same thing as other
    if msg == "ENTER NAME":
        mc = typebox("Name: ")
        return mc
    elif maincharacter == None and char == None:
        # newImage(0,0, bg) #check if this needs to be there
        variable = font_size().render(msg, True, (255, 255,255))
        screen.blit(variable, (100, 100))
    elif msg == None:
        pygame.display.update()
    else:
        convo_text(bg, char, emo, msg, maincharacter)
        pygame.display.update()
        while_wait("right")
def game_intro():
    intro = True
    while intro:
        bg = pygame.image.load("Images/Background.png")
        screen.blit(bg, (0, 0))
        show_title()
        love_screen_location("mainscreen", "main")
        first = newGameButton(327, 120, 'main_menu_buttons', "START", 358, 132)
        if first == True:
            newGameButton(323, 116, 'main_bigger', "START", 353,130, 40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP and first == True:
                enemyImg = pygame.image.load('Images/Mercy.png')
                enemyx = -150
                enemyy = 210
                change = 7
                while enemyx < 600:
                    screen.blit(background_dictionary["default"], (0, 0))
                    show_title()
                    screen.blit(enemyImg, (enemyx, enemyy))
                    enemyx += change
                    pygame.display.update()
                if enemyx > 600:
                    intro = False
        pygame.display.update()