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
FPS = 60

#screen size
screen = pygame.display.set_mode((800, 600)) #create the screen w and h

#background dictionary
background_dictionary = {"default": pygame.image.load('Images/Background.png'), "casual": pygame.transform.scale(pygame.image.load('Images/background_pos.jpg').convert_alpha(),(800,600)),
"kingsrow":pygame.transform.scale(pygame.image.load('Images/kings_row.jpg').convert_alpha(),(800,600))}

#textbox
textbox = pygame.transform.scale(pygame.image.load('Images/textbox.png').convert_alpha(), (600,210))

#window icon and title
pygame.display.set_caption("Mercy Dating Sim") #Title of game
icon = pygame.image.load('Images/heart.png') #Icon
pygame.display.set_icon(icon) 

#buttons
button_dictionary = {"main_menu_buttons": pygame.transform.scale(pygame.image.load("Images/newButton.png").convert_alpha(), (125,55)), 
                    "text_button": pygame.transform.scale(pygame.image.load("Images/output-onlinepngtools (1).png").convert_alpha(), (450, 80)),
                    "main_bigger": pygame.transform.scale(pygame.image.load("Images/newButton.png").convert_alpha(), (135,65))}

#love interest
mc = "Unknown"
love_interest = {
    "Mercy":[pygame.image.load('Images/Mercy.png'), 
            pygame.transform.scale(pygame.image.load('Images/normalmercy.png').convert_alpha(), (600,500)),
            pygame.image.load("Images/MercyAngry.png"),
            pygame.image.load('Images/othermercy.png'),
            pygame.transform.scale(pygame.image.load('Images/pngwave (1).png').convert_alpha(), (400,300))],
    mc:[pygame.image.load("Images/transparent.png")],
    "????": [pygame.image.load("Images/transparent.png")],
    "Nava": [pygame.transform.scale(pygame.image.load('Images/nava.png').convert_alpha(), (370,600))]
    }
love_interest_dem = {0: [170, 40, 0], 1: [350, 40, 0], 2: [170, 40, 0], 3:[170, 30, 0], 4:[350, 100, 0]}#dem of photos, emo is the variable for future functions


# background sound
# mixer.music.load('Music/OVERWATCH SOUNDTRACK - 113 - Hollywood.mp3')
# mixer.music.set_volume(1)
# mixer.music.play()


#FUNCTIONS
def font_size(font='Fonts/bignoodletoo.ttf' , size=25):
    return pygame.font.Font(font, size)

def wrap_text(message, wraplimit):
    return textwrap.fill(message, wraplimit)

def message_display(message):
    y = 200 # so we won't modify the original values]
    message = wrap_text(message,88) #textvars[1]
    for part in message.split('\n'):
         rendered_text = font_size().render(part, True, (255,255,255))
         screen.blit(rendered_text,(105, y))
         y += 25
         pygame.display.update()

def love_screen_location(love,emotion, x, y, c):
    "Shows where the love interest will be on screen, changes with the size of the image, c is the direction it will go if any"
    if love not in love_interest:
        screen.blit(love_interest["????"][0], (x,y))
    else:
        screen.blit(love_interest[love][emotion], (x, y))
    c = 1 #for now.. it means change

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
    txtbox_surface = pygame.Surface((534, 135))
    txtbox_surface.fill((255,255,255))
    screen.blit(txtbox_surface,(123,407))
    newImage(90, 370, textbox)
    screen.blit(char, (160, 420))
    txts = txt_font.render(txt, True, (0, 0, 0))
    screen.blit(txts,(160, 450))
    txting = []
    for x in txt:
        txting.append(x)
        newImage(0,0, bg)
        love_screen_location(mcs, emo, love_interest_dem[emo][0], love_interest_dem[emo][1], love_interest_dem[emo][2])
        screen.blit(txtbox_surface,(123,407))
        newImage(90, 370, textbox)
        screen.blit(char, (160, 420))
        screen.blit(char, (160, 420))
        txts = txt_font.render("".join(txting), True, (0, 0, 0))
        screen.blit(txts,(160, 450))
        w = "w"
        while w == "w":
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        pygame.display.update()
                        w = "b"
            pygame.display.update()
            pygame.time.wait(20)
            w= "b"

def newGameButton(x,y, imageget, text = None, tx = None, ty= None, size = 35):
    "new button maker"
    newGameButton = button_dictionary[imageget]
    x_len = newGameButton.get_width()
    y_len = newGameButton.get_height()
    screen.blit(newGameButton, (x,y)) #3 lines below new
    if text != None:
        txt_font = font_size('Fonts/bignoodletoo.ttf', size)
        variable = txt_font.render(text, True, (255, 255,255))
        screen.blit(variable, (tx, ty))
    # pygame.display.update()
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
        love_screen_location("Mercy", 0, -150, 210, 7)
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
        love_screen_location(char, emo, love_interest_dem[emo][0], love_interest_dem[emo][1], love_interest_dem[emo][2])
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
                print(1)
                return 1
            elif event.type == pygame.MOUSEBUTTONUP and b == True:
                print(2)
                return 2
            elif event.type == pygame.MOUSEBUTTONUP and c == True:
                print(3)
                return 3


def gameSlide(bg, char, emo, msg, maincharacter = None):
    global mc
    "basic slide"
    if char != "Unknown":
        maincharacter = char
    elif char == "Unknown":
        maincharacter = mc
    print (maincharacter)
    newImage(0, 0, bg)
    love_screen_location(char, emo, love_interest_dem[emo][0], love_interest_dem[emo][1], love_interest_dem[emo][2])
    if msg == "ENTER NAME":
        mc = typebox("Name: ")
        print(mc)
        return mc
    elif maincharacter == None and char == None:
        newImage(0,0, bg)
        # txt_font = pygame.font.Font('Fonts/bignoodletoo.ttf', 20)
        variable = font_size().render(msg, True, (255, 255,255))
        screen.blit(variable, (100, 100))
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
    # mc = "Unknown"
    global mc
    for dialogue in dialogue_json[scene]:
        background = dialogue["Background"]
        button = dialogue["Button"]
        base = dialogue['Character']
        maincharacter = "Unknown"
        for charline in base:
            character = base[charline][0]
            if character == "Unknown":
                character = mc
            emotion = int(base[charline][1])
            print(character)
            for line in base[charline][2:]:
                print(line)
                if line == "ENTER NAME":
                    print(line)
                    print("start")
                    mc = gameSlide(background_dictionary["casual"], "Mercy", 1, "ENTER NAME")
                    print(mc)
                    print("done")
                else:
                    texts = []
                    for letter in line:
                        if letter == "*":
                            texts.append(mc)
                        else:
                            texts.append(letter)
                    print(texts)
                    finaltxt = "".join(texts)
                    gameSlide(background_dictionary[background], character, emotion, finaltxt, character) 
    choice = optionSlide(background_dictionary[background], button[0], button[1], button[2], character, emotion)
    if choice == 1:
        end = "Good"
    elif choice == 2:
        end = "Bad"
    elif choice == 3:
        end = "Neutral"
    for good in dialogue['Endings'][end]["Character"]:
        char = dialogue['Endings'][end]["Character"][[good][0]][0]
        if char == "Unknown":
            char = mc
        emo = int(dialogue['Endings'][end]["Character"][[good][0]][1])
        for lin in dialogue['Endings'][end]["Character"][[good][0]][2:]:
            gameSlide(background_dictionary[background], char, emo, lin) 


def Gameloop():
    clock.tick(FPS)
    game_intro()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                mousepos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        for i in dialogue_json:
            action_json(i)
        running = False
        pygame.display.update()


Gameloop()