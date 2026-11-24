import pygame
import random
from sys import exit

pygame.init()
pygame.mixer.init()

# ---------------- WINDOW ----------------

main_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()


# ---------------- SOUND SYSTEM ----------------

# Sound effects

eat_sound = pygame.mixer.Sound("sounds/eat.wav")
game_over_sound = pygame.mixer.Sound("sounds/game over.wav")
click_sound = pygame.mixer.Sound("sounds/click.wav")

# Music ended event

MUSIC_ENDED = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(MUSIC_ENDED)

# Keep track of the currently playing music

current_music = "bg-3"


# Start menu music immediately

pygame.mixer.music.load("sounds/bg-3.wav")
pygame.mixer.music.play(-1)


# ---------------- MUSIC FUNCTIONS ----------------

def play_menu_music():

    global current_music

    pygame.mixer.music.stop()

    pygame.mixer.music.load("sounds/bg-3.wav")
    pygame.mixer.music.play(-1)

    current_music = "bg-3"


def play_start_music():

    global current_music

    pygame.mixer.music.stop()

    pygame.mixer.music.load("sounds/start.wav")
    pygame.mixer.music.play()

    current_music = "start"


def play_bg2_music():

    global current_music

    pygame.mixer.music.stop()

    pygame.mixer.music.load("sounds/bg-2.wav")
    pygame.mixer.music.play()

    current_music = "bg-2"


def play_next_game_music():

    global current_music

    # If start or bg-1 finishes, play bg-2

    if current_music == "start" or current_music == "bg-1":

        pygame.mixer.music.load("sounds/bg-2.wav")
        pygame.mixer.music.play()

        current_music = "bg-2"

    # If bg-2 finishes, play bg-1

    elif current_music == "bg-2":

        pygame.mixer.music.load("sounds/bg-1.wav")
        pygame.mixer.music.play()

        current_music = "bg-1"


# ---------------- GAME STATES ----------------

MENU = "menu"
SETTINGS = "settings"
PLAYING = "playing"

game_state = MENU


# ---------------- DIFFICULTY ----------------

difficulty = "Medium"

speeds = {
    "Easy": 5,
    "Medium": 10,
    "Hard": 15
}


# ---------------- FONTS ----------------

title_font = pygame.font.SysFont("consolas", 65, bold=True)
button_font = pygame.font.SysFont("consolas", 30, bold=True)
small_font = pygame.font.SysFont("consolas", 22, bold=True)
score_font = pygame.font.SysFont("Fixedsys", 30, bold=True)


# ---------------- COLORS ----------------

GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (100, 100, 100)


# ---------------- BUTTONS ----------------

play_button = pygame.Rect(275, 250, 250, 60)
settings_button = pygame.Rect(275, 330, 250, 60)
quit_button = pygame.Rect(275, 410, 250, 60)

easy_button = pygame.Rect(100, 330, 170, 55)
medium_button = pygame.Rect(315, 330, 170, 55)
hard_button = pygame.Rect(530, 330, 170, 55)
back_button = pygame.Rect(275, 440, 250, 60)


# ---------------- SNAKE ----------------

snake_body = [
    [100, 100],
    [80, 100],
    [60, 100]
]

direction = (20, 0)

score = 0
game_over = False


# ---------------- FOOD ----------------

def generate_food():

    while True:

        food = [
            random.randrange(0, 800, 20),
            random.randrange(0, 600, 20)
        ]

        if food not in snake_body:
            return food


food = generate_food()


# ---------------- RESTART ----------------

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


# ---------------- BUTTON FUNCTION ----------------

def draw_button(text, rect):

    mouse = pygame.mouse.get_pos()

    if rect.collidepoint(mouse):
        color = DARK_GREEN
    else:
        color = GRAY

    pygame.draw.rect(
        main_display,
        color,
        rect
    )

    text_surface = button_font.render(text, True, WHITE)

    text_rect = text_surface.get_rect(center=rect.center)

    main_display.blit(text_surface, text_rect)


# ---------------- MAIN MENU ----------------

def main_menu():

    main_display.fill(BLACK)

    title = title_font.render("SNAKE GAME", True, GREEN)

    main_display.blit(
        title,
        title.get_rect(center=(400, 150))
    )

    draw_button("PLAY", play_button)
    draw_button("SETTINGS", settings_button)
    draw_button("QUIT", quit_button)


