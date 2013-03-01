# -*- coding: utf-8 *-*
import pygame, sys
from random import randint
from pygame.locals import *
import stars as starslib
from header import draw_header

# default pygame
pygame.init()
pygame.display.set_caption('PyInSpace!')
graphics = pygame.display.set_mode((900, 500))
fpsClock = pygame.time.Clock()
tick = 0

# image render list
renderImg = dict()
for e in ['logo', 'player', 'playershot', 'enemy1', 'enemy1shot', 'enemy2',
	'enemy2shot', 'enemy3', 'enemy3shot', 'enemy4', 'enemy4shot']:
	renderImg[e] = pygame.image.load('res/' + e + '.png')

# star 3tuple list
stars = [(randint(50, 850), randint(50, 450), 0) for i in range(randint(5, 10))]

# variable initiations
textfont = pygame.font.SysFont("monospace", 28)
KEYS = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_RETURN, K_p]
menu = False

# render functions
def renderMenu():
	''' Render start screen. '''
	graphics.blit(renderImg['logo'], (157, 100))
	pygame.draw.rect(graphics, (192, 192, 192), (250, 300, 400, 60))
	pygame.draw.rect(graphics, (80, 80, 80), (255, 305, 390, 50))

	# label
	label = textfont.render("Start game!", 1, (200,200,200))
	labelPos = label.get_rect(centerx = 450, centery = 330)
	graphics.blit(label, labelPos)

def renderStarsky(stars):
	''' render astonishing star sky. '''
	# create new stars
	if tick % 100 == 0:
		for i in range(randint(0, 25 - len(stars))):
			stars.append((randint(50, 850), randint(-500, 0), 0))

	# update and delete stars
	if tick % 3 == 0:
		stars = [(x, y + 1, z if z == 0 or z > 190 else z + 7) for x, y, z in stars if y < 500]
	if tick % 100 == 0:
		r = randint(0, len(stars) - 1)
		if stars[r][2] == 0: stars[r] = (stars[r][0], stars[r][1], 1)

	# render stars
	for x, y, z in stars:
		#pygame.draw.circle(graphics, (60+z%190, 60+z%190, 60+z%190), (x, y), 3, 0)
		starslib.draw_star(graphics, (x,y), (60+z%190, 60+z%190, 60+z%190), kind=4, scale=1)


	return stars

offset = 0
trigger = None

def renderShip():
	''' Render battle ship. '''
	graphics.blit(renderImg['player'], (418+offset, 440))
	graphics.blit(renderImg['playershot'], (418+offset+29, 440-23))

while True: # main game loop
	eventList = pygame.event.get()

	# check for quit event
	if any(e.type == QUIT or (e.type == KEYDOWN and e.key == K_q) for e in eventList):
		break

	# reduce events up to key strokes
	eventList = filter(lambda e: e.type in [KEYDOWN,KEYUP] and e.key in KEYS, eventList)

	if any(e.type == KEYDOWN and e.key == K_UP for e in eventList):
		shoot = True

	# iterate over events
	for e in eventList:
		if e.type == KEYDOWN: trigger = e.key
		elif e.type == KEYUP and e.key == trigger: trigger = None

	if len(eventList) != 0: print eventList

	if offset > -55 * 7 and trigger == K_LEFT: offset -= 7
	elif offset < 55 * 7 and trigger == K_RIGHT: offset += 7

	graphics.fill((0, 0, 0))
	stars = renderStarsky(stars)
	if menu: renderMenu()
	else: renderShip()
	renderMenu()

	draw_header(graphics, 100, 100, 0, 1337)

	pygame.display.update()
	# upper limit to frames
	tick = tick + 1
	fpsClock.tick(30)

# halt the game
pygame.quit()
sys.exit()
