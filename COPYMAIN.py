
#buttons -INTIALIZED - COME BACK
button_dictionary = {"main_menu_buttons": pygame.transform.scale(pygame.image.load("Images/newButton.png").convert_alpha(), (125,55)), 
                    "text_button": pygame.transform.scale(pygame.image.load("Images/output-onlinepngtools (1).png").convert_alpha(), (450, 80)),
                    "main_bigger": pygame.transform.scale(pygame.image.load("Images/newButton.png").convert_alpha(), (135,65))
                }

#sound - NEED
sound_dictionary = {"Heroes never die!": 'Music/Heroes_never_die!.mp3'}

# background sound - COME BACK
mixer.music.load('Music/OVERWATCH SOUNDTRACK - 113 - Hollywood.mp3')
mixer.music.set_volume(1)
mixer.music.play()


#FUNCTIONS


#FUCK - COME BACK? PROBABLY COULD DO THIS IN HTML OR CSS TBH...
def wrap_text(message, wraplimit):
    return textwrap.fill(message, wraplimit)

#SEE ABOVE
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


def typebox(question):
  "ask(screen, question) -> answer"
    for event in pygame.event.get():
        elif event.type == pygame.KEYDOWN and event.key < 123 and event.key > 91:
            kpress = pygame.key.get_pressed()
            if (kpress[pygame.K_LSHIFT] or kpress[pygame.K_RSHIFT]) and len(current_string) < 11:
                current_string.append(chr(event.key).upper())
            elif len(current_string) < 11:  
                current_string.append(pygame.key.name(event.key))
    # pygame.display.update()



def action_json(scene):

        if "SettingText" in dialogue:
            setting = dialogue["SettingText"]
            for settingtext in setting:
                if settingtext != setting[0]:
                    while_wait("right")
                message_display(settingtext)
    message_display("Now Entering " + background, background_dictionary[background])
 else:
                if line in sound_dictionary:
                    mixer.music.load(sound_dictionary[line])
                    mixer.music.play()  
                texts = []


