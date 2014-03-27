import pygame
from random import choice
from math import floor



### SETTINGS ###

pygame.init()

size = (1000,550)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Battleship")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana",25)

ship_size = 100
ship_border = 2



### SOUNDS ###

sound_hit = pygame.mixer.Sound("hit.wav")
sound_error = pygame.mixer.Sound("error.wav")
sound_win = pygame.mixer.Sound("win.wav")
sound_lose = pygame.mixer.Sound("lose.wav")



### START GAME FUNCTION ###

def start_game():

    global gameover
    gameover = False

    global turn
    turn = "user"

    global ships_put
    ships_put = 0

    global comp_ship_color
    comp_ship_color = (255,0,0)

    # Creating lists for fields
    global field_user
    global field_comp
    field_user = []
    field_comp = []
    for i in range(25):
        field_user.append(0)
        field_comp.append(0)

    # Creating lists for ships
    global ships_user
    global ships_comp
    ships_user = []
    ships_comp = []

    # Creating lists for available shots
    global shots_user
    global shots_comp
    shots_user = []
    shots_comp = []
    for i in range(25):
        shots_user.append(i)
        shots_comp.append(i)
        
    # Computer puts 5 ships
    while len(ships_comp) < 5:
        new_ship_comp = choice(range(25))
        if new_ship_comp not in ships_comp:
            ships_comp.append(new_ship_comp)
            field_comp[new_ship_comp] = 1



### DRAWING SQUARES FUNCTIONS ###

def draw_user_empty(x,y):
    pygame.draw.rect(screen, (255,255,255), [x,y,ship_size,ship_size])
    pygame.draw.rect(screen, (0,0,255), [x+ship_border,y+ship_border,ship_size-2*ship_border,ship_size-2*ship_border])

def draw_user_ship(x,y):
    pygame.draw.rect(screen, (255,255,255), [x,y,ship_size,ship_size])
    pygame.draw.rect(screen, (0,0,100), [x+ship_border,y+ship_border,ship_size-2*ship_border,ship_size-2*ship_border])

def draw_user_empty_hit(x,y):
    pygame.draw.rect(screen, (255,255,255), [x,y,ship_size,ship_size])
    pygame.draw.rect(screen, (0,0,255), [x+ship_border,y+ship_border,ship_size-2*ship_border,ship_size-2*ship_border])
    pygame.draw.circle(screen, (0,0,0), [int(x+ship_size/2),int(y+ship_size/2)], 20)

def draw_user_ship_hit(x,y):
    pygame.draw.rect(screen, (255,255,255), [x,y,ship_size,ship_size])
    pygame.draw.rect(screen, (0,0,100), [x+ship_border,y+ship_border,ship_size-2*ship_border,ship_size-2*ship_border])
    pygame.draw.circle(screen, (0,0,0), [int(x+ship_size/2),int(y+ship_size/2)], 20)

def draw_comp_empty(x,y):
    pygame.draw.rect(screen, (255,255,255), [x,y,ship_size,ship_size])
    pygame.draw.rect(screen, (255,0,0), [x+ship_border,y+ship_border,ship_size-2*ship_border,ship_size-2*ship_border])

def draw_comp_ship(x,y):
    pygame.draw.rect(screen, (255,255,255), [x,y,ship_size,ship_size])
    pygame.draw.rect(screen, comp_ship_color, [x+ship_border,y+ship_border,ship_size-2*ship_border,ship_size-2*ship_border])

def draw_comp_empty_hit(x,y):
    pygame.draw.rect(screen, (255,255,255), [x,y,ship_size,ship_size])
    pygame.draw.rect(screen, (255,0,0), [x+ship_border,y+ship_border,ship_size-2*ship_border,ship_size-2*ship_border])
    pygame.draw.circle(screen, (0,0,0), [int(x+ship_size/2),int(y+ship_size/2)], 20)

def draw_comp_ship_hit(x,y):
    pygame.draw.rect(screen, (255,255,255), [x,y,50,50])
    pygame.draw.rect(screen, (139,0,0), [x+ship_border,y+ship_border,ship_size-2*ship_border,ship_size-2*ship_border])
    pygame.draw.circle(screen, (0,0,0), [int(x+ship_size/2),int(y+ship_size/2)], 20)



### DRAWING FIELDS FUNCTIONS ###

