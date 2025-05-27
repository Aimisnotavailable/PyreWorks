import pygame
import sys
import os
import random
import math
import json
from scripts.engine import Engine
from scripts.sparks import Sparks
from scripts.firecracker import FireCracker

SPARK_COUNT = 100
SPARK_SPEED_MIN = 6
FIRECRACKER_WIDTH = 6
FIRECRACKER_SPEED_MIN = 7

class Window(Engine):
    
    def __init__(self, dim=..., font_size=20):
        super().__init__(dim, font_size)

        self.outline = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        self.sparks : list[Sparks] = []
        self.fire_crackers : list[FireCracker] = []
        self.reload = 0
        self.delay = 5

        pygame.mixer.init()

        try:
            with open(f'{os.getcwd()}\\data\\config.json', 'r+') as fp:
                config = json.load(fp)

                global SPARK_COUNT 
                global SPARK_SPEED_MIN
                global FIRECRACKER_WIDTH
                global FIRECRACKER_SPEED_MIN

                SPARK_COUNT = config['SPARK_COUNT']
                SPARK_SPEED_MIN = config['SPARK_SPEED_MIN']
                FIRECRACKER_WIDTH = config['FIRECRACKER_WIDTH']
                FIRECRACKER_SPEED_MIN = config['FIRECRACKER_SPEED_MIN']
                self.delay = min(60, 60 // config['FIRECRACKER_SPAWN_PER_SECOND'])

        except Exception as e:
            with open(f'{os.getcwd()}\\data\\config.json', 'w+') as fp:
                json.dump({"SPARK_COUNT" : 100,
                           "SPARK_SPEED_MIN" : 6,
                           "FIRECRACKER_WIDTH" : 6,
                           "FIRECRACKER_SPEED_MIN" : 6,
                           "FIRECRACKER_SPAWN_PER_SECOND" : 12}, fp)
        self.clicking = False
        
    
    def draw_outlines(self):
        mask = pygame.mask.from_surface(self.outline)
        mask_surf = mask.to_surface(setcolor=(255, 192, 203, 180), unsetcolor=(0, 0, 0, 0))

        for offset in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            self.display.blit(mask_surf, offset)

    def run(self):
        global SPARK_COUNT 
        global SPARK_SPEED_MIN
        global FIRECRACKER_WIDTH
        global FIRECRACKER_SPEED_MIN

        while True:
            self.outline.fill((0, 0, 0, 0))
            self.display.fill((0, 0, 0))
            mpos = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # for i in range(SPARK_COUNT):
                        #     self.sparks.append(Sparks((random.random() * math.pi * 2), random.random() + 3, (mpos[0] // 2, mpos[1] // 2)))
                        self.clicking = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                        self.reload = 0

            if self.clicking :
                if not self.reload % self.delay:
                    self.fire_crackers.append(FireCracker(self, (mpos[0]//2, mpos[1]//2), random.random() + FIRECRACKER_SPEED_MIN, FIRECRACKER_WIDTH, (random.randint(255, 255), random.randint(140, 192), random.randint(160, 203)), volume=max(0.2, random.random())))
                    self.fire_crackers[-1].whistle.play()
                self.reload += 1
            
            for fire_cracker in self.fire_crackers.copy():
                fire_cracker.render(self.display)

                if fire_cracker.update():
                    for i in range(SPARK_COUNT):
                        self.sparks.append(Sparks((random.random() * math.pi * 2), random.random() + SPARK_SPEED_MIN, fire_cracker.pos, fire_cracker.color))
                    fire_cracker.boom.play()
                    self.fire_crackers.remove(fire_cracker)

            for spark in self.sparks.copy():
                spark.render(self.outline)

                if spark.update():
                    # spark.set_death_timer()
                    # if spark.kill:
                        self.sparks.remove(spark)

            self.draw_outlines()
            # self.outline.blit(self.display, (0, 0))
            self.display.blit(self.outline, (0, 0))
            

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(60)


Window((800, 400)).run()