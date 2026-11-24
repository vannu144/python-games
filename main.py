import pygame
import random
import json
from sys import exit


pygame.init()
pygame.mixer.init()


# ---------------- WINDOW ----------------

main_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()


# ---------------- SAVE SYSTEM ----------------

SAVE_FILE = "snake_save.json"


def load_data():

    try:

        with open(SAVE_FILE, "r") as file:

            data = json.load(file)

            return data

    except (FileNotFoundError, json.JSONDecodeError):

        return {}


saved_data = load_data()


# ---------------- GAME STATES ----------------

MENU = "menu"
SETTINGS = "settings"
PLAYING = "playing"

game_state = MENU


# ---------------- DIFFICULTY ----------------

speeds = {
    "Easy": 5,
    "Medium": 10,
    "Hard": 15
}


difficulty = saved_data.get("difficulty", "Medium")

if difficulty not in speeds:
    difficulty = "Medium"


# ---------------- VOLUMES ----------------

music_volume = saved_data.get("music_volume", 0.3)
effects_volume = saved_data.get("effects_volume", 0.5)

try:
    music_volume = float(music_volume)
    effects_volume = float(effects_volume)

except (ValueError, TypeError):

    music_volume = 0.3
    effects_volume = 0.5


music_volume = max(0, min(1, music_volume))
effects_volume = max(0, min(1, effects_volume))


# ---------------- HIGH SCORE ----------------

high_score = saved_data.get("high_score", 0)

try:
    high_score = max(0, int(high_score))

except (ValueError, TypeError):
    high_score = 0


def save_data():

    data = {
        "high_score": high_score,
        "difficulty": difficulty,
        "music_volume": music_volume,
        "effects_volume": effects_volume
    }

    try:

        with open(SAVE_FILE, "w") as file:

            json.dump(data, file, indent=4)

    except OSError:

        print("Could not save game data!")


# ---------------- FONTS ----------------

title_font = pygame.font.SysFont("consolas", 65, bold=True)
button_font = pygame.font.SysFont("consolas", 26, bold=True)
small_font = pygame.font.SysFont("consolas", 20, bold=True)
score_font = pygame.font.SysFont("Fixedsys", 30, bold=True)


# ---------------- COLORS ----------------

GREEN = (80, 220, 100)
DARK_GREEN = (20, 90, 45)
LIGHT_GREEN = (120, 240, 130)

RED = (230, 65, 65)

WHITE = (240, 240, 240)
BLACK = (15, 25, 20)

GRAY = (65, 80, 70)
DARK_GRAY = (30, 45, 35)

GOLD = (255, 205, 70)


# ---------------- SOUND SYSTEM ----------------

eat_sound = pygame.mixer.Sound("sounds/eat.wav")
game_over_sound = pygame.mixer.Sound("sounds/game over.wav")
click_sound = pygame.mixer.Sound("sounds/click.wav")

eat_sound.set_volume(effects_volume)
game_over_sound.set_volume(effects_volume)
click_sound.set_volume(effects_volume)


MUSIC_ENDED = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(MUSIC_ENDED)

current_music = "bg-3"


pygame.mixer.music.load("sounds/bg-3.wav")
pygame.mixer.music.set_volume(music_volume)
pygame.mixer.music.play(-1)


# ---------------- MUSIC FUNCTIONS ----------------

def play_menu_music():

    global current_music

    pygame.mixer.music.stop()

    pygame.mixer.music.load("sounds/bg-3.wav")
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)

    current_music = "bg-3"


def play_start_music():

    global current_music

    pygame.mixer.music.stop()

    pygame.mixer.music.load("sounds/start.wav")
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play()

    current_music = "start"


def play_bg2_music():

    global current_music

    pygame.mixer.music.stop()

    pygame.mixer.music.load("sounds/bg-2.wav")
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play()

    current_music = "bg-2"


