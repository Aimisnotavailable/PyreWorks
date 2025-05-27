import pygame
import math
import os
import random
from scripts.sparks import Sparks

class FireCracker:

    def __init__(self, game, pos, speed, width=10, color=(255, 255, 255), volume=1):
        self.game = game
        self.pos = list(pos)
        self.color = color
        self.speed = speed 
        self.width = width
        self.angle = 0

        self.boom = pygame.mixer.Sound(f"{os.getcwd()}\\data\sounds\\boom.wav")
        self.boom.set_volume(volume)

        self.whistle = pygame.mixer.Sound(f"{os.getcwd()}\\data\sounds\\whistle.wav")
        self.whistle.set_volume(volume)
        
    def update(self):

        for i in range(3):
            self.game.sparks.append(Sparks( (-math.pi * 1.5) + random.random() - 0.5, random.random() + 1, self.pos, self.color))
        self.pos[1] -= self.speed
        self.speed = max(0, self.speed - 0.3)

        return not self.speed
    
    def render(self, surf, offset=(0, 0)):
        
        render_points = [
            (self.pos[0], self.pos[1] - self.width),
            (self.pos[0] + self.width // 2, self.pos[1]),
            (self.pos[0] , self.pos[1] + self.width),
            (self.pos[0] - self.width // 2, self.pos[1])
        ]

        pygame.draw.polygon(surf, self.color, render_points)
