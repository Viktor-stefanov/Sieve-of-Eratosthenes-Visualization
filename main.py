import pygame
import sys
from algorithm import sieve
import os

pygame.init()

clock = pygame.time.Clock()

numbers_font = pygame.font.SysFont("ComicSansMS", 25)
big_font = pygame.font.SysFont("Comic Sans MS", 60)
medium_font = pygame.font.SysFont("Comic Sans MS", 45)
small_font = pygame.font.SysFont("Comic Sans MS", 40)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (211, 211, 211)
HOVERED_COLOR = (146, 185, 247)
CHOSEN_COLOR = (255, 199, 204)
LIGHT_GREEN = (182, 245, 66)
LIGHT_RED = (255, 122, 122)
CURRENT_NUMBER_COLOR = (211, 222, 151)

def setup():
    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Sieve of Eratosthenes")
    s_width, s_height = pygame.display.get_surface().get_size()

    return win, s_width, s_height

def blit_text(win, s_width, s_height, hovered_colors, chosen_color_idx):
    script_path = os.path.dirname(__file__) # <-- absolute dir the script is in
    grey_path = script_path + r"\img\grey_info.png"
    green_path = script_path + r"\img\green_info.png"
    red_path = script_path + r"\img\red_info.png"

    grey_square = pygame.image.load(grey_path)
    green_square = pygame.image.load(green_path)
    red_square = pygame.image.load(red_path)

    win.blit(grey_square, (s_width * 0.000001, s_height // 2))
    win.blit(green_square, (s_width // 2.9, s_height // 1.95))
    win.blit(red_square, (s_width // 1.55, s_height // 2))
    # below are the colors of the text currently hovered over
    if hovered_colors is None:
        hovered_colors = [WHITE, WHITE, WHITE]
    if chosen_color_idx is not None:
        hovered_colors[chosen_color_idx] = CHOSEN_COLOR

    sieve_text = big_font.render("Sieve of Eratosthenes", False, WHITE)
    sieve_shadow = big_font.render("Sieve of Eratosthenes", False, GREY)

    choose_size = medium_font.render("Choose number size:", False, WHITE)
    small_txt = small_font.render("small", False, hovered_colors[0])
    medium_txt = small_font.render("medium", False, hovered_colors[1])
    big_txt = small_font.render("big", False, hovered_colors[2])

    main_text_pos = (s_width // 3.5, s_height // 8)
    win.blit(sieve_shadow, (main_text_pos[0] + 2, main_text_pos[1] + 2))
    win.blit(sieve_text, main_text_pos)

    choose_text_position = (s_width // 3, s_height // 3.5)
    win.blit(choose_size, choose_text_position)

    sp = (s_width // 3, s_height // 2.8)
    s = win.blit(small_txt, sp)
    mp = (s_width // 2.3, s_height // 2.8)
    m = win.blit(medium_txt, mp)
    lp = (s_width // 1.8, s_height // 2.8)
    l = win.blit(big_txt, lp)

    return (s, m, l)

def menu(win, screen_width, screen_height):
    hovered_colors = None
    chosen_color_idx = None
    while True:
        win.fill(BLACK)
        rects = blit_text(win, screen_width, screen_height, hovered_colors, chosen_color_idx)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit(), sys.exit()
                elif event.key == pygame.K_LEFT:
                    if chosen_color_idx is not None:
                        chosen_color_idx -= 1 if chosen_color_idx > 0 else 0
                elif event.key == pygame.K_RIGHT:
                    if chosen_color_idx is not None:
                        chosen_color_idx += 1 if chosen_color_idx < 2 else 0
                elif event.key == pygame.K_RETURN:
                    if chosen_color_idx is not None:
                        # return small, medium or large size number
                        return [50, 100, 200][chosen_color_idx]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_over_text = [rect.collidepoint(mouse_pos) for rect in rects]
                    if 1 in mouse_over_text:
                        idx = mouse_over_text.index(1)
                        chosen_color_idx = idx

        # create a hover graphic
        mouse_hover = [rect.collidepoint(mouse_pos) for rect in rects]
        if 1 in mouse_hover:
            idx = mouse_hover.index(1)
            hovered_colors = [WHITE if i != idx else HOVERED_COLOR for i in range(3)]
        else:
            hovered_colors = [WHITE, WHITE, WHITE]

        pygame.display.update()

def run_algorithm(win, size, s_width, s_height):
    columns = [int(size / (size / 10) + i) for i in range(100) if size % (size / 10) - i == 0][-1]
    rows = int(size / columns)
    square_width = int((s_width - 15) / columns)
    square_height = int((s_height - 15) / rows)

    fps = 3
    finished = False
    algorithm_steps = None
    current_number = None
    animate = True
    while True:
        win.fill(BLACK)
        # if the algorithm is running create the square_color of the squares - red for the non-primes and green for the primes
        if algorithm_steps is not None and not finished:
            try:
                current_step, current_number = next(algorithm_steps)
            except StopIteration:
                finished = True
                current_number = float("inf")
        number = 1
        for y in range(rows):
            for x in range(columns):
                text_color = WHITE
                square_color = GREY
                if algorithm_steps is not None:
                    square_color = current_step[number]
                    if square_color is True:
                        square_color = LIGHT_GREEN
                        text_color = BLACK
                    else:
                        square_color = LIGHT_RED

                # if the number being drawn right now is the number we are using as a factor of the number size then square_color it differently and draw a circle around the number
                if number == current_number:
                    square_color = CURRENT_NUMBER_COLOR
                    radius = 30
                    circle_pos = (x * square_width + 22 + square_width // 2.45, y * square_height + square_height // 1.85)
                    if size == 100:
                        circle_pos = (x * square_width + 22 + square_width // 2.45, y * square_height + square_height // 1.45)
                    elif size == 200:
                        circle_pos = (x * square_width + 22 + square_width // 2.45, y * square_height + square_height // 1.3)
                        radius = 20
                    pygame.draw.circle(win, BLACK, circle_pos, radius, 5)

                # hard code the position of the biggest number choice - 200 !(by making it work right the other 2 numbers break)!
                middle_number_pos = [x * square_width + 15 + square_width // 2.45, y * square_height + 15 + square_height // 2.65]
                if size == 200:
                    middle_number_pos[1] = y * square_height + 15 + square_height // 10

                rect = (x * square_width + 15, y * square_height + 15, square_width - 6, square_height - 6)
                pygame.draw.rect(win, square_color, rect)
                win.blit(numbers_font.render(str(number), False, text_color), middle_number_pos)

                number += 1
                if animate is True:
                    animation_speed = size // 3
                    clock.tick(animation_speed)
                    pygame.display.update()
                if number-1 == size:
                    animate = False

        if algorithm_steps is not None:
            clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit(), sys.exit()
                elif event.key == pygame.K_RETURN:
                    algorithm_steps = sieve(size + 1)
                elif event.key == pygame.K_r:
                    algorithm_steps = sieve(size + 1)
                    finished = False
                elif event.key == pygame.K_m:
                    main()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    fps += 2
                elif event.button == 5:
                    fps -= 2 if fps >= 3 else 0

        pygame.display.update()

def main():
    win, s_width, s_height = setup()
    size = menu(win, s_width, s_height)
    run_algorithm(win, size, s_width, s_height)

if __name__ == "__main__":
    main()