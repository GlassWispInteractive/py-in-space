# -*- coding: utf-8 *-*
import sys

import pygame
from pygame.locals import *

from menu import render_menu
from hud import render_hud
from starsky import init_starsky, update_starsky, render_starsky

from entity import entity
from player import player
from enemy import enemy, populate
from shot import shot

from enum import enum

# init pygame
pygame.init()
pygame.display.set_caption('PyInSpace!')
display = pygame.display.set_mode((900, 500))
fpsClock = pygame.time.Clock()
textfont = pygame.font.SysFont("monospace", 28)
tick = 0

# possible modes (menu, game, highscore?)
Mode = enum(Menu=0, Game=1)
# start in the menu
mode = Mode.Menu

# variable initiations
MOVEMENT_KEYS = [K_LEFT, K_RIGHT, K_SPACE]
CONTROL_KEYS = [K_RETURN, K_ESCAPE, K_p]
KEYS = MOVEMENT_KEYS + CONTROL_KEYS

# initialisations
stars = init_starsky()

# initialize entities
entities = list()
player = player(100, 100, 0, 0) # the one and only
#entities.append(player)
entities.extend(populate(10)) # only contains enemies and shots

# do the initial drawing
render_starsky(display, stars)
render_menu(display, textfont)

while True: # main game loop

	### EVENTS

	# get events
	eventList = pygame.event.get()

	# check for quit event
	if any(e.type == QUIT or (e.type == KEYDOWN and e.key == K_q) for e in eventList):
		break

	# reduce events up to key strokes
	eventList = filter(lambda e: e.type in [KEYDOWN,KEYUP] and e.key in KEYS, eventList)
	#keyDownEvents = filter(lambda e: e.type == KEYDOWN, eventList)

	if len(eventList) != 0: print eventList

	# send event list to player


	### TICK
	starts = update_starsky(stars, tick)
	player.tick(entities, filter(lambda e: e.key in MOVEMENT_KEYS, eventList))
	for e in entities: e.tick(entities, eventList)

	# only retain living entities
	entities = filter(lambda e: e.dead == False, entities)

	if mode == Mode.Menu and any((e.type == KEYDOWN and e.key == K_RETURN) for e in eventList):
		mode = Mode.Game

	if mode == Mode.Game and any((e.type == KEYDOWN and e.key == K_ESCAPE) for e in eventList):
		mode = Mode.Menu

	### RENDER
	display.fill((0, 0, 0))
	render_starsky(display, stars)

	if mode == Mode.Menu:
		render_menu(display, textfont)

	if mode == Mode.Game:
		render_hud(display, player)
		player.render(display)
		#for e in entities: e.render(display)


	# All drawing goes before this
	pygame.display.update()

	### WAIT
	tick += 1
	fpsClock.tick(30)


# tidy up and quit
pygame.quit()
sys.exit()