def play_next_game_music():

    global current_music

    if current_music == "start" or current_music == "bg-1":

        pygame.mixer.music.load("sounds/bg-2.wav")
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play()

        current_music = "bg-2"

    elif current_music == "bg-2":

        pygame.mixer.music.load("sounds/bg-1.wav")
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play()

        current_music = "bg-1"


# ---------------- BUTTONS ----------------

play_button = pygame.Rect(275, 270, 250, 55)
settings_button = pygame.Rect(275, 345, 250, 55)
quit_button = pygame.Rect(275, 420, 250, 55)

easy_button = pygame.Rect(100, 420, 170, 55)
medium_button = pygame.Rect(315, 420, 170, 55)
hard_button = pygame.Rect(530, 420, 170, 55)

back_button = pygame.Rect(275, 510, 250, 55)

game_over_restart_button = pygame.Rect(275, 390, 250, 55)
game_over_menu_button = pygame.Rect(275, 465, 250, 55)


# ---------------- SLIDERS ----------------

music_slider = pygame.Rect(250, 210, 300, 10)
effects_slider = pygame.Rect(250, 290, 300, 10)


def update_music_slider(mouse_x):

    global music_volume

    music_volume = (mouse_x - music_slider.x) / music_slider.width

    if music_volume < 0:
        music_volume = 0

    if music_volume > 1:
        music_volume = 1

    pygame.mixer.music.set_volume(music_volume)

    save_data()


def update_effects_slider(mouse_x):

    global effects_volume

    effects_volume = (mouse_x - effects_slider.x) / effects_slider.width

    if effects_volume < 0:
        effects_volume = 0

    if effects_volume > 1:
        effects_volume = 1

    eat_sound.set_volume(effects_volume)
    game_over_sound.set_volume(effects_volume)
    click_sound.set_volume(effects_volume)

    save_data()


def draw_slider(text, slider_rect, volume):

    label = button_font.render(text, True, WHITE)

    main_display.blit(
        label,
        label.get_rect(center=(400, slider_rect.y - 35))
    )

    pygame.draw.rect(main_display, GRAY, slider_rect)

    knob_x = int(slider_rect.x + volume * slider_rect.width)

    filled_width = knob_x - slider_rect.x

    filled_rect = pygame.Rect(
        slider_rect.x,
        slider_rect.y,
        filled_width,
        slider_rect.height
    )

    pygame.draw.rect(main_display, GREEN, filled_rect)

    pygame.draw.circle(
        main_display,
        LIGHT_GREEN,
        (knob_x, slider_rect.centery),
        12
    )

    percentage = int(volume * 100)

    volume_text = small_font.render(
        str(percentage) + "%",
        True,
        WHITE
    )

    main_display.blit(volume_text, (570, slider_rect.y - 15))


# ---------------- BACKGROUND ----------------

def draw_background():

    main_display.fill(BLACK)

    # Draw subtle grid

    grid_color = (25, 45, 32)

    for x in range(0, 800, 20):

        pygame.draw.line(
            main_display,
            grid_color,
            (x, 0),
            (x, 600)
        )

    for y in range(0, 600, 20):

        pygame.draw.line(
            main_display,
            grid_color,
            (0, y),
            (800, y)
        )

    # Draw outer border

    pygame.draw.rect(
        main_display,
        DARK_GREEN,
        (2, 2, 796, 596),
        4,
        border_radius=8
    )


# ---------------- FOOD ----------------

def draw_food():

    food_x = food[0]
    food_y = food[1]

    # Apple body

    pygame.draw.circle(
        main_display,
        RED,
        (food_x + 10, food_y + 11),
        9
    )

    # Apple leaf

    pygame.draw.ellipse(
        main_display,
        GREEN,
        (food_x + 11, food_y, 9, 6)
    )

    # Small highlight

    pygame.draw.circle(
        main_display,
        (255, 150, 150),
        (food_x + 6, food_y + 8),
        2
    )


# ---------------- SNAKE ----------------