def show_fields():

    # Clear the screen
    screen.fill((255,255,255))

    # Do for each row
    for i in range(5):

        # Do five user squares
        for j in range(5):
            if field_user[j+i*5] == 0:
                draw_user_empty(j*ship_size,i*ship_size)
            elif field_user[j+i*5] == 1:
                draw_user_ship(j*ship_size,i*ship_size)
            elif field_user[j+i*5] == 2:
                draw_user_empty_hit(j*ship_size,i*ship_size)
            elif field_user[j+i*5] == 3:
                draw_user_ship_hit(j*ship_size,i*ship_size)

        if ships_put > 4:

            # Do five comp squares
            for k in range(5,10):
                if field_comp[k-5+i*5] == 0:
                    draw_comp_empty(k*ship_size,i*ship_size)
                elif field_comp[k-5+i*5] == 1:
                    draw_comp_ship(k*ship_size,i*ship_size)
                elif field_comp[k-5+i*5] == 2:
                    draw_comp_empty_hit(k*ship_size,i*ship_size)
                elif field_comp[k-5+i*5] == 3:
                    draw_comp_ship_hit(k*ship_size,i*ship_size)

    # Message "put ships"
    if ships_put < 5:
        text1 = font.render("PUT FIVE SHIPS ON YOUR FIELD", True, (0,0,0))
        screen.blit(text1,[45,508])
        
    # Or message "current score"
    elif ships_put > 4 and not gameover:
        text2 = font.render("YOUR SHIPS: " + str(len(ships_user)), True, (0,0,0))
        screen.blit(text2,[10, 508])
        text3 = font.render("COMP SHIPS: " + str(len(ships_comp)), True, (0,0,0))
        screen.blit(text3,[795, 508])

    # Or message "gameover"
    elif ships_put > 4 and gameover:
        screen.blit(text4,[420, 508])

    # Show everything
    pygame.display.flip()



### START GAME ###

done = False

start_game()


    
### MAIN LOOP ###

while not done:
        
    # Limit to 20 frames per second
    clock.tick(20)
    
    # Events    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()

            # For testing and cheating :)
            if key[pygame.K_c]:
                comp_ship_color = (139,0,0)

            # To restart during the game
            elif key[pygame.K_r]:
                start_game()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Get mouse coordinates and save them
            pos = pygame.mouse.get_pos()
            x_user = pos[0]
            y_user = pos[1]

            # If user haven't put 5 ships yet
            if ships_put < 5:

                # If mouse is clicked inside user field
                if x_user < size[0] / 2:

                    # Convert coordinates to new ship
                    new_ship_user = floor(x_user / ship_size) + floor(y_user / ship_size) * 5

                    # If this new ship is not on field yet
                    if new_ship_user not in ships_user:

                        field_user[new_ship_user] = 1                       
                        ships_user.append(new_ship_user)
                        ships_put += 1

                    # If new ship is alrealy on the field
                    else:
                        sound_error.play()

                # If mouse is clicked outside of user field
                else:
                    sound_error.play()

            # If user has put 5 ships on the field
            else:

                # If mouse is clicked inside of comp field
                if x_user > size[0] / 2 and turn == "user":

                    # Convert coordinates to shot
                    shot_user = floor((x_user - size[0] / 2) / ship_size) + floor(y_user / ship_size) * 5

                    # If this shot haven't been done before
                    if shot_user in shots_user:

                        # User hit an empty square
                        if field_comp[shot_user] == 0:
                            field_comp[shot_user] = 2
                            shots_user.remove(shot_user)
                            turn = "comp"

                        # User hit a ship
                        elif field_comp[shot_user] == 1:
                            field_comp[shot_user] = 3
                            ships_comp.remove(shot_user)
                            shots_user.remove(shot_user)
                            sound_hit.play()

                            # If it was the last ship of comp
                            if len(ships_comp) == 0:
                                show_fields()
                                pygame.time.wait(500)
                                sound_win.play()
                                text4 = font.render("YOU WIN!", True, (255,0,0), (255,255,255))
                                gameover = True
                                show_fields()
                                pygame.time.wait(500)
                                start_game()

                            # If comp still has ships, user keeps turn
                            else:
                                turn = "user"
            
                    # Error: this shot have been done before
                    else:
                        sound_error.play()

                # Error: mouse is clicked outside of comp field 
                else:
                    sound_error.play()

    if turn == "comp":

        show_fields()
        
        # Pause
        pygame.time.wait(250)
        
        # Comp makes a shot
        comp_shot = choice(shots_comp)

        # Comp hit an empty square
        if field_user[comp_shot] == 0:
            field_user[comp_shot] = 2
            shots_comp.remove(comp_shot)
            turn = "user"

        # Comp hit a ship
        elif field_user[comp_shot] == 1:
            field_user[comp_shot] = 3
            ships_user.remove(comp_shot)
            shots_comp.remove(comp_shot)
            sound_hit.play()

            # If it was the last ship of user
            if len(ships_user) == 0:
                show_fields()
                pygame.time.wait(500)
                sound_lose.play()
                text4 = font.render("YOU LOSE!", True, (255,0,0), (255,255,255))
                gameover = True
                show_fields()
                pygame.time.wait(500)
                start_game()

            # If user still has ships, computer keeps turn
            else:
                turn = "comp"

    show_fields()



### END GAME ###
    
pygame.time.wait(500)
pygame.quit()
