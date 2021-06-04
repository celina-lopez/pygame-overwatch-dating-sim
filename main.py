import pygame
from pygame import mixer
import time, os
from pygame.locals import *
import math
import json
import textwrap

pygame.init()

#STORY DATA
with open('maindialogue.json') as f:
  dialogue_json = json.load(f)

#CONSTANTS
clock = pygame.time.Clock()
FPS = 120

#screen size
screen = pygame.display.set_mode((800, 600)) #create the screen w and h 


#background dictionary
background_dictionary = {"default": pygame.image.load('Images/Background.png'), 
"casual": pygame.transform.scale(pygame.image.load('Images/background_pos.jpg').convert_alpha(),(800,600)),
"kingsrow":pygame.transform.scale(pygame.image.load('Images/kings_row.jpg').convert_alpha(),(800,600)),
"black": pygame.image.load("Images/black.jpg")}


#textbox
textbox = pygame.transform.scale(pygame.image.load('Images/textbox.png').convert_alpha(), (600,210))

#window icon and title
pygame.display.set_caption("Mercy Dating Sim") #Title of game
icon = pygame.image.load('Images/heart.png') #Icon
pygame.display.set_icon(icon) 

#buttons
button_dictionary = {"main_menu_buttons": pygame.transform.scale(pygame.image.load("Images/newButton.png").convert_alpha(), (125,55)), 
                    "text_button": pygame.transform.scale(pygame.image.load("Images/output-onlinepngtools (1).png").convert_alpha(), (450, 80)),
                    "main_bigger": pygame.transform.scale(pygame.image.load("Images/newButton.png").convert_alpha(), (135,65))
                }
sound_dictionary = {"Heroes never die!": 'Music/Heroes_never_die!.mp3'
    
}

Progress_dictionary = {"Mercy":{"Pre": 0}}

#love interest
mc = "Unknown"
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
    } #fix json 


# background sound
# mixer.music.load('Music/OVERWATCH SOUNDTRACK - 113 - Hollywood.mp3')
# mixer.music.set_volume(1)
# mixer.music.play()


#FUNCTIONS
def font_size(font='Fonts/bignoodletoo.ttf' , size=25):
    return pygame.font.Font(font, size)

def wrap_text(message, wraplimit):
    return textwrap.fill(message, wraplimit)

def message_display(message, image = None):
    y = 200 
    message = wrap_text(message,75)
    full_text = [" "]
    if image == None:
        screen.fill((0,0,0))
    else:
        newImage(0,0,image)
    for part in message.split('\n'):
        scroll = []
        for p in part:
            scroll.append(p)
            rendered_text = font_size().render("".join(scroll), True, (255,255,255))
            if image == None:
                pygame.draw.rect(screen, (0,0,0),(120,190,534, 100))
            else:
                newImage(0,0, image)
            for i in full_text:
                rendered_full = font_size().render(i, True, (255,255,255))
                screen.blit(rendered_full,(120, y - 25))
            screen.blit(rendered_text,(120, y))
            pygame.display.update()
            pygame.time.wait(5) #unhash when done editing total length of previous character
        full_text.append(part)
        y += 25

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

def show_title(): 
    title = font_size('Fonts/bignoodletoo.ttf', 46).render("Mercy  Dating  Sim!", True, (255,255,255))
    temp_surface = pygame.Surface(title.get_size())
    temp_surface.fill((210, 145, 188))
    screen.blit(temp_surface, (220+40, 70))
    screen.blit(title, (220+40, 70))

