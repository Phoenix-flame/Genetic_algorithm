import sys
import pygame
import numpy as np
from random import randint
import random as rand
import numpy as np


class enemy:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self._speed = 2
        self.radius = 30

    def move(self):
        self.x += self._speed
        self.check()

    def check(self):
        if self.x > 800 - self.radius or self.x < 200 + self.radius :
            self._speed = -self._speed

    def draw(self, screen):
        circle_color = 255, 210, 20
        pygame.draw.circle(screen, circle_color, [self.x, self.y], self.radius)

class player:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
        self.radius = 10

    def move(self, x, y):
        if x > 0 and x < 1000 and y > 0 and y < 600:
            if x > 190 and x < 215:
                if y > 100 and y < 450:
                    return  
            if x > 790 and x < 810:
                if y > 150 and y < 500:
                    return  
            if y > 90 and y < 110:
                if x > 200 and x < 800:
                    return  
            if y > 490 and y < 510:
                if x > 200 and x < 800:
                    return 
            self.x, self.y = x, y


    def check(self, enemies, br):
        for i in enemies:
            if self.dist(self.x, i.x, self.y, i.y) < 30 :
                print("Collision")
                return False
        return True


    def dist(self, x1, x2, y1, y2):
        return np.sqrt( ((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)) )


class Brain:
    def __init__(self, size):
        self.size = size
        self.directions = self.random(size)
        self.step = 0
    def random(self, size):
        directions = []
        for i in range(size):
            x = rand.choice([-1, 1])
            y = rand.choice([-1, 1])
            directions.append([x, y])
        return directions
    def clone(self):
        brain_clone = Brain(self.size)
        for i in range(self.size):
             brain_clone.directions[i] = self.directions[i]
        return brain_clone
    def mutate(self):
        mutate_rate = 0.01
        for i in range(self.size):
            r = rand.random()
            if r < mutate_rate:
                print("ok")
                self.directions[i] = [rand.choice([-1, 1]), rand.choice([-1, 1])]






class Dot:
    def __init__(self):
        self.brain = Brain(1000)
        self.x, self.y = 200, 475
        self.vel_x, self.vel_y = 0, 0
        self.acc_x, self.acc_y = 0, 0
        self.fitness = 0
        self.isBest = False
        self.isDead = False

    def move(self):
        # print("move")
        if len(self.brain.directions) > self.brain.step:
            self.acc_x, self.acc_y = self.brain.directions[self.brain.step]
            self.brain.step += 1
        else :
            self.isDead = True
        x_check = self.vel_x + self.acc_x
        y_check = self.vel_y + self.acc_y

        speed_limit = 4
        if x_check < speed_limit and y_check < speed_limit and x_check > -speed_limit and y_check > -speed_limit:
            self.vel_x, self.vel_y = x_check, y_check
        # print("---------------------")
        # print(self.vel_x, " ", self.vel_y)
        self.x, self.y = self.x + self.vel_x, self.y + self.vel_y
        # print(self.x, " ", self.y)

    def update(self, enemies):
        if not self.isDead:
            self.move()
            x = self.x
            y = self.y
            if x < 5 and x > 995 and y < 5 and y > 595:
                self.isDead = True
            elif x > 190 and x < 215:
                if y > 100 and y < 450:
                    self.isDead = True  
            if x > 790 and x < 810:
                if y > 150 and y < 500:
                    self.isDead = True
            if y > 90 and y < 110:
                if x > 200 and x < 800:
                    self.isDead = True
            if y > 490 and y < 510:
                if x > 200 and x < 800:
                    self.isDead = True
            for i in enemies:
                if self.dist(self.x, i.x, self.y, i.y) < (i.radius / 2) + 10 :
                    self.isDead = True

    def dist(self, x1, x2, y1, y2):
        return np.sqrt( ((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)) )