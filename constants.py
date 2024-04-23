import pygame
from random import randint
import os
import math

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150,150,150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 16:9 aspect ratio
WIDTH = 1280
HEIGHT = 720

WORLD_WIDTH = 5000
WORLD_HEIGHT = 5000

PLAYER_MAX_SPEED = 200
ENEMY_MAX_SPEED = 110
BULLET_SPEED = 300

SCORE_INCREASE_ON_ENEMY_DEATH = 100