snake_body = [
    [100, 100],
    [80, 100],
    [60, 100]
]

direction = (20, 0)


def draw_snake():

    for index, segment in enumerate(snake_body):

        x = segment[0]
        y = segment[1]

        if index == 0:

            color = LIGHT_GREEN

        else:

            color = GREEN

        pygame.draw.rect(
            main_display,
            color,
            (x, y, 20, 20),
            border_radius=6
        )

    # Draw eyes on the head

    head_x = snake_body[0][0]
    head_y = snake_body[0][1]

    eye_one = (head_x + 6, head_y + 6)
    eye_two = (head_x + 14, head_y + 6)

    if direction == (20, 0):

        eye_one = (head_x + 14, head_y + 6)
        eye_two = (head_x + 14, head_y + 14)

    elif direction == (-20, 0):

        eye_one = (head_x + 6, head_y + 6)
        eye_two = (head_x + 6, head_y + 14)

    elif direction == (0, -20):

        eye_one = (head_x + 6, head_y + 6)
        eye_two = (head_x + 14, head_y + 6)

    elif direction == (0, 20):

        eye_one = (head_x + 6, head_y + 14)
        eye_two = (head_x + 14, head_y + 14)

    pygame.draw.circle(
        main_display,
        BLACK,
        eye_one,
        2
    )

    pygame.draw.circle(
        main_display,
        BLACK,
        eye_two,
        2
    )


# ---------------- FOOD GENERATION ----------------

def generate_food():

    while True:

        new_food = [
            random.randrange(0, 800, 20),
            random.randrange(0, 600, 20)
        ]

        if new_food not in snake_body:

            return new_food


food = generate_food()


# ---------------- SCORE ----------------

score = 0
game_over = False


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
        rect,
        border_radius=10
    )

    pygame.draw.rect(
        main_display,
        GREEN,
        rect,
        2,
        border_radius=10
    )

    text_surface = button_font.render(
        text,
        True,
        WHITE
    )

    text_rect = text_surface.get_rect(center=rect.center)

    main_display.blit(text_surface, text_rect)


# ---------------- MAIN MENU ----------------

def main_menu():

    draw_background()

    title = title_font.render(
        "SNAKE GAME",
        True,
        LIGHT_GREEN
    )

    main_display.blit(
        title,
        title.get_rect(center=(400, 150))
    )

    best_text = small_font.render(
        "BEST SCORE: " + str(high_score),
        True,
        GOLD
    )

    main_display.blit(
        best_text,
        best_text.get_rect(center=(400, 215))
    )

    draw_button("PLAY", play_button)
    draw_button("SETTINGS", settings_button)
    draw_button("QUIT", quit_button)


# ---------------- SETTINGS MENU ----------------

def settings_menu():

    draw_background()

    title = title_font.render(
        "SETTINGS",
        True,
        LIGHT_GREEN
    )

    main_display.blit(
        title,
        title.get_rect(center=(400, 90))
    )

    draw_slider(
        "MUSIC VOLUME",
        music_slider,
        music_volume
    )

    draw_slider(
        "SOUND EFFECTS",
        effects_slider,
        effects_volume
    )

    difficulty_text = button_font.render(
        "DIFFICULTY: " + difficulty,
        True,
        WHITE
    )

    main_display.blit(
        difficulty_text,
        difficulty_text.get_rect(center=(400, 365))
    )

    draw_button("EASY", easy_button)
    draw_button("MEDIUM", medium_button)
    draw_button("HARD", hard_button)
    draw_button("BACK", back_button)


# ---------------- GAME OVER SCREEN ----------------