def convo_text(bg, mcs, emo, txt, char):
    txt_font = font_size('Fonts/PlayfairDisplay-Regular.ttf', 20)
    char = font_size().render(char, True, (210, 145, 188))
    # txtbox_surface = pygame.Surface((534, 135))
    # txtbox_surface.fill((255,255,255))
    pygame.draw.rect(screen, (255, 255,255),(123,407,534, 135))
    newImage(90, 370, textbox)
    screen.blit(char, (160, 420))
    txting = []

    for x in txt:
        txting.append(x)
        pygame.draw.rect(screen, (255, 255,255),(153,448,470, 50))
        txts = txt_font.render("".join(txting), True, (0, 0, 0))
        screen.blit(txts,(160, 450))
        w = "w"
        while w == "w":
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        pygame.display.update()
                        w = "b"
            pygame.display.update()
            pygame.time.wait(10) #unhash when done editing
            w= "b"

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

def mousepos(mousex, mousey):
    "shows mouse position for refrence"
    mouserect = pygame.Rect(mousex, mousey, 10, 10)
    print(mouserect)

def typebox(question):
  "ask(screen, question) -> answer"
  run = True
  current_string = []
  while run == True:
    txt_font = font_size('Fonts/PlayfairDisplay-Regular.ttf', 20)
    temp_surface = pygame.Surface((305, 40))
    temp_surface.fill((210, 145,188))
    lol = screen.blit(temp_surface, (245, 251))
    display_txt = "".join(current_string)
    variable = txt_font.render(question, True, (255, 255,255))
    typing = txt_font.render(display_txt, True, (255, 255, 255))
    screen.blit(variable, (255, 255))
    screen.blit(typing, (318, 255))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == 8:
            current_string = current_string[0:-1]
        elif event.type == pygame.KEYDOWN and event.key == 13:
            run = False
            return display_txt
        elif event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN and event.key < 123 and event.key > 91:
            kpress = pygame.key.get_pressed()
            if (kpress[pygame.K_LSHIFT] or kpress[pygame.K_RSHIFT]) and len(current_string) < 11:
                current_string.append(chr(event.key).upper())
            elif len(current_string) < 11:  
                current_string.append(pygame.key.name(event.key))
    pygame.display.update()

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

def while_wait(right):
    wait = True
    while wait == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and right == "right":
                    wait = False
            if event.type == pygame.QUIT:
                quit()

def action_json(scene):
    global mc
    global Progress_dictionary
    for dialogue in dialogue_json[scene]:
        background = dialogue["Background"]
        button = dialogue["Button"]
        base = dialogue['Character']
        maincharacter = "Unknown"
        if "SettingText" in dialogue:
            setting = dialogue["SettingText"]
            for settingtext in setting:
                if settingtext != setting[0]:
                    while_wait("right")
                message_display(settingtext)
                while_wait("right")
    message_display("Now Entering " + background, background_dictionary[background])
    pygame.display.update()
    while_wait("right")
    for charline in base:
        character = base[charline][0]
        if character == "Unknown":
            character = mc
        emotion = base[charline][1]
        for line in base[charline][2:]:
            if line == "ENTER NAME":
                mc = gameSlide(background_dictionary["casual"], "Mercy", "Default", "ENTER NAME")
            else:
                # if line in sound_dictionary:
                #     mixer.music.load(sound_dictionary[line])
                #     mixer.music.play()  
                texts = []
                for letter in line:
                    if letter == "*":
                        texts.append(mc)
                    else:
                        texts.append(letter)
                finaltxt = "".join(texts)
                gameSlide(background_dictionary[background], character, emotion, finaltxt)
    choice = optionSlide(background_dictionary[background], button[0], button[1], button[2], character, emotion)
    if choice == 1:
        end = "Good"
        Progress_dictionary[scene] = +1
    elif choice == 2:
        end = "Bad"
        Progress_dictionary[scene] = -1
    elif choice == 3:
        end = "Neutral"
        Progress_dictionary[scene] = 0
    for good in dialogue['Endings'][end]["Character"]:
        char = dialogue['Endings'][end]["Character"][[good][0]][0]
        if char == "Unknown":
            char = mc
        emo = dialogue['Endings'][end]["Character"][[good][0]][1]
        for lin in dialogue['Endings'][end]["Character"][[good][0]][2:]:
            gameSlide(background_dictionary[background], char, emo, lin) 


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