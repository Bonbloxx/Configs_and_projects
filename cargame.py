#!/usr/bin/python

import pygame
import random
import time
from sys import exit

pygame.init()

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Racegame")
clock = pygame.time.Clock()
speed = [0, 5]
test_font = pygame.font.Font("pixelfont.ttf", 28)
test_font2 = pygame.font.Font("pixelfont.ttf", 23)

car = pygame.image.load("car75.png").convert_alpha()
asteroid = pygame.image.load("asteroidnew75.png").convert_alpha()
background = pygame.image.load("background2.png").convert_alpha()

height = 650
asteroid_height = -100

random_width = random.randint(150, 550)
random_width2 = random.randint(150, 550)
aa = random.randint(150, 550)
ab = random.randint(150, 550)
ac = random.randint(150, 550)
ad = random.randint(150, 550)
ae = random.randint(150, 550)
af = random.randint(150, 550)
ag = random.randint(150, 550)

car_rect = car.get_rect(midbottom=(random_width, height))
asteroid_rect = asteroid.get_rect(midtop=(random_width2, asteroid_height))
danger = asteroid.get_rect(midtop=(aa, asteroid_height))
danger1 = asteroid.get_rect(midtop=(ab, asteroid_height))
danger2 = asteroid.get_rect(midtop=(ac, asteroid_height))
danger3 = asteroid.get_rect(midtop=(ad, asteroid_height))
danger4 = asteroid.get_rect(midtop=(ae, asteroid_height))
danger5 = asteroid.get_rect(midtop=(af, asteroid_height))
danger6 = asteroid.get_rect(midtop=(ag, asteroid_height))

points = 0


def spawn_asteroids():
    screen.blit(asteroid, asteroid_rect)
    global points
    if asteroid_rect.y > 850:
        asteroid_rect.y = -50
        asteroid_rect.x = random.randint(-60, 900)
        points += 1

    if points >= 2:
        screen.blit(asteroid, danger)
        danger.y += random.randint(3, 6)
    if danger.y > 850:
        danger.y = -60
        danger.x = random.randint(-60, 900)
        points += 1

    if points >= 5:
        screen.blit(asteroid, danger1)
        danger1.y += random.randint(3, 7)
        danger1.x += 2
    if danger1.y > 850:
        danger1.y = -200
        danger1.x = random.randint(-60, 900)
        points += 1

    if points >= 8:
        screen.blit(asteroid, danger2)
        danger2.y += random.randint(4, 8)
        danger2.x -= 2
    if danger2.y > 850:
        danger2.y = -350
        danger2.x = random.randint(-60, 900)
        points += 1

    if points >= 15:
        screen.blit(asteroid, danger3)
        danger3.y += random.randint(4, 9)
    if danger3.y > 850:
        danger3.y = -400
        danger3.x = random.randint(-60, 900)
        points += 1

    if points >= 28:
        screen.blit(asteroid, danger4)
        danger4.y += random.randint(5, 8)
        danger4.x += 5
    if danger4.y > 850:
        danger4.y = -450
        danger4.x = random.randint(-60, 900)
        points += 1

    if points >= 45:
        screen.blit(asteroid, danger5)
        danger5.y += random.randint(5, 9)
    if danger5.y > 850:
        danger5.y = -500
        danger5.x = random.randint(-60, 900)
        points += 1

    if points >= 70:
        screen.blit(asteroid, danger6)
        danger6.y += random.randint(5, 10)
    if danger6.y > 850:
        danger6.y = -600
        danger6.x = random.randint(-60, 900)
        points += 1


def score():
    target_label = test_font.render(f"Asteroids dodged: {points}", False, "green")
    text_rect = target_label.get_rect(midtop=(500, 10))
    screen.blit(target_label, text_rect)


def game_end():
    screen.fill("Black")
    global points
    end_label = test_font.render(
        (f"Crashed! Your total points are: {points}"), False, "green"
    )
    end_label2 = test_font2.render(
        ("Press y to play again or x to exit"), False, "green"
    )
    end_rect2 = end_label2.get_rect(center=(500, 475))
    end_rect = end_label.get_rect(center=(500, 400))
    screen.blit(end_label2, end_rect2)
    screen.blit(end_label, end_rect)


def main():
    running = True
    global points
    game_active = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if not game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                    game_active = True
                    points = -1
                    asteroid_rect.y = 849
                    danger.y = 849
                    danger1.y = 849
                    danger2.y = 849
                    danger3.y = 849
                    danger4.y = 849
                    danger5.y = 849
                    danger6.y = 849
                    car_rect.x = 500
                    car_rect.y = 600
                if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    pygame.quit()
                    exit()

        if game_active:
            screen.blit(background, (0, 0))
            screen.blit(car, car_rect)
            asteroid_rect.y += 5
            spawn_asteroids()
            score()

            if car_rect.y <= 0 or car_rect.y >= 678:
                game_active = False
            if car_rect.x <= -10 or car_rect.x >= 923:
                game_active = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                car_rect.y -= 650 * dt
            if keys[pygame.K_s]:
                car_rect.y += 650 * dt
            if keys[pygame.K_a]:
                car_rect.x -= 650 * dt
            if keys[pygame.K_d]:
                car_rect.x += 650 * dt

            if (
                asteroid_rect.colliderect(car_rect)
                or danger.colliderect(car_rect)
                or danger1.colliderect(car_rect)
                or danger2.colliderect(car_rect)
                or danger3.colliderect(car_rect)
                or danger4.colliderect(car_rect)
                or danger5.colliderect(car_rect)
                or danger6.colliderect(car_rect)
            ):
                game_active = False
        else:
            game_end()

        dt = clock.tick(120) / 1000
        pygame.display.flip()


main()
