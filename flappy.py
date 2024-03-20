import pygame
import neat
import os
import time
import random

# window height
WIN_WIDTH = 600
WIN_HEIGHT = 800

# loading ui image elements
BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))


class Bird:

    IMG = BIRD_IMG
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.tilt = 0
        self.tick_count = 0
        self.vel = 0

        self.height = self.y
        self.img_count = 0
        self.img = self.IMG[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # arc movement
        d = self.vel * self.tick_count + 1.5*self.tick_count**2

        # setting limits for displacement
        if d >= 16:
            d = 16
        
        if d < 0:
            d -= 2
        
        self.y = self.y + d
