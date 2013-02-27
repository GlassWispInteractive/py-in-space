import pygame, sys
from random import randint
from pygame.locals import *
import stars as starslib

# default pygame
pygame.init()
pygame.display.set_caption('PyInSpace!')
graphics = pygame.display.set_mode((900, 500))
fpsClock = pygame.time.Clock()
tick = 0

# image render list
renderImg = dict()
for e in ['logo', 'player', 'playershot', 'enemy1', 'enemy1shot', 'enemy2', 'enemy2shot', 'enemy3', 'enemy3shot', 'enemy4', 'enemy4shot']:
	renderImg[e] = pygame.image.load('res/' + e + '.png')

# star 3tuple list
stars = [(randint(50, 850), randint(50, 450), 0) for i in range(randint(5, 10))]

# variable initiations
textfont = pygame.font.SysFont("monospace", 28)
KEYS = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_RETURN, K_p, K_q]
menu = True

# render functions
def renderMenu():
	''' Render start screen. '''
	graphics.blit(renderImg['logo'], (157, 100))
	pygame.draw.rect(graphics, (192, 192, 192), (250, 300, 400, 60))
	pygame.draw.rect(graphics, (80, 80, 80), (260, 305, 380, 50))
	
	# label
	label = textfont.render("Start game!", 1, (200,200,200))
	labelPos = label.get_rect(centerx=450, centery = 330)
	graphics.blit(label, labelPos)

def renderStarsky(stars):
	''' render astonishing star sky. '''
	# create new stars
	if tick % 100 == 0:
		for i in range(randint(0, 25 - len(stars))):
			stars.append((randint(50, 850), randint(-500, 0), 0))
	
	# update and delete stars
	if tick % 3 == 0: stars = [(x, y + 1, z if z == 0 or z > 190 else z + 7) for x, y, z in stars if y < 500]
	if tick % 100 == 0:
		r = randint(0, len(stars) - 1)
		if stars[r][2] == 0: stars[r] = (stars[r][0], stars[r][1], 1)
		
	# render stars
	for x, y, z in stars:
		#pygame.draw.circle(graphics, (60+z%190, 60+z%190, 60+z%190), (x, y), 3, 0)
		starslib.draw_star(graphics, (x,y), (60+z%190, 60+z%190, 60+z%190), kind=4, scale=1)
	
	return stars

def renderShip():
	''' Render battle ship. '''
	pass

while True: # main game loop
	eventList = pygame.event.get()
	
	# check for quit event
	if any(e.type == QUIT or (e.type == KEYDOWN and e.key == K_q) for e in eventList):
		break
	
	# reduce events up to key strokes
	eventList = [e.key for e in eventList if e.type == KEYDOWN and e.key in KEYS]
	
	# just accepts the first movement
#	print eventList
	
	graphics.fill((0, 0, 0))
	stars = renderStarsky(stars)
	renderMenu()

	pygame.display.update()
	# upper limit to frames
	tick = tick + 1
	fpsClock.tick(30)

# halt the game
pygame.quit()
sys.exit()
