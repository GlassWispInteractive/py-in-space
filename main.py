# -*- coding: utf-8 *-*
import pygame
from pygame.locals import *		# import pygame.locals as pyloc
from random import randint
import math

# pygame inits
pygame.init()
pygame.display.set_caption('PyInSpace!')
display = pygame.display.set_mode((900, 500))
# pygame.mixer.music.load("res/JustInSpace-Galaxy.ogg")
# pygame.mixer.music.play()

FONT = pygame.font.Font("res/starcraft.ttf", 20)
TIMER = pygame.time.Clock()
tick = 0



# variable initiations
MOVEMENT_KEYS = [K_LEFT, K_RIGHT, K_SPACE]
CONTROL_KEYS = [K_RETURN, K_ESCAPE, K_p]
KEYS = MOVEMENT_KEYS + CONTROL_KEYS


def render(func=None):
	''' decorator function for rendering '''	
	# store function
	if func:
		render.funcs.append(func)
		return func
	
	# rendering process
	else:
		display.fill((0, 0, 0))
		for f in render.funcs: f()
		TIMER.tick(30) # 30 frames per second
		pygame.display.update()
render.funcs = []


def getSurface(img):
	''' get surface from image name '''
	return pygame.image.load('res/' + str(img) + '.png')

def getogg(snd):
	return pygame.mixer.Sound('res/' + str(snd) + '.ogg')


@render
def starsky():
	''' render astonishing star sky. '''
	if tick % 100 == 0:
		for i in range(randint(0, 25 - len(starsky.stars))):
			starsky.stars.append((randint(22, 882), randint(-500, 0), 0))
	# update and delete stars
	if tick % 3 == 0:
		starsky.stars = [(x, y + 1, z if z == 0 or z > 190 else z + 7) for x, y, z in starsky.stars if y < 500]
	if tick % 100 == 0:
		r = randint(0, len(starsky.stars) - 1)
		if starsky.stars[r][2] == 0: starsky.stars[r] = (starsky.stars[r][0], starsky.stars[r][1], 1)
	
	# render stars
	for x, y, z in starsky.stars:
		pygame.draw.circle(display, (60+z%190, 60+z%190, 60+z%190), (x, y), 2)
starsky.stars = [(randint(50, 850), randint(50, 450), 0) for i in range(randint(5, 10))]




@render
def menu():
	''' render the menu '''
	if state is not menu: return
	
	display.blit(getimageobject('logo'), (157, 100))
	pygame.draw.rect(display, (192, 192, 192), (250, 300, 400, 60))
	pygame.draw.rect(display, (80, 80, 80), (255, 305, 390, 50))
	label = FONT.render("Press ENTER to start", 1, (200,200,200))
	label_pos = label.get_rect(centerx = 450, centery = 330)
	display.blit(label, label_pos)




@render
def game():
	''' Render Heads Up Display '''
	if state is not game: return
	
	textColor=(200,200,200) 
	
	info = zip(map(lambda s: pygame.image.load('res/'+s+'.png'), ['heart', 'shield', 'lightning', 'coin_stacks']),
		[0, 80, 160, 800], map(str, [player.health, player.shield, player.thunder, player.score]))
	
	for img, px, txt in info:
		display.blit(img, (4+px, 4))
		label = FONT.render(txt, 1, textColor)
		pos = label.get_rect(left = 40+px, centery = 20)
		display.blit(label, pos)




@render
def player():
	# no rendering if not game
	if state is not game: return
	
	# move shots
	player.shots = [(x, y+1) for x, y in player.shots if y < 60]
	
	# reload thunder
	player.reload = (player.reload + 1) % 40
	if player.reload == 39 and player.thunder < 9:
		player.thunder += 1
		
	# release cooldown
	if player.cooldown > 0:
		player.cooldown -= 1
	
	# render stuff
	display.blit(pygame.image.load('res/player.png'), (32+7*player.xUnits, 440))
	for x, y in player.shots:
		display.blit(pygame.image.load('res/playershot.png'), (54+7*x, 440-7*y))
player.health	= 5
player.shield	= 0
player.thunder	= 9
player.shots	= []
player.xUnits	= 56
player.movement	= 7
player.cooldown	= 0
player.score	= 0
player.reload	= 0



def f(n):
	x, y, n = 1, 0, n - 8
	while n >= 8: 
		while abs(x) % 100 != 0 and n >= 8:
			x += 1
			n -= 8
		x = x * -1 + 1
		cur = y + 6
		while y < cur and n >= 8:
			y += 1
			n -= 8
	return abs(x) % 100, y
	





@render
def mobs():
	for i in range(len(mobs.enemy)):
		n = mobs.enemy[i]
		mobs.enemy[i] += 1
		x, y = f(n)
		display.blit(pygame.image.load('res/enemy1a.png'), (26+8*x, 45+8*y))
	
mobs.enemy = [i for i in range(0, 4000, 80)]
mobs.shots = []
mobs.movement = 7




# main game loop 
state = game
events = []

while state:
	# even handling

	for e in pygame.event.get():
		# quit event
		if e.type == QUIT:
			state = None
		
		# skip event
		if e.type not in [KEYDOWN,KEYUP] or e.key not in KEYS:
			continue
		
		# store events
		if e.type == KEYDOWN:
			events.append(e.key)
		elif e.key in events:
			events.remove(e.key)
	
	# start game
	if state is menu and K_RETURN in events:
		state = game
		continue
	
	# back to menu
	if K_ESCAPE in events:
		state = menu
	
	if state is game:
		# move player
		if K_LEFT in events and player.xUnits > 0:
			player.xUnits -= 1
		elif K_RIGHT in events and player.xUnits < 112:
			player.xUnits += 1
		
		# shoot player
		if K_SPACE in events and player.thunder > 0 and player.cooldown == 0:
			#player.thunder -= 1 # TODO: workout a good balance between infinity shooting and having less ammo
			player.reload = 20
			player.cooldown = 7
			player.shots.append((player.xUnits, 0))
	
	render()
	# WAIT
	tick = tick % 3000 + 1


# tidy up and quit
pygame.quit()
