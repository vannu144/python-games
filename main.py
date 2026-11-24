import pygame
import random
from sys import exit

pygame.init()

# Game window

main_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Colours

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)

# Snake body

snake_body = [
    [100, 100],
    [80, 100],
    [60, 100]
]

# Initial direction

direction = (20, 0)

# Generate food

def generate_food():
    while True:
        food = [
            random.randrange(0, 800, 20),
            random.randrange(0, 600, 20)
        ]

        if food not in snake_body:
            return food


food = generate_food()
score = 0

running = True
game_over = False

def restart_game():
    global snake_body, direction, food, score, game_over

    snake_body = [
        [100, 100],
        [80, 100],
        [60, 100]
    ]

    direction = (20, 0)
    food = generate_food()
    score = 0
    game_over = False

while running:

    # Event handling

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Keyboard controls

        if event.type == pygame.KEYDOWN:
            
            if game_over and event.key == pygame.K_r:
                restart_game()

            elif (event.key in (pygame.K_UP, pygame.K_w)
                    and direction != (0, 20)):
                direction = (0, -20)

            elif (event.key in (pygame.K_DOWN, pygame.K_s)
                    and direction != (0, -20)):
                direction = (0, 20)

            elif (event.key in (pygame.K_LEFT, pygame.K_a)
                    and direction != (20, 0)):
                direction = (-20, 0)

            elif (event.key in (pygame.K_RIGHT, pygame.K_d)
                    and direction != (-20, 0)):
                direction = (20, 0)

    if not game_over:

        # Calculate new head

        head_x = (snake_body[0][0] + direction[0]) % 800
        head_y = (snake_body[0][1] + direction[1]) % 600

        new_head = [head_x, head_y]

        # Check if food is eaten

        ate_food = new_head == food

        # Self collision detection

        if new_head in (snake_body if ate_food else snake_body[:-1]):
            game_over = True

        else:

            # Move snake

            snake_body.insert(0, new_head)

            if ate_food:
                score += 1
                food = generate_food()

            else:
                snake_body.pop()

    # Background

    main_display.fill(BLACK)

    # Draw snake

    for segment in snake_body:
        pygame.draw.rect(
            main_display,
            GREEN,
            pygame.Rect(segment[0], segment[1], 20, 20)
        )

    # Draw food

    pygame.draw.rect(
        main_display,
        RED,
        pygame.Rect(food[0], food[1], 20, 20)
    )

    # Display score

    font = pygame.font.SysFont("Fixedsys", 30, bold=True)
    score_text = font.render(f"Score: {score}", True, WHITE)
    main_display.blit(score_text, (10, 10))

    # Game over screen

    if game_over:
        font = pygame.font.Font(None, 60)
        text = font.render("GAME OVER", True, RED)

        text_rect = text.get_rect(center=(400, 300))
        main_display.blit(text, text_rect)
        
        # Restart instruction

        small_font = pygame.font.SysFont("consolas", 30, bold=True)
        restart_text = small_font.render("Press R to Restart", True, WHITE)

        restart_rect = restart_text.get_rect(center=(400, 330))
        main_display.blit(restart_text, restart_rect)

    pygame.display.flip()

    clock.tick(5)

pygame.quit()
exit()