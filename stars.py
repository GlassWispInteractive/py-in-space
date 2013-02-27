import pygame, sys
from pygame.locals import *
import random
import math

def draw_random_star(surface, kind=0, scale=1):
	x = random.randint(0,899)
	y = random.randint(0,599)
	c = random.randint(200,255)
	color = (c,c,c)
	if kind == 0:
		surface.set_at((x, y), color)
	if kind == 1:
		r = random.randint(1,4)
		pygame.draw.circle(surface, color, (x, y), r)
	if kind == 2:
		positionieren = lambda (a,b) : (math.floor(a*scale)+x, math.floor(b*scale)+y)
		
		# karo
		karo = [(10,0),(20,10),(10,20),(0,10)]
		karo = list(map(positionieren,karo))
		pygame.draw.polygon(surface, color, karo)
		
		# quadrat
		quadrat = [(3,3),(17,3),(17,17),(3,17)]
		quadrat = list(map(positionieren,quadrat))
		pygame.draw.polygon(surface, color, quadrat)

# start it
pygame.init()

# manage window
DISPLAY = pygame.display.set_mode((900, 500))

# clock object for fps
#fpsClock = pygame.time.Clock()
# list of objects to render
renderList = []

# some colors
grey = (80, 80, 80)
silver = (192, 192, 192)
white = (255, 255, 255)

#textfont = pygame.font.SysFont("monospace", 28)

while True: # main game loop
	eventList = pygame.event.get()
	if any(e.type == QUIT for e in eventList):
		break
		
	for i in range(1,100):
		draw_random_star(DISPLAY, 0)
	
	pygame.time.wait(5000000)
	
	pygame.display.update()
	# upper limit to frames
	#fpsClock.tick(30)
	
	break

# halt the game
pygame.quit()
sys.exit()