# ---------------- SETTINGS MENU ----------------

def settings_menu():

    main_display.fill(BLACK)

    title = title_font.render("SETTINGS", True, GREEN)

    main_display.blit(
        title,
        title.get_rect(center=(400, 120))
    )

    difficulty_text = button_font.render(
        "DIFFICULTY: " + difficulty,
        True,
        WHITE
    )

    main_display.blit(
        difficulty_text,
        difficulty_text.get_rect(center=(400, 250))
    )

    draw_button("EASY", easy_button)
    draw_button("MEDIUM", medium_button)
    draw_button("HARD", hard_button)
    draw_button("BACK", back_button)


# ---------------- GAME LOOP ----------------

running = True

last_move_time = pygame.time.get_ticks()

while running:

    # ---------------- EVENTS ----------------

    for event in pygame.event.get():

        # Music transition event

        if event.type == MUSIC_ENDED:

            if game_state == PLAYING and not game_over:

                play_next_game_music()

        # Quit game

        if event.type == pygame.QUIT:

            running = False

        # Mouse clicks

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                # MAIN MENU

                if game_state == MENU:

                    if play_button.collidepoint(event.pos):

                        click_sound.play()

                        restart_game()

                        game_state = PLAYING

                        last_move_time = pygame.time.get_ticks()

                        play_start_music()

                    elif settings_button.collidepoint(event.pos):

                        click_sound.play()

                        game_state = SETTINGS

                    elif quit_button.collidepoint(event.pos):

                        click_sound.play()

                        running = False

                # SETTINGS

                elif game_state == SETTINGS:

                    if easy_button.collidepoint(event.pos):

                        click_sound.play()

                        difficulty = "Easy"

                    elif medium_button.collidepoint(event.pos):

                        click_sound.play()

                        difficulty = "Medium"

                    elif hard_button.collidepoint(event.pos):

                        click_sound.play()

                        difficulty = "Hard"

                    elif back_button.collidepoint(event.pos):

                        click_sound.play()

                        game_state = MENU

        # KEYBOARD EVENTS

        if event.type == pygame.KEYDOWN:

            if game_state == SETTINGS:

                if event.key == pygame.K_ESCAPE:

                    game_state = MENU

            elif game_state == PLAYING:

                if game_over:

                    if event.key == pygame.K_r:

                        restart_game()

                        last_move_time = pygame.time.get_ticks()

                        play_bg2_music()

                    elif event.key == pygame.K_m:

                        game_state = MENU

                        play_menu_music()

                else:

                    if (event.key in (pygame.K_UP, pygame.K_w)
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

    # ---------------- MENU DISPLAY ----------------

    if game_state == MENU:

        main_menu()

    elif game_state == SETTINGS:

        settings_menu()

    # ---------------- GAMEPLAY ----------------

    elif game_state == PLAYING:

        if not game_over:

            current_time = pygame.time.get_ticks()

            if current_time - last_move_time >= 1000 / speeds[difficulty]:

                last_move_time = current_time

                # Calculate new head

                head_x = (snake_body[0][0] + direction[0]) % 800
                head_y = (snake_body[0][1] + direction[1]) % 600

                new_head = [head_x, head_y]

                # Check food

                ate_food = new_head == food

                # Collision detection

                if ate_food:

                    body_to_check = snake_body

                else:

                    body_to_check = snake_body[:-1]

                if new_head in body_to_check:

                    game_over = True

                    pygame.mixer.music.stop()

                    game_over_sound.play()

                else:

                    snake_body.insert(0, new_head)

                    if ate_food:

                        eat_sound.play()

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

        # Score

        score_text = score_font.render(
            f"Score: {score}", True, WHITE
        )

        main_display.blit(score_text, (10, 10))

        # Game over

        if game_over:

            text = title_font.render("GAME OVER", True, RED)

            main_display.blit(
                text,
                text.get_rect(center=(400, 250))
            )

            restart_text = small_font.render(
                "Press R to Restart", True, WHITE
            )

            main_display.blit(
                restart_text,
                restart_text.get_rect(center=(400, 320))
            )

            menu_text = small_font.render(
                "Press M for Main Menu", True, WHITE
            )

            main_display.blit(
                menu_text,
                menu_text.get_rect(center=(400, 360))
            )

    # ---------------- UPDATE DISPLAY ----------------

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
exit()