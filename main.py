# -*- coding: utf-8 *-*
import sys
import pygame
from pygame.locals import *
from random import randint

from entities import Entity, Player, Enemy, Shot
from pyinspacelib import *

# init pygame
pygame.init()
pygame.display.set_caption('PyInSpace!')
display = pygame.display.set_mode((900, 500))
menufont = pygame.font.SysFont("monospace", 28)
hudfont = pygame.font.Font("res/ubuntu_mono.ttf", 20)
if MUSIC:
	pygame.mixer.music.load("res/JustInSpace-Galaxy.ogg")
	pygame.mixer.music.play()
fpsClock = pygame.time.Clock()
tick = 0
FPS = 30

# possible modes (menu, game, highscore?)
modeMenu, modeHighscore, modeGame, modePaused = range(4)

# start in the menu
mode = modeMenu

# init background
stars = [(randint(50, 850), randint(50, 450), 0) for i in range(randint(5, 10))]

# variable initiations
MOVEMENT_KEYS = [K_LEFT, K_RIGHT, K_SPACE]
CONTROL_KEYS = [K_RETURN, K_ESCAPE, K_p]
KEYS = MOVEMENT_KEYS + CONTROL_KEYS

def render_menu(surface, textfont):
	surface.blit(getimageobject('logo'), (157, 100))
	pygame.draw.rect(surface, (192, 192, 192), (250, 300, 400, 60))
	pygame.draw.rect(surface, (80, 80, 80), (255, 305, 390, 50))
	label = textfont.render("Press ENTER to start", 1, (200,200,200))
	label_pos = label.get_rect(centerx = 450, centery = 330)
	surface.blit(label, label_pos)

def render_hud(surface, hudfont, player, textPadding=20,
				textColor=(200,200,200), iconPadding=4):
	''' Render Heads Up Display '''
	header_sprites = dict()
	for e in ['heart', 'shield', 'lightning', 'coin_stacks']:
		header_sprites[e] = getimageobject(e)
	surface.blit(header_sprites['heart'], (0+iconPadding, iconPadding))
	surface.blit(header_sprites['shield'], (1*90+iconPadding, iconPadding))
	surface.blit(header_sprites['lightning'], (2*90+iconPadding, iconPadding))
	surface.blit(header_sprites['coin_stacks'], (864, iconPadding))
	label = hudfont.render(str(player.health), 1, textColor)
	label_pos = label.get_rect(left = 0.5*90, centery = textPadding)
	surface.blit(label, label_pos)
	label = hudfont.render(str(player.shield), 1, textColor)
	label_pos = label.get_rect(left = 1.5*90, centery = textPadding)
	surface.blit(label, label_pos)
	label = hudfont.render(str(player.thunder), 1, textColor)
	label_pos = label.get_rect(left = 2.5*90, centery = textPadding)
	surface.blit(label, label_pos)
	label = hudfont.render(str(player.score), 1, textColor)
	label_pos = label.get_rect(right = 9.5*90, centery = textPadding)
	surface.blit(label, label_pos)

def tick_starsky(stars, tick):
	# create new stars
	if tick % 100 == 0:
		for i in range(randint(0, 25 - len(stars))):
			stars.append((randint(22, 882), randint(-500, 0), 0))
	# update and delete stars
	if tick % 3 == 0:
		stars = [(x, y + 1, z if z == 0 or z > 190 else z + 7) for x, y, z in stars if y < 500]
	if tick % 100 == 0:
		r = randint(0, len(stars) - 1)
		if stars[r][2] == 0: stars[r] = (stars[r][0], stars[r][1], 1)

	return stars

def render_starsky(stars):
	''' render astonishing star sky. '''
	# render stars
	for x, y, z in stars:
		pygame.draw.circle(display, (60+z%190, 60+z%190, 60+z%190), (x, y), 2)


while True: # main game loop

	# EVENTS
	eventList = pygame.event.get()

	# check for quit event
	if any(e.type == QUIT or (isDownPress(e) and e.key == K_q) for e in eventList):
		break

	# reduce events up to key strokes
	eventList = [e for e in eventList if e.type in [KEYDOWN,KEYUP] and e.key in KEYS]
	#keyDownEvents = filter(lambda e: isDownPress(e), eventList)

	if len(eventList) != 0: print eventList

	# TICK
	stars = tick_starsky(stars, tick)

	if mode == modeMenu and any(isDownPress(e) and e.key == K_RETURN for e in eventList):
		# enter the game
		mode = modeGame
		theplayer = Player() # the one and only
		entities = list()			# contains the player and all enemies and shots
		entities.append(theplayer)	# but we maintain a reference to theplayer
		entities.extend(Enemy.populate(10))
		continue

	if mode == modeGame:
		# switch to menu
		if any(isDownPress(e) and e.key == K_ESCAPE for e in eventList):
			del entities
			mode = modeMenu
			continue

		theplayer.tick(tick, entities, [e for e in eventList if e.key in MOVEMENT_KEYS])
		for e in entities: e.tick(tick, entities, eventList)

		# only retain living entities
		entities = [e for e in entities if e.dead == False]

	# RENDER
	display.fill((0, 0, 0))
	render_starsky(stars)

	if mode == modeMenu:
		render_menu(display, menufont)

	if mode == modeGame:
		theplayer.render(display)
		#for e in entities: e.render(display)
		for e in [e for e in entities if isinstance(e, Shot)]: e.render(display)
		for e in [e for e in entities if isinstance(e, Enemy)]: e.render(display)
		render_hud(display, hudfont, theplayer)

	pygame.display.update()

	# WAIT
	tick = tick % 3000 + 1
	# avoid overflow, calculations in starsky are done with %3 and %100 of the tick
	fpsClock.tick(FPS)

# tidy up and quit
pygame.quit()
sys.exit()

