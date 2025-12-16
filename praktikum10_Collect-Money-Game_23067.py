import pygame
import random
import sys

pygame.init()

# Window settings
WIDTH = 500
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect Money Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HEART_RED = (255, 60, 60)
YELLOW = (255, 255, 0)
BUTTON_COLOR = (50, 150, 255)
BUTTON_HOVER = (80, 180, 255)

font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 60)

# LOAD IMAGES
background_img = pygame.image.load("latar.jpeg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

player_img = pygame.image.load("orang.png")
player_img = pygame.transform.scale(player_img, (80, 80))

money_img = pygame.image.load("uang.png")
money_img = pygame.transform.scale(money_img, (60, 60))

knife_img = pygame.image.load("bom.png")
knife_img = pygame.transform.scale(knife_img, (80, 80))

# HEART (LOVE)
def draw_heart(surface, x, y, size):
    top_radius = size // 2
    pygame.draw.circle(surface, HEART_RED, (x + top_radius, y + top_radius), top_radius)
    pygame.draw.circle(surface, HEART_RED, (x + top_radius*3, y + top_radius), top_radius)
    points = [(x, y + top_radius), (x + size*2, y + top_radius), (x + size, y + size*2)]
    pygame.draw.polygon(surface, HEART_RED, points)

# COLLISION
def collide(px, py, sx, sy, size, player_size):
    return (px < sx + size and px + player_size > sx and py < sy + size and py + player_size > sy)

# EXPLOSION EFFECT
def explosion_effect(surface, x, y, size):
    for i in range(10):
        radius = size + i * 4
        alpha = 255 - i * 22  
        temp = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        color = (255, 200 - i * 15, 0, alpha)
        pygame.draw.circle(temp, color, (radius, radius), radius)
        surface.blit(temp, (x - radius + size//2, y - radius + size//2))
        pygame.display.update()
        pygame.time.delay(25)

# GAME OVER MENU
def game_over_menu(score, level):
    while True:
        window.blit(background_img, (0, 0))

        # Title
        text = title_font.render("GAME OVER", True, WHITE)
        window.blit(text, (WIDTH//2 - text.get_width()//2, 150))

        # Score & Level
        score_text = font.render(f"Score: {score}   Level: {level}", True, WHITE)
        window.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 230))

        mx, my = pygame.mouse.get_pos()

        # Buttons
        play_btn = pygame.Rect(WIDTH//2 - 150, 320, 130, 55)
        exit_btn = pygame.Rect(WIDTH//2 + 20, 320, 130, 55)

        # Hover effect
        pygame.draw.rect(window, BUTTON_HOVER if play_btn.collidepoint(mx, my) else BUTTON_COLOR, play_btn)
        pygame.draw.rect(window, BUTTON_HOVER if exit_btn.collidepoint(mx, my) else BUTTON_COLOR, exit_btn)

        play_text = font.render("PLAY AGAIN", True, WHITE)
        exit_text = font.render("EXIT", True, WHITE)

        window.blit(play_text, (play_btn.centerx - play_text.get_width()//2,
                                play_btn.centery - play_text.get_height()//2))

        window.blit(exit_text, (exit_btn.centerx - exit_text.get_width()//2,
                                exit_btn.centery - exit_text.get_height()//2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(mx, my):
                    return "restart"
                if exit_btn.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

# START MENU
def start_menu():
    while True:
        window.blit(background_img, (0, 0))

        title = title_font.render("COLLECT MONEY GAME", True, WHITE)
        window.blit(title, (WIDTH//2 - title.get_width()//2, 150))

        mx, my = pygame.mouse.get_pos()
        button_rect = pygame.Rect(WIDTH//2 - 100, 300, 200, 60)

        pygame.draw.rect(window, BUTTON_HOVER if button_rect.collidepoint(mx, my) else BUTTON_COLOR, button_rect)

        start_text = font.render("START", True, WHITE)
        window.blit(start_text, (button_rect.centerx - start_text.get_width()//2,
                                 button_rect.centery - start_text.get_height()//2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(mx, my):
                    return

# GAME LOOP
def game_loop():

    player_size = 80
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 10
    player_speed = 7

    danger_size = 80
    danger_x = random.randint(0, WIDTH - danger_size)
    danger_y = -danger_size
    danger_speed = 6

    blue_size = 60
    blue_x = random.randint(0, WIDTH - blue_size)
    blue_y = -blue_size
    blue_speed = 5

    score = 0
    lives = 3
    level = 1
    max_level = 20

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        danger_y += danger_speed
        blue_y += blue_speed

        if danger_y > HEIGHT:
            danger_y = -danger_size
            danger_x = random.randint(0, WIDTH - danger_size)

        if blue_y > HEIGHT:
            blue_y = -blue_size
            blue_x = random.randint(0, WIDTH - blue_size)

        if collide(player_x, player_y, blue_x, blue_y, blue_size, player_size):
            score += 1
            blue_y = -blue_size
            blue_x = random.randint(0, WIDTH - blue_size)

            if score % 20 == 0 and level < max_level:
                level += 1
                danger_speed += 0.8
                blue_speed += 0.4

        if collide(player_x, player_y, danger_x, danger_y, danger_size, player_size):
            
            explosion_effect(window, player_x, player_y, player_size)

            lives -= 1
            danger_y = -danger_size
            danger_x = random.randint(0, WIDTH - danger_size)

            if lives <= 0:
                running = False

        # Draw background
        window.blit(background_img, (0, 0))

        # Draw items
        window.blit(player_img, (player_x, player_y))
        window.blit(money_img, (blue_x, blue_y))
        window.blit(knife_img, (danger_x, danger_y))

        score_text = font.render(f"Score: {score}", True, WHITE)
        window.blit(score_text, (10, 10))

        level_text = font.render(f"Level: {level}", True, YELLOW)
        window.blit(level_text, (10, 40))

        heart_x = 10
        for i in range(lives):
            draw_heart(window, heart_x, 80, 13)
            heart_x += 40

        pygame.display.update()

    # Jika game berakhir → tampilkan menu pilihan
    result = game_over_menu(score, level)
    if result == "restart":
        game_loop()

# RUN
start_menu()
game_loop()
pygame.quit()
