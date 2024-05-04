#!/usr/bin/python

import math
import random
import time
import pygame

# initializes pygame(fonts and other things)
pygame.init()

# creates a 800x600 window using pygame
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# set caption
pygame.display.set_caption("Aim Trainer")

# how often a target appears
TARGET_INCREMENT = 475
TARGET_EVENT = pygame.USEREVENT

# padding off the borders
TARGET_PADDING = 30

# background color
BG_COLOR = (0, 25, 40)
LIVES = 3
TOP_BAR_HEIGHT = 50

# specifies the font
LABEL_FONT = pygame.font.SysFont("comicsans", 24)


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    # x and y are locations on screen. self.grow must be true at start, but need to change to false once it reaches MAX_SIZE.
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    # once self.size reaches max_size, turn self.grow to false
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        # if growing, add growth rate to current size
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    # draws a circle to the window(win) with set parameters. need to do it 4 times to make it look smooth
    # in pygame the order you draw things is important. the thing you draw first will be overlapped by the second drawing
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    # checks for center coordinate of mouse vs radius of the circle (distance to point formula)
    def collide(self, x, y):
        dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return dis <= self.size


# fill window with set background color
def draw(win, targets):
    win.fill(BG_COLOR)
    # looks for all targets and draws them all to the screen
    for target in targets:
        target.draw(win)


# formats time in a nice way. math.floor rounds down
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    # formats it so that seconds are 01, 02, 03, 04.. etc vs 1, 2, 3, 4. works only on int type.
    return f"{minutes:02d}:{seconds:02d}:{milli}"


# draws a rectangle to the top left hand corner of window with specified stuff
def draw_top_bar(win, elapsed_time, target_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    # renders font to screen. in pygame this must be done
    speed = round(target_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {target_pressed}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    # blit displays another surface, in this case time_label
    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))


def end_screen(win, elapsed_time, target_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(target_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {target_pressed}", 1, "white")

    accuracy = round(target_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}", 1, "white")

    # prints sh*t in the middle of the screen
    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                run = False
                break


# gets the middle point of screen
def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2


def main():
    run = True
    targets = []
    # clock is to regulate the while loop below
    clock = pygame.time.Clock()

    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    # triggers an TARGET_EVENT every 400ms(TARGET_INCREMENT)
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    # infinite while loop that breaks if ...
    while run:
        # clock.tick regulates the FPS of the while loop. Without it the loop runs as fast as possible. this determines how quickly the target appears and dissappears
        clock.tick(100)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            # generates a target at random location.TARGET_PADDING, WIDTH - TARGET_PADDING must be used so that it does not spawn out of bounds
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING
                )
                target = Target(x, y)
                targets.append(target)

            # this captures clicks and increments by one
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        # updates targets. no clue whats happening
        for target in targets:
            target.update()

            # removes target once it hits size of 0. this if statement needs to be after the for loop above, because when the loop starts the size is 0
            if target.size <= 0:
                targets.remove(target)
                misses += 1

            # asterisk (*) is used to break the tuple to invidiual components. shorthand for (mouse_pos[0], mouse_pos[1])
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed += 1

        if misses >= LIVES:
            end_screen(WIN, elapsed_time, target_pressed, clicks)

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, target_pressed, misses)
        pygame.display.update()
    pygame.quit()


# has something to do with importing files
if __name__ == "__main__":
    main()
