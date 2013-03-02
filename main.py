# -*- coding: utf-8 *-*
import pygame, sys
from random import randint
from pygame.locals import *
import stars as starslib
from header import draw_header
import entity

# default pygame
pygame.init()
pygame.display.set_caption('PyInSpace!')
display = pygame.display.set_mode((900, 500))
fpsClock = pygame.time.Clock()
tick = 0

# possible modes (menu, game, highscore?)
Mode = enum(Menu=0, Game=1)

# start in the menu
mode = Mode.Menu

# variable initiations
textfont = pygame.font.SysFont("monospace", 28)
MOVEMENT_KEYS = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE]
CONTROL_KEYS = [K_RETURN, K_p]


while True: # main game loop

	### EVENTS

	# get events
	eventList = pygame.event.get()

	# check for quit event
	if any(e.type == QUIT or (e.type == KEYDOWN and e.key == K_q) for e in eventList):
		break

	# reduce events up to key strokes
	eventList = filter(lambda e: e.type in [KEYDOWN,KEYUP] and e.key in KEYS, eventList)

	if len(eventList) != 0: print eventList

	# send event list to player


	### TICK





	### RENDER
	display.fill((0, 0, 0))
	stars = renderStarsky(stars)
	if menu: renderMenu()
	else: renderShip()
	renderMenu()

	draw_header(display, 100, 100, 0, 1337)

	pygame.display.update()


	### WAIT
	tick += 1
	fpsClock.tick(30)


# halt the game
pygame.quit()
sys.exit()
