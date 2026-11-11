import pygame
import random
import sys


# SETTINGS

WIDTH = 800
HEIGHT = 500
FPS = 60

PLAYER_SPEED = 4


# INIT

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hokejists - Sasniedz Vārtus!")

clock = pygame.time.Clock()

# LOAD IMAGES

player_img = pygame.image.load("hokejists.png").convert_alpha()
goal_img = pygame.image.load("varti.png").convert_alpha()
obstacle_img = pygame.image.load("asvhokejists.png").convert_alpha()

player_img = pygame.transform.scale(player_img, (90, 90))
goal_img = pygame.transform.scale(goal_img, (150, 140))
obstacle_img = pygame.transform.scale(obstacle_img, (100, 100))


# COLORS

WHITE = (255, 255, 255)
RED = (180, 0, 0)
DARK = (20, 20, 20)
ICE = (220, 240, 255)


# PLAYER

player = pygame.Rect(50, HEIGHT // 2, 60, 60)


# GOAL

goal = pygame.Rect(WIDTH - 220, HEIGHT // 2 - 70, 180, 140)


# FONT

font = pygame.font.SysFont("Arial", 30)


# GAME VARIABLES

start_ticks = pygame.time.get_ticks()

running = True
won = False
seconds = 0

# pēdējo 10 spēļu laiki
game_times = []


# CREATE OBSTACLES

def create_obstacles():

    obstacles = []

    while len(obstacles) < 5:

        new_rect = pygame.Rect(
            random.randint(200, WIDTH - 300),
            random.randint(50, HEIGHT - 100),
            60,
            60
        )

        collision = False

        # Nepārklājas ar citiem
        for obstacle in obstacles:

            if new_rect.colliderect(obstacle["rect"]):
                collision = True

        # Netuvu playerim
        if new_rect.colliderect(player.inflate(200, 200)):
            collision = True

        # Netuvu vārtiem
        if new_rect.colliderect(goal.inflate(150, 150)):
            collision = True

        if not collision:

            obstacles.append({
                "rect": new_rect
            })

    return obstacles


# INITIAL OBSTACLES

obstacles = create_obstacles()


# RESET PLAYER

def reset_player():

    valid_position = False

    while not valid_position:

        random_x = random.randint(20, 120)
        random_y = random.randint(50, HEIGHT - 100)

        player.x = random_x
        player.y = random_y

        valid_position = True

        # Nepārklājas ar obstacles
        for obstacle in obstacles:

            if player.colliderect(obstacle["rect"]):
                valid_position = False


# RESTART GAME

def restart_game():

    global won
    global start_ticks
    global obstacles
    global seconds

    # Saglabā iepriekšējo laiku
    game_times.append(seconds)

    # Tikai pēdējās 10 spēles
    if len(game_times) > 10:
        game_times.pop(0)

    won = False

    # Jauns laiks
    seconds = 0
    start_ticks = pygame.time.get_ticks()

    # Jauns obstacle izkārtojums
    obstacles = create_obstacles()

    # Jauna spawn vieta
    reset_player()

# sākuma spawn
reset_player()


# MAIN LOOP

while running:

    clock.tick(FPS)


    # EVENTS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

   
    # MOVEMENT

    if not won:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            player.y -= PLAYER_SPEED

        if keys[pygame.K_s]:
            player.y += PLAYER_SPEED

        if keys[pygame.K_a]:
            player.x -= PLAYER_SPEED

        if keys[pygame.K_d]:
            player.x += PLAYER_SPEED

   
    # SCREEN LIMITS
    
    if player.left < 0:
        player.left = 0

    if player.right > WIDTH:
        player.right = WIDTH

    if player.top < 0:
        player.top = 0

    if player.bottom > HEIGHT:
        player.bottom = HEIGHT


    # COLLISION

    for obstacle in obstacles:

        if player.colliderect(obstacle["rect"]):
            reset_player()

  
    # WIN CONDITION

    if player.colliderect(goal):
        won = True


    # TIMER
  
    # Laiks apstājas pie uzvaras
    if not won:

        seconds = (
            pygame.time.get_ticks() - start_ticks
        ) // 1000

   
    # DRAW
   
    screen.fill(ICE)

    # Ledus līnija
    pygame.draw.line(
        screen,
        RED,
        (WIDTH // 2, 0),
        (WIDTH // 2, HEIGHT),
        5
    )

    # Obstacles
    for obstacle in obstacles:

        screen.blit(
            obstacle_img,
            (obstacle["rect"].x, obstacle["rect"].y)
        )

    # Goal
    screen.blit(goal_img, (goal.x, goal.y))

    # Player
    screen.blit(player_img, (player.x, player.y))

  
    # TIMER TEXT
    
    timer_text = font.render(
        f"Laiks: {seconds}s",
        True,
        DARK
    )

    screen.blit(timer_text, (20, 20))


    # AVERAGE TIME
   
    if len(game_times) > 0:

        average_time = sum(game_times) / len(game_times)

        avg_text = font.render(
            f"Average (10): {average_time:.1f}s",
            True,
            DARK
        )

        screen.blit(avg_text, (20, 60))


    # WIN SCREEN
  
    if won:

        # Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        screen.blit(overlay, (0, 0))

        # Win text
        win_font = pygame.font.SysFont("Arial", 60)

        text = win_font.render(
            f"UZVARA! Laiks: {seconds}s",
            True,
            WHITE
        )

        screen.blit(text, (220, 220))

        # Button
        button_rect = pygame.Rect(
            380,
            350,
            240,
            80
        )

        pygame.draw.rect(
            screen,
            RED,
            button_rect,
            border_radius=20
        )

        # Button text
        button_font = pygame.font.SysFont("Arial", 40)

        button_text = button_font.render(
            "Atkārtot",
            True,
            WHITE
        )

        screen.blit(button_text, (420, 370))

        # Mouse click
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if button_rect.collidepoint(mouse):

            if click[0] == 1:
                restart_game()

    pygame.display.update()

pygame.quit()
sys.exit()