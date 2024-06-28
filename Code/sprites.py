"""
Author: Agilan Hariharan
Description: An Original Maze Game: Graveyard Shift
Creation Date: January 08, 2024
Last Modified: January 19, 2024
"""
# Import and Initialize
import pygame
import random

# Global Constants for colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Entities
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

background_image = pygame.image.load("Images/background_image.png").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

pygame.mixer.init()
move_sound = pygame.mixer.Sound("Sounds/move_sound.mp3")
spike_sound = pygame.mixer.Sound("Sounds/spike_spawn.mp3")
lose_sound = pygame.mixer.Sound("Sounds/lose_sound.mp3")


class Character(pygame.sprite.Sprite):
    """
    Class representing the player character in the game.
    """
    def __init__(self, screen_width, screen_height):
        """
        Initialize the Character object.
        """
        super().__init__()
        # Use the properly scaled background image as the surface
        self.image = pygame.image.load("Images/character.png").convert()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (20, 20)

    def update(self, maze):
        """
        Update the position of the character based on user input.
        """
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        elif keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1

        self.rect.x += dx
        self.rect.y += dy

        # Check for collisions with walls and reset position if collided
        if pygame.sprite.spritecollide(self, maze.walls, False):
            self.rect.topleft = (20, 20)

    def draw(self, screen):
        """
        Draw the character on the screen.
        """
        screen.blit(self.image, self.rect)


