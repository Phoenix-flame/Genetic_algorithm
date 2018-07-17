import sys
import pygame
import numpy as np
from random import randint
import random as rand
import numpy as np


class enemy:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self._speed = 4
        self.radius = 50

    def move(self):
        self.x += self._speed
        self.check()

    def check(self):
        if self.x > 800 - self.radius or self.x < 200 + self.radius:
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


    def check(self, enemies):
        for i in enemies:
            if self.dist(self.x, i.x, self.y, i.y) < (i.radius / 2) + 25:
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
                self.directions[i] = [rand.choice([-1, 1]), rand.choice([-1, 1])]






class Dot:
    def __init__(self):
        self.brain = Brain(1000)
        self.x, self.y = 200, 475
        # initial position for debugging
        # self.x, self.y = 500, 300
        self.vel_x, self.vel_y = 0, 0
        self.acc_x, self.acc_y = 0, 0
        self.fitness = float(0.0)
        self.isBest = False
        self.isDead = False
        self.reachedGoal = False

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
        if not self.isDead and not self.reachedGoal:
            self.move()
            x = self.x
            y = self.y
            if self.dist(self.x, 800, self.y, 125) < 25:
                self.reachedGoal = True
            if x < 5 and x > 995 and y < 5 and y > 595:
                self.isDead = True
            elif x > 195 and x < 205:
                if y > 100 and y < 450:
                    self.isDead = True  
            if x > 795 and x < 805:
                if y > 150 and y < 500:
                    self.isDead = True
            if y > 95 and y < 105:
                if x > 200 and x < 800:
                    self.isDead = True
            if y > 495 and y < 505:
                if x > 200 and x < 800:
                    self.isDead = True
            if y > 495 and y < 505:
                if x > 150 and x < 200:
                    self.isDead = True
            if y > 450 and y < 500:
                if x > 145 and x < 155:
                    self.isDead = True
            if y > 445 and y < 455:
                if x > 150 and x < 200:
                    self.isDead = True

            for i in enemies:
                if self.dist(self.x, i.x, self.y, i.y) < (i.radius / 2) + 25:
                    self.isDead = True

    def dist(self, x1, x2, y1, y2):
        return np.sqrt( ((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)) )

    def Calculatefitness(self):
        if (self.reachedGoal):
            self.fitness = float(1.0/16 + 10000.0/(self.brain.step * self.brain.step))
        else :
            d = self.dist(self.x, 800, self.y, 125)
            self.fitness = float(1.0 / (d * d))
        # print(self.fitness)     ## for debugging

    def clone(self):
        baby = Dot()
        baby.brain = self.brain.clone()
        return baby

class Population:
    def __init__(self, size):
        self.size = size
        self.dots = []
        self.gen = 1
        self.best_dot = 0
        self.min_step = 1000
        self.fitnessSum = float(0.0)
        for i in range(self.size):
            self.dots.append(Dot())

    def update(self, enemies):
        for i in range(self.size):
            if (self.dots[i].brain.step > self.min_step):
                self.dots[i].isDead = True
            else:
                self.dots[i].update(enemies)

    def calculateAllFitness(self):
        for i in range(self.size):
            self.dots[i].Calculatefitness()

    def allDead(self) -> bool:
        for i in range(self.size):
            if not self.dots[i].isDead and  not self.dots[i].reachedGoal:
                return False
        return True

    def naturalSelection(self):
        new_gen = []
        self.setBestDot()
        self.calculateAllFitness()
        self.calculateFitnessSum()
        new_gen.append(self.dots[self.best_dot].clone())
        new_gen[0].isBest = True

        for i in range(1, self.size):
            parent = self.selectParent()
            new_gen.append(parent.clone())

        self.dots = new_gen
        self.gen += 1
        self.fitnessSum = 0.0

    def calculateFitnessSum(self):
        for i in range(self.size):
            self.fitnessSum = float(float(self.fitnessSum) + float(self.dots[i].fitness))
        return float(self.fitnessSum)

    def selectParent(self):

        # print(self.fitnessSum)   ## for debugging
        r = rand.uniform(0.0, self.fitnessSum)

        runningSum = 0.0
        test = 0.0
        for i in range(self.size):
            runningSum += self.dots[i].fitness
            if runningSum > r:
                return self.dots[i]
            test += self.dots[i].fitness


    def mutate(self):
        for i in range(self.size):
            self.dots[i].brain.mutate()

    def setBestDot(self):
        max = 0.0
        maxIndex = 0

        for i in range(self.size):
            if self.dots[i].fitness > max:
                max = self.dots[i].fitness
                maxIndex = i

        self.best_dot = maxIndex

        if self.dots[self.best_dot].reachedGoal:
            self.min_step = self.dots[self.best_dot].brain.step