def game_over_screen():

    # Dark overlay

    overlay = pygame.Surface((800, 600))

    overlay.set_alpha(190)

    overlay.fill(BLACK)

    main_display.blit(overlay, (0, 0))

    # Main panel

    panel = pygame.Rect(150, 110, 500, 430)

    pygame.draw.rect(
        main_display,
        DARK_GRAY,
        panel,
        border_radius=20
    )

    pygame.draw.rect(
        main_display,
        DARK_GREEN,
        panel,
        4,
        border_radius=20
    )

    # Title

    title = title_font.render(
        "GAME OVER",
        True,
        RED
    )

    main_display.blit(
        title,
        title.get_rect(center=(400, 180))
    )

    # Current score

    score_text = button_font.render(
        "SCORE: " + str(score),
        True,
        WHITE
    )

    main_display.blit(
        score_text,
        score_text.get_rect(center=(400, 265))
    )

    # High score

    best_text = button_font.render(
        "BEST: " + str(high_score),
        True,
        GOLD
    )

    main_display.blit(
        best_text,
        best_text.get_rect(center=(400, 315))
    )

    # Buttons

    draw_button(
        "PLAY AGAIN",
        game_over_restart_button
    )

    draw_button(
        "MAIN MENU",
        game_over_menu_button
    )


# ---------------- GAME LOOP ----------------

running = True

last_move_time = pygame.time.get_ticks()


while running:

    # ---------------- EVENTS ----------------

    for event in pygame.event.get():

        # Music transitions

        if event.type == MUSIC_ENDED:

            if game_state == PLAYING and not game_over:

                play_next_game_music()

        # Quit

        if event.type == pygame.QUIT:

            save_data()

            running = False

        # Mouse clicks

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                # SETTINGS

                if game_state == SETTINGS:

                    if music_slider.inflate(0, 25).collidepoint(event.pos):

                        update_music_slider(event.pos[0])

                    elif effects_slider.inflate(0, 25).collidepoint(event.pos):

                        update_effects_slider(event.pos[0])

                    elif easy_button.collidepoint(event.pos):

                        click_sound.play()

                        difficulty = "Easy"

                        save_data()

                    elif medium_button.collidepoint(event.pos):

                        click_sound.play()

                        difficulty = "Medium"

                        save_data()

                    elif hard_button.collidepoint(event.pos):

                        click_sound.play()

                        difficulty = "Hard"

                        save_data()

                    elif back_button.collidepoint(event.pos):

                        click_sound.play()

                        game_state = MENU

                # MAIN MENU

                elif game_state == MENU:

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

                        save_data()

                        running = False

                # GAME OVER

                elif game_state == PLAYING and game_over:

                    if game_over_restart_button.collidepoint(event.pos):

                        click_sound.play()

                        restart_game()

                        last_move_time = pygame.time.get_ticks()

                        play_start_music()

                    elif game_over_menu_button.collidepoint(event.pos):

                        click_sound.play()

                        game_over = False

                        game_state = MENU

                        play_menu_music()

        # Slider dragging

        if event.type == pygame.MOUSEMOTION:

            if game_state == SETTINGS:

                if event.buttons[0]:

                    if music_slider.inflate(0, 25).collidepoint(event.pos):

                        update_music_slider(event.pos[0])

                    elif effects_slider.inflate(0, 25).collidepoint(event.pos):

                        update_effects_slider(event.pos[0])

        # Keyboard

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

                        game_over = False

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

                        # Update high score

                        if score > high_score:

                            high_score = score

                            save_data()

                        food = generate_food()

                    else:

                        snake_body.pop()

        # Draw background

        draw_background()

        # Draw snake

        draw_snake()

        # Draw food

        draw_food()

        # Draw score

        score_text = score_font.render(
            "SCORE: " + str(score),
            True,
            WHITE
        )

        main_display.blit(score_text, (20, 15))

        # Draw best score

        best_text = small_font.render(
            "BEST: " + str(high_score),
            True,
            GOLD
        )

        main_display.blit(best_text, (650, 20))

        # Game Over

        if game_over:

            game_over_screen()

    # ---------------- UPDATE DISPLAY ----------------

    pygame.display.flip()

    clock.tick(60)


# ---------------- EXIT ----------------

save_data()

pygame.quit()

exit()