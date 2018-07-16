import sys
import pygame
import numpy as np
from random import randint
import random as rand
import numpy as np
from classes import *



def events(me):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            pass
            # print(pygame.mouse.get_pos())
            # me.move(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        # elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        #     if event.key == pygame.K_UP :
        #         me.move(me.x, me.y + 1)
               


def loop(enemies, me, br, dots):
    for i in enemies:
        i.move()
    for j in dots:
        j.update(enemies)
    return me.check(enemies, br)


def draw(screen, me):
    white = 255, 255, 255
    black = 0, 0, 0
    screen.fill(white)
    # print("ok")
    up_left_corner = 200, 100
    up_right_corner = 800, 100
    down_left_corner = 200, 500
    down_right_corner = 800, 500

    pygame.draw.line(screen, black, up_left_corner, up_right_corner, 5)

    pygame.draw.line(screen, black, down_left_corner, down_right_corner, 5)

    pygame.draw.line(screen, black, up_left_corner, [down_left_corner[0], down_left_corner[1] - 50], 5)

    pygame.draw.line(screen, black, [up_right_corner[0], up_right_corner[1] + 50], down_right_corner, 5)

    circle_color = 255, 210, 20
    pygame.draw.circle(screen, circle_color, [me.x, me.y], me.radius)

    # pygame.display.update()
    # pygame.display.flip()
    # fps.tick(60)


def main():
    # fps = pygame.time.Clock()
    paused = False
    size = [1000, 600]
    pygame.init()
    Fullscreen = pygame.DOUBLEBUF | pygame.FULLSCREEN
    Normal = pygame.DOUBLEBUF
    screen = pygame.display.set_mode(size, Normal)
    circle_color = 255, 210, 20
    people_color = 200, 180, 255
    br = True
    while 1:
        enemies = []
        enemies.append(enemy(230, 200))
        enemies.append(enemy(770, 300))
        enemies.append(enemy(230, 400))
        pygame.mouse.set_visible(True)
        me = player(150, 550)
        br = True
        dots = []
        for i in range(500):
            dots.append(Dot())

        while br:
            # print(g.mouse.get_pos())
    
            ### defining enemies
            events(me)
            br = loop(enemies, me, br, dots)
            draw(screen, me)

            for i in enemies:
                pygame.draw.circle(screen, circle_color, [i.x, i.y], i.radius)
            for j in dots:
                pygame.draw.circle(screen, people_color, [j.x, j.y], 4)
            pygame.display.update()
            # pygame.display.flip()

            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_LEFT]: 
                me.move(me.x - 1, me.y)       
            if pressed_key[pygame.K_RIGHT]:
                me.move(me.x + 1, me.y)
            if pressed_key[pygame.K_UP]:
                me.move(me.x, me.y - 1)
            if pressed_key[pygame.K_DOWN]:
                me.move(me.x, me.y + 1)  
            if pressed_key[pygame.K_SPACE]:
                break

if __name__ == "__main__":
    main()