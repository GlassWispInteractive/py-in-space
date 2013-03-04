# -*- coding: utf-8 *-*
import sys

import pygame
from pygame.locals import *
from pyinspacelib import *

from menu import render_menu
from hud import render_hud
from starsky import init_starsky, tick_starsky, render_starsky

from entity import entity
from player import player
from enemy import enemy, populate
from shot import shot

# init pygame
pygame.init()
pygame.display.set_caption('PyInSpace!')
display = pygame.display.set_mode((900, 500))
menufont = pygame.font.SysFont("monospace", 28)
hudfont = pygame.font.Font("res/ubuntu_mono.ttf", 20)
fpsClock = pygame.time.Clock()
tick = 0
FPS = 30

# possible modes (menu, game, highscore?)
Mode = enum(Menu=0, Highscore=1, Game=42, Paused=21)
# start in the menu
mode = Mode.Menu
# init background
stars = init_starsky()

# variable initiations
MOVEMENT_KEYS = [K_LEFT, K_RIGHT, K_SPACE]
CONTROL_KEYS = [K_RETURN, K_ESCAPE, K_p]
KEYS = MOVEMENT_KEYS + CONTROL_KEYS


while True: # main game loop

	##############
	### EVENTS ###
	##############
	# get events
	eventList = pygame.event.get()

	# check for quit event
	if any(e.type == QUIT or (isDownPress(e) and e.key == K_q) for e in eventList):
		break

	# reduce events up to key strokes
	eventList = filter(lambda e: e.type in [KEYDOWN,KEYUP] and e.key in KEYS, eventList)
	#keyDownEvents = filter(lambda e: isDownPress(e), eventList)

	if len(eventList) != 0: print eventList

	############
	### TICK ###
	############
	stars = tick_starsky(stars, tick)

	# enter the game
	if mode == Mode.Menu and any(isDownPress(e) and e.key == K_RETURN for e in eventList):
		mode = Mode.Game
		theplayer = player() # the one and only
		entities = list()	# contains the player and all enemies and shots
							# but we maintain a reference to theplayer
		entities.append(theplayer)
		entities.extend(populate(10))
		continue

	if mode == Mode.Game:
		# switch to menu
		if any(isDownPress(e) and e.key == K_ESCAPE for e in eventList):
#			del theplayer
			del entities
			mode = Mode.Menu
			continue

		theplayer.tick(tick, entities, filter(lambda e: e.key in MOVEMENT_KEYS, eventList))
		for e in entities: e.tick(tick, entities, eventList)

		# only retain living entities
		entities = filter(lambda e: e.dead == False, entities)

	##############
	### RENDER ###
	##############
	display.fill((0, 0, 0))

	render_starsky(display, stars)

	if mode == Mode.Menu:
		render_menu(display, menufont)

	if mode == Mode.Game:
		theplayer.render(display)
		#for e in entities: e.render(display)
		for e in filter(lambda e: isinstance(e,shot), entities): e.render(display)
		for e in filter(lambda e: isinstance(e,enemy), entities): e.render(display)
		render_hud(display, hudfont, theplayer)

	pygame.display.update()

	############
	### WAIT ###
	############
	tick = tick % 3000 + 1
	# avoid overflow, calculations in starsky are done with %3 and %100 of the tick
	fpsClock.tick(FPS)


# tidy up and quit
pygame.quit()
sys.exit()
