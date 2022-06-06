#game options
import pygame as pg

TITLE = "FREAKS"
score = 0
SCREEN_WIDTH = 1200         
SCREEN_HEIGHT = 600
FPS = 60
iFrame = 0
zombie_spawn_counter = 0

FONT_NAME = 'arial'
#player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.
PLAYER_JUMP = -15
GRAVITY = 0.75
SHOT_DELAY = 20
PLAYERSPEED = 6
gameisplaying = False
#starting platforms
# PLATFORM_LIST = [(0, HEIGHT -40, WIDTH, 40),
#                  (WIDTH / 2 -50, HEIGHT * 3 / 4, 100,20),
#                  (125, HEIGHT -350, 100, 20),
#                  (350, 200, 100, 20),
#                  (175, 100, 50, 20)]
                 
#define colour 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
RED1 = (165,10,10)
DEEPRED = (90, 0 ,0)
GREEN = (0, 255, 0)
GREEN1 = (0, 165, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BG = LIGHTBLUE

wavestart = False
wavenumber = 0
wave_time = 0
cooldown = 0

jumpheighlvl = 0
playerspeedlvl = 0
fireratelvl = 0