class ScoreKeeper(pygame.sprite.Sprite):
    """
    Class representing the score keeper and timer in the game.
    """
    def __init__(self):
        """
        Initialize the ScoreKeeper object.
        """
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.time_left = 45
        self.last_time_update = pygame.time.get_ticks()

    def update(self):
        """
        Update the timer and decrement time left.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time_update >= 1000:
            self.time_left -= 1
            self.last_time_update = current_time

    def draw(self, screen):
        """
        Draw the time left on the screen.
        """
        text = self.font.render(f"Time Left: {max(0, self.time_left)}", True, WHITE)
        screen.blit(text, (10, 10))

    def time_up(self):
        """
        Check if the time has run out.
        """
        return self.time_left <= 0
    def reset(self, initial_time = 45):
        self.time_left = initial_time
        self.last_time_update = pygame.time.get_ticks()
class HowToPlayScreen(pygame.sprite.Sprite):
    """
    Class representing the How to Play screen.
    """
    def __init__(self, screen_width, screen_height):
        """
        Initialize the HowToPlayScreen object.
        """
        self.image = pygame.image.load("Images/background_image.png").convert()
        self.image = pygame.transform.scale(self.image, (background_image.get_width(), background_image.get_height()))
        self.rect = self.image.get_rect()

        self.title_font = pygame.font.Font("Fonts/youmurdererbb_reg.ttf", 100)
        self.title = self.title_font.render("How to Play", True, WHITE)
        self.title_rect = self.title.get_rect(center=(screen_width // 2, 50))
        self.instructions = [
            "Welcome to Graveyard Shift!",
            "Navigate through the maze to reach the end.",
            "Use the arrow keys to move the character.",
            "Avoid zombies and reach the exit by the time limit.",
            "Zombies stay where they are, even if they disappear,",
            "meaning you can run into empty space and die",
            "Click on Level 1, Level 2, or Level 3 to start",
            "Good luck!",
        ]
        self.button_font = pygame.font.Font("Fonts/mrsmonstercondital.ttf", 35)
        self.instruction_texts = [self.button_font.render(text, True, WHITE) for text in self.instructions]
        self.instruction_rects = [text.get_rect(center=(screen_width // 2, 150 + i * 30)) for i, text in enumerate(self.instruction_texts)]
        self.back_button = self.button_font.render("Back to Menu", True, WHITE)
        self.back_rect = self.back_button.get_rect(center=(screen_width // 2, screen_height - 50))
        pygame.draw.rect(self.back_button, WHITE, self.back_button.get_rect(), 2)

    def draw(self, screen):
        """
        Draw the How to Play Screen
        """
        screen.blit(self.image, self.rect)
        screen.blit(self.title, self.title_rect)
        for text, rect in zip(self.instruction_texts, self.instruction_rects):
            screen.blit(text, rect)
        screen.blit(self.back_button, self.back_rect)

class HomeScreen(pygame.sprite.Sprite):
    """
    Class representing the Home screen.
    """
    def __init__(self, screen_width, screen_height):
        """
        Initialize the HomeScreen object.
        """
        super().__init__()
        # Use background image as the surface
        self.image = pygame.image.load("Images/background_image.png").convert()
        self.image = pygame.transform.scale(self.image, (background_image.get_width(), background_image.get_height()))
        self.rect = self.image.get_rect()

        self.title_font = pygame.font.Font("Fonts/youmurdererbb_reg.ttf", 100)
        self.title = self.title_font.render("Graveyard Shift", True, WHITE)
        self.title_rect = self.title.get_rect(center=(screen_width // 2, 50))

        self.button_font = pygame.font.Font("Fonts/mrsmonstercondital.ttf", 60)

        self.level1_button = self.button_font.render("Level 1", True, WHITE)
        self.level1_rect = self.level1_button.get_rect(center=(screen_width//4, 225))
        pygame.draw.rect(self.level1_button, WHITE, self.level1_button.get_rect(), 2)

        self.level2_button = self.button_font.render("Level 2", True, WHITE)
        self.level2_rect = self.level2_button.get_rect(center=(screen_width // 2, 325))
        pygame.draw.rect(self.level2_button, WHITE, self.level2_button.get_rect(), 2)

        self.level3_button = self.button_font.render("Level 3", True, WHITE)
        self.level3_rect = self.level3_button.get_rect(center=(480, 425))
        pygame.draw.rect(self.level3_button, WHITE, self.level3_button.get_rect(), 2)

        self.how_to_play_button = self.button_font.render("How to Play", True, WHITE)
        self.how_to_play_rect = self.how_to_play_button.get_rect(center=(screen_width//2, 125))
        pygame.draw.rect(self.how_to_play_button, WHITE, self.how_to_play_button.get_rect(), 2)

    def draw(self, screen):
        """
        Draw the Home screen on the window.
        """
        screen.blit(self.image, self.rect)
        screen.blit(self.title, self.title_rect)
        screen.blit(self.level1_button, self.level1_rect)
        screen.blit(self.level2_button, self.level2_rect)
        screen.blit(self.level3_button, self.level3_rect)
        screen.blit(self.how_to_play_button, self.how_to_play_rect)

class Spikes(pygame.sprite.Sprite):
    """
    Class representing spikes in the game.
    """
    def __init__(self, x, y, size):
        """
        Initialize a spike/zombie sprite.
        """
        super().__init__()
        self.image = pygame.image.load("Images/spike.png").convert()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawn_time = pygame.time.get_ticks()
        self.sound = pygame.mixer.Sound("Sounds/spike_spawn.mp3")

    def draw(self, screen):
        """
        Draw the spike on the given screen.
        """
        screen.blit(self.image, self.rect)

class Maze(pygame.sprite.Sprite):
    """
    Class representing the maze.
    """
    def __init__(self, current_level):
        """
        Initialize the maze.
        """
        super().__init__()
        self.image = pygame.image.load("Images/background_image.png").convert()
        self.rect = self.image.get_rect()

        self.level = current_level
        self.maze = self.generate_maze(current_level)
        self.player_position = (1, 1)
        self.dest_reached = False
        self.dest_unreached = False

        self.spikes_group = pygame.sprite.Group()
        self.spawn_spikes_timer = pygame.time.get_ticks()
        self.spikes_spawn_interval = 5000  # 5 seconds in milliseconds
        self.spikes_duration = 2000  # 2 seconds in milliseconds

    def generate_spikes(self):
        """
        Generate spikes in empty positions of the maze based on the current level.
        """
        empty_positions = [(x, y) for y, row in enumerate(self.maze) for x, block in enumerate(row) if block == 0]

        # Adjust the number of spikes based on the current level
        if self.level == 1:
            num_spikes = 5
        elif self.level == 2:
            num_spikes = 10
        elif self.level == 3:
            num_spikes = 15
        else:
            num_spikes = 10

        for _ in range(num_spikes):
            x, y = random.choice(empty_positions)
            empty_positions.remove((x, y))
            spike = Spikes(x * 20, (y * 20) + 40, 20)
            self.spikes_group.add(spike)
            self.maze[y][x] = 4


    def update(self, timer):
        """
        Update the maze, including spawning and removing spikes.
        """
        self.brick_size = 20
        super().update()

        current_time = pygame.time.get_ticks()

        # Spawn spikes every 5 seconds
        if current_time - self.spawn_spikes_timer >= self.spikes_spawn_interval:
            spike_sound.play()
            self.generate_spikes()
            self.spawn_spikes_timer = current_time

        # Remove spikes after 2 seconds
        spikes_to_remove = [spike for spike in self.spikes_group if current_time - spike.spawn_time >= self.spikes_duration]
        for spike in spikes_to_remove:
            self.spikes_group.remove(spike)

    def generate_maze(self, current_level):
        """
        Generate the maze layout based on the current level.
        """
        if current_level == 1:
            maze = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
                [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
        elif current_level == 2:
            maze = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
                [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
        elif current_level == 3:
            maze = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
                [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
        return maze
    def render(self, timer):
        """
        Render the maze, spikes, and game information on the screen.
        """
        self.spikes_group.draw(screen)
        maze_height = 22

        brick_size = min(20, 20)

        # Calculate the vertical offset to align the bottom of the maze with the bottom of the screen
        vertical_offset = screen_height - maze_height * brick_size
        x, y = 0, vertical_offset
        for row in self.maze:
            for block in row:
                if block == 1:
                    pygame.draw.rect(screen, (153, 27, 27), (x, y, brick_size, brick_size))
                elif block == 2:
                    end_block_image = pygame.image.load("Images/end_block.jpg").convert()
                    end_block_image = pygame.transform.scale(end_block_image, (brick_size, brick_size))
                    screen.blit(end_block_image, (x, y))
                elif block == 3:
                    character_image = pygame.image.load("Images/character.png").convert()
                    character_image = pygame.transform.scale(character_image, (brick_size, brick_size))
                    screen.blit(character_image, (x, y))
                x += brick_size
            y += brick_size
            x = 0 
        # Display timer at the top right
        timer_font = pygame.font.Font("Fonts/youmurdererbb_reg.ttf", 24)
        timer_text = timer_font.render(f"Time Left: {max(0, timer.time_left)}", True, WHITE)
        timer_rect = timer_text.get_rect(topright=(screen_width - 10, 20))
        screen.blit(timer_text, timer_rect)

        # Display "Graveyard Shift" text at the top center
        title_font = pygame.font.Font("Fonts/youmurdererbb_reg.ttf", 36)
        title_text = title_font.render("Graveyard Shift", True, WHITE)
        title_rect = title_text.get_rect(center=(screen_width // 2, 20))
        screen.blit(title_text, title_rect)

        # Display "escape the horror" text at the top left
        subtitle_font = pygame.font.Font("Fonts/youmurdererbb_reg.ttf", 18)
        subtitle_text = subtitle_font.render("escape the horror", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(topleft=(10, 20))
        screen.blit(subtitle_text, subtitle_rect)

    def move_player(self, direction):
        """
        Move the player in the specified direction within the maze.
        """
        if not self.dest_reached or self.dest_unreached:
            x, y = self.player_position

            if direction in ["left", "right", "up", "down"]:
                move_sound.play()

            if direction == "left" and x - 1 >= 0:
                block = self.maze[y][x - 1]
                if block == 0:
                    self.maze[y][x - 1] = 3
                    self.maze[y][x] = 0
                    self.player_position = (x - 1, y)
                elif block == 2:
                    # Player reached block "2", remove all walls instantly
                    self.remove_walls_instantly()
                    self.dest_reached = True
                elif block == 4:
                    self.remove_walls_instantly()
                    self.dest_unreached = True

            elif direction == "right" and x + 1 < len(self.maze[0]):
                block = self.maze[y][x + 1]
                if block == 0:
                    self.maze[y][x + 1] = 3
                    self.maze[y][x] = 0
                    self.player_position = (x + 1, y)
                elif block == 2:
                    # Player reached block "2", remove all walls instantly
                    self.remove_walls_instantly()
                    self.dest_reached = True
                elif block == 4:
                    self.remove_walls_instantly()                    
                    self.dest_unreached = True      

            elif direction == "up" and y - 1 >= 0:
                block = self.maze[y - 1][x]
                if block == 0:
                    self.maze[y - 1][x] = 3
                    self.maze[y][x] = 0
                    self.player_position = (x, y - 1)
                elif block == 2:
                    # Player reached block "2", remove all walls instantly
                    self.remove_walls_instantly()
                    self.dest_reached = True
                elif block == 4:
                    self.remove_walls_instantly()
                    self.dest_unreached = True      

            elif direction == "down" and y + 1 < len(self.maze):
                block = self.maze[y + 1][x]
                if block == 0:
                    self.maze[y + 1][x] = 3
                    self.maze[y][x] = 0
                    self.player_position = (x, y + 1)
                elif block == 2:
                    # Player reached block "2", remove all walls instantly
                    self.remove_walls_instantly()
                    self.dest_reached = True
                elif block == 4:
                    self.remove_walls_instantly()
                    self.dest_unreached = True       

    def remove_walls_instantly(self):
        """
        Remove all walls in the maze instantly.
        """
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 1:
                    self.maze[i][j] = 0         