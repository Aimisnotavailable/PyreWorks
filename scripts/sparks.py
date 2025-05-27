import pygame
import math
import random

class Sparks:

    def __init__(self, angle, speed, pos, color=(255, 255, 255), is_spread=False):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.max_speed = speed

        self.color = color
        self.spread = []
        self.is_spread = is_spread

        self.render_points = []
        self.drop_offset = 0

        self.flicker = False

        self.death_timer = 0
        self.kill = False
    
    def recalculate_render_points(self, offset):

        render_points = [
            (self.pos[0] - offset[0] + math.cos(self.angle) * self.speed * 3 + self.drop_offset * math.cos(self.angle) * 0.4,
             self.pos[1] - offset[1] + math.sin(self.angle) * self.speed * 3 + self.drop_offset),
            (self.pos[0] - offset[0] + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5 + self.drop_offset * math.cos(self.angle) * 0.4,
             self.pos[1] - offset[1] + math.sin(self.angle + math.pi * 0.5) * self.speed * 0.5 + self.drop_offset * 0.7),
            (self.pos[0] - offset[0] + math.cos(self.angle + math.pi) * self.speed * 3 + self.drop_offset * math.cos(self.angle) * 0.4,
             self.pos[1] - offset[1] + math.sin(self.angle + math.pi) * self.speed * 3 + self.drop_offset * 0.7),
            (self.pos[0] - offset[0] + math.cos(self.angle - math.pi * 0.5) * self.speed * 0.5 + self.drop_offset * math.cos(self.angle) * 0.4,
             self.pos[1] - offset[1] + math.sin(self.angle - math.pi * 0.5) * self.speed * 0.5 + self.drop_offset * 0.7)
        ]
        return render_points

    def calculate_drop_offset(self):
        self.drop_offset += (self.max_speed - self.speed) * 0.5

    def set_death_timer(self):
        if not self.death_timer:
            self.death_timer = 10
        
    def update(self):
        if not self.is_spread and random.randint(0, 1) :
            self.spread.append(Sparks((random.random() - 0.5) * math.pi, self.speed / 2, self.pos, (0, 0, 0), True))

        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 0.1)
        self.calculate_drop_offset()

        # if self.death_timer:
        #     # self.flicker = bool(self.death_timer % 2)
        #     self.death_timer = max(0, self.death_timer - 1)
            
        #     if not self.death_timer:
        #         self.kill = True

        return not self.speed
    
    def render(self, surf, offset=(0, 0)):

        if not self.flicker:
            self.render_points = self.recalculate_render_points(offset=offset)

            pygame.draw.polygon(surf, self.color, self.render_points)