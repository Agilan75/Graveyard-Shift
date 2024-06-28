"""
Author: Agilan Hariharan
Description: An Original Maze Game: Graveyard Shift
Creation Date: January 08, 2024
Last Modified: January 19, 2024
"""

# I - Import and Initialize - Start IDEA
import pygame
from sprites import Character, Spikes, ScoreKeeper, HomeScreen, HowToPlayScreen, Maze
pygame.init()
pygame.mixer.init()

# D - Display configuration
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Graveyard Shift")

# E - Entities 
background_image = pygame.image.load("Images/background_image.png").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

pygame.mixer.music.load("Sounds/background_music.mp3")
pygame.mixer.music.play(-1)

win_sound = pygame.mixer.Sound("Sounds/win_sound.mp3")
lose_sound = pygame.mixer.Sound("Sounds/lose_sound.mp3")

# A - Action (broken into ALTER steps)
# A - Assign values to key variables
clock = pygame.time.Clock()

# Initialize game objects
character = Character(20, 20)
spikes = pygame.sprite.Group()
timer = ScoreKeeper()
how_to_play_screen = HowToPlayScreen(screen_width, screen_height)
home_screen = HomeScreen(640, 700)
maze = None

# Main menu loop
main_menu = True
selected_level = None
maze = None
running = False

def show_how_to_play_screen():
    """
    Display the How To Play screen.
    """
    how_to_play_screen = HowToPlayScreen(screen_width, screen_height)
    running_how_to_play = True

    # Shows Instructional Screen
    while running_how_to_play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_how_to_play = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if how_to_play_screen.back_rect.collidepoint(event.pos):
                    running_how_to_play = False

        how_to_play_screen.draw(screen)
        pygame.display.flip()

while main_menu:
    # Creates Main Menu Screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_menu = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if home_screen.level1_rect.collidepoint(event.pos):
                selected_level = 1
                main_menu = False
            elif home_screen.level2_rect.collidepoint(event.pos):
                selected_level = 2
                main_menu = False
            elif home_screen.level3_rect.collidepoint(event.pos):
                selected_level = 3
                main_menu = False
            elif home_screen.how_to_play_rect.collidepoint(event.pos):
                show_how_to_play_screen()

    home_screen.draw(screen)
    pygame.display.flip()

# If a level is selected, start the game loop
if selected_level is not None:
    running = True
    current_level = selected_level

    # Create an end rectangle to check if the player reached the destination
    end_rect = pygame.Rect(700, 500, 30, 30)
    maze = Maze(current_level)

# Show the main menu after completing a level
show_main_menu = False

# L - Loop
while running:
    # T - Timer to set frame rate
    clock.tick(30)
    # E - Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_level is not None:
                # Movement System to Play the Game
                if event.key == pygame.K_LEFT:
                    maze.move_player("left")
                elif event.key == pygame.K_RIGHT:
                    maze.move_player("right")
                elif event.key == pygame.K_UP:
                    maze.move_player("up")
                elif event.key == pygame.K_DOWN:
                    maze.move_player("down")
                # Shows Menu Screen based on whether or not destination reached
                if maze.dest_reached:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect.collidepoint(event.pos):
                            maze.dest_reached = False
                            show_main_menu = True  
                if maze.dest_unreached:
                    if event.type == pygame.QUIT:
                        maze.dest_reached = False
                        show_main_menu = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect.collidepoint(event.pos):
                            maze.dest_reached = False
                            show_main_menu = True  
                             

    else:
        # Update Timer and Refresh Baground
        timer.update()
        # R - Refresh display
        screen.blit(background_image,(0,0))
        if not maze.dest_reached:
            maze.render(timer)
        maze.update(timer)

        if timer.time_left <= 0:
            screen.blit(background_image,(0,0))
            # Shows Losing Message
            congrats_font = pygame.font.Font("Fonts/youmurdererbb_reg.ttf", 100)

            congrats_text = congrats_font.render("Unfortunate :(", True, (255, 255, 255))
            congrats_text2 = congrats_font.render(f" You Lost Level {selected_level}", True, (255, 255, 255))

            congrats_rect = congrats_text.get_rect(center=(screen_width // 2, screen_height // 2 - 75)) 
            congrats_rect2 = congrats_text2.get_rect(center=(screen_width // 2, screen_height // 2 + 25)) 

            screen.blit(congrats_text2, congrats_rect2)           
            screen.blit(congrats_text, congrats_rect)

            # Display "Back to Main Menu" button
            button_font = pygame.font.Font("Fonts/youmurdererbb_reg.ttf", 50)
            button_text = button_font.render("Back to Main Menu", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 125))            
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 3)
            screen.blit(button_text, button_rect)
        
        elif maze.dest_unreached:
            screen.blit(background_image,(0,0))
            
            # Shows Losing Message
            congrats_font = pygame.font.Font("Fonts/youmurdererbb_reg.ttf", 100)
            congrats_text = congrats_font.render("Unfortunate :(", True, (255, 255, 255))
            congrats_text2 = congrats_font.render(f" You Lost Level {selected_level}", True, (255, 255, 255))
            congrats_rect = congrats_text.get_rect(center=(screen_width // 2, screen_height // 2 - 75)) 
            congrats_rect2 = congrats_text2.get_rect(center=(screen_width // 2, screen_height // 2 + 25)) 
            screen.blit(congrats_text2, congrats_rect2)           
            screen.blit(congrats_text, congrats_rect)

            # Display "Back to Main Menu" button
            button_font = pygame.font.Font("Fonts/youmurdererbb_reg.ttf", 50)
            button_text = button_font.render("Back to Main Menu", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 125))            
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 3)
            screen.blit(button_text, button_rect)
        
        elif maze.dest_reached:
            screen.blit(background_image,(0,0))
            # Display congratulatory message
            congrats_font = pygame.font.Font("Fonts/youmurdererbb_reg.ttf", 100)
            congrats_text = congrats_font.render("Congrats! You beat", True, (255, 255, 255))
            congrats_text2 = congrats_font.render(f"Level {selected_level}", True, (255, 255, 255))
            congrats_rect = congrats_text.get_rect(center=(screen_width // 2, screen_height // 2 - 75)) 
            congrats_rect2 = congrats_text2.get_rect(center=(screen_width // 2, screen_height // 2 + 25)) 
            screen.blit(congrats_text2, congrats_rect2)           
            screen.blit(congrats_text, congrats_rect)

            # Display "Back to Main Menu" button
            button_font = pygame.font.Font("Fonts/youmurdererbb_reg.ttf", 50)
            button_text = button_font.render("Back to Main Menu", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 125))            
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 3)
            screen.blit(button_text, button_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        # Reset variables and show the main menu
                        maze.dest_reached = False
                        maze.dest_unreached = False
                        show_main_menu = True            
                        while show_main_menu:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    main_menu = False
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    if home_screen.level1_rect.collidepoint(event.pos):
                                        selected_level = 1
                                        show_main_menu = False
                                    elif home_screen.level2_rect.collidepoint(event.pos):
                                        selected_level = 2
                                        show_main_menu = False
                                    elif home_screen.level3_rect.collidepoint(event.pos):
                                        selected_level = 1
                                        show_main_menu = False
                                    elif home_screen.how_to_play_rect.collidepoint(event.pos):
                                        show_how_to_play_screen()

                            home_screen.draw(screen)
                            pygame.display.flip()

                        if selected_level is not None:
                            running = True
                            current_level = selected_level

                            end_rect = pygame.Rect(700, 500, 30, 30)
                            maze = Maze(current_level)                           
                            timer.reset()

        pygame.display.flip()

pygame.quit()