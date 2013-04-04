#!/usr/bin/env python
# -*- coding: utf-8 *-*
import pygame
#from pygame.locals import *		# import pygame.locals as pyloc
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE, K_RETURN, K_ESCAPE, K_p, KEYUP, KEYDOWN, QUIT
from random import randint

pygame.init()

MENU_FONT = pygame.font.Font("res/starcraft.ttf", 20)
HUD_FONT = pygame.font.Font("res/pixel.ttf", 20)

MUSIC = { 'active' : True,
			'menu' : "res/ObservingTheStar.ogg",
			'game' : "res/DataCorruption.ogg"
		}
TIMER = pygame.time.Clock()
DEBUG = False
FPS = 30 # 30 frames per second seem reasonable
tick = 0
TEXT_COLOR = (200, 200, 200)
MOVEMENT_KEYS = [K_LEFT, K_RIGHT, K_SPACE]
CONTROL_KEYS = [K_RETURN, K_ESCAPE, K_p]
KEYS = MOVEMENT_KEYS + CONTROL_KEYS
LEAGUE = [10, 50, 100, 500, 1000, 5000]

# pygame inits
pygame.display.set_caption('PyInSpace!')
if DEBUG: print("initialzing display")
DISPLAY = pygame.display.set_mode((900, 500))

# load all sprites at the beginning
if DEBUG: print("precaching sprites")
SPRITES = {s : pygame.image.load('res/' + str(s) + '.png').convert_alpha()
			for s in [ 'award_bronze', 'award_silver', 'award_gold',
				'coin_bronze', 'coin_silver', 'coin_gold',
				'coin_stack', 'coin_stacks',
				'ufo', 'enemyshot',
				'player', 'playershot',
				'empty', 'logo',
				'heart', 'shield', 'lightning',
				'fire', 'diamond', 'ruby' ]
				+ ["enemy"+str(i)+s+str(x) for x in range(3,5) for s in ['a','b'] for i in range(1,4)]
		  }
if DEBUG: print("precaching sounds")
SOUNDS = {s : pygame.mixer.Sound('res/' + str(s) + '.ogg')
			for s in ['laser_single', 'menu-confirm', 'confirm', 'playerdeath',
					  'enemy123deathA', 'enemy123deathB', 'ufodeath']
		 }

# helper functions
getsurface = lambda s: SPRITES[s] if s in SPRITES else pygame.image.load('res/' + s + '.png').convert_alpha()
getogg = lambda s: SOUNDS[s] if s in SOUNDS else pygame.mixer.Sound('res/' + s + '.ogg')
playsound = lambda s: getogg(s).play()


def render(func=None):
	''' decorator function for rendering '''
	# store function
	if func:
		render.funcs.append(func)
		return func

	# rendering process
	else:
		DISPLAY.fill((0, 0, 0))
		for f in render.funcs:
			f()
		TIMER.tick(FPS)
		pygame.display.update()
render.funcs = []


@render
def starsky():
	''' render astonishing star sky. '''
	if tick % 100 == 0:
		for _ in range(randint(0, 25 - len(starsky.stars))):
			starsky.stars.append((randint(22, 882), randint(-500, 0), 0))
	# update and delete stars
	if tick % 3 == 0:
		starsky.stars = [(x, y + 1, z if z == 0 or z > 190 else z + 7)
						for x, y, z in starsky.stars if y < 500]
	if tick % 100 == 0:
		r = randint(0, len(starsky.stars) - 1)
		if starsky.stars[r][2] == 0: starsky.stars[r] = (starsky.stars[r][0], starsky.stars[r][1], 1)

	# render stars
	for x, y, z in starsky.stars:
		pygame.draw.circle(DISPLAY, (60+z%190, 60+z%190, 60+z%190), (x, y), 2)
# mode doesn't matter for the bg, so initialsing it once is ok
starsky.stars = [(randint(50, 850), randint(50, 450), 0) for _ in range(randint(5, 10))]


@render
def milestone():
	''' shows milestone '''
	if not LEAGUE or 0 < LEAGUE[0]: return # TODO: 0 replace with player.score
	# initializing
	state = milestone
	new_level = 6 - len(LEAGUE) # 6 leagues - remaining milestones
	LEAGUE.pop(0)

	# get sprite, animation
	# spriteLeague = getsurface('league' + str(new_level))


	# TODO: increase difficulty
	player.thunderMax = 9 - new_level
	player.shield = max(0, player.shield - 1)


@render
def menu():
	''' render the menu '''
	# no rendering when not in menu
	if state is not menu: return

	DISPLAY.blit(getsurface('logo'), (157, 100))
	pygame.draw.rect(DISPLAY, (192, 192, 192), (250, 300, 400, 60))
	pygame.draw.rect(DISPLAY, (80, 80, 80), (255, 305, 390, 50))
	label = MENU_FONT.render("Press ENTER to start", 1, TEXT_COLOR)
	pos = label.get_rect(centerx = 450, centery = 330)
	DISPLAY.blit(label, pos)


@render
def game():
	''' Render Heads Up Display '''
	# no rendering if not in-game
	if state is not game: return

	info = list(zip(list(map(getsurface, ['heart', 'shield', 'lightning', 'coin_stacks'])),
			[0, 80, 160, 800],
			list(map(str, [player.health, player.shield, player.thunder, player.score]))))

	for img, px, txt in info:
		DISPLAY.blit(img, (4+px, 4))
		label = HUD_FONT.render(txt, 1, TEXT_COLOR)
		pos = label.get_rect(left = 40+px, centery = 20)
		DISPLAY.blit(label, pos)


@render
def player():
	''' Player function which renders the player and holds its state '''
	# no rendering if not in-game
	if state is not game: return

	# move shots
	for shot in player.shots:
		shot.rect.y -= 7
		if shot.rect.y < -20:
			player.shots.remove(shot)
			del shot
			
	# reload thunder
	player.reload = (player.reload + 1) % 100
	if player.reload == 99 and player.thunder < 9:
		player.thunder += 1

	# release cooldown
	if player.cooldown > 0:
		player.cooldown -= 1

	# render stuff
	DISPLAY.blit(getsurface('player'), (32+7*player.xUnits, 440))

	player.shots.draw(DISPLAY) # these shots are fine when rendered by the group
player.xUnits = 56
player.movement = 7


@render
def invaders():
	''' Renders enemies and their shots '''
	def move(e, x, y):
		e.pos = (e.pos[0] + x, e.pos[1] + y)
	
	# no rendering if not in-game
	if state is not game: return
	
	# mob variables
	xMin = min(map(lambda e:e.pos[0], invaders.mob))
	xMax = max(map(lambda e:e.pos[0], invaders.mob))
	
	if tick % 20 == 0:
		if invaders.dir == (True, 0):
			if xMax >= 30: invaders.dir = (True, 3)
		elif invaders.dir == (False, 0):
			if xMin <= 0: invaders.dir = (False, 3)
		else:
			a, b = invaders.dir
			invaders.dir = (not a, b - 1)
	
	for invader in invaders.mob:
		# move invader
		x, y = invader.pos
		if tick % 20 == 0:
			if invaders.dir == (True, 0):
				if xMax < 30: x += 1
			elif invaders.dir == (False, 0):
				if xMin > 0: x -= 1
			else:
				y += 1
			
			invader.pos = (x, y)
		
		# render invader
		invader.rect.topleft = (26+25*x, 45+10*y)
		DISPLAY.blit(invader.image, (invader.rect.x, invader.rect.y))
		#invaders.mob.draw(DISPLAY) # TODO: flashes...?!
		# Hast du das problem auch dass das malen über die Group flackert?
invaders.movement = 7
invaders.dir = (True, 0)

def initialize_game():
	if DEBUG: print("initializing game mode")
	player.health	= 3
	player.shield	= 0
	player.thunder	= 9
	player.shots	= pygame.sprite.OrderedUpdates() # do these need to be ordered?
	player.cooldown	= 0
	player.score	= 0
	player.reload	= 0
	invaders.mob = pygame.sprite.OrderedUpdates() # do these need to be ordered?
	
	for x in range(0,30,3):
		for y in range(0, 18, 3):
			next = pygame.sprite.Sprite()
			next.image = getsurface('enemy'+str(y%3+1)+'a3')
			next.rect = next.image.get_rect()
			next.pos = (x, y)
			invaders.mob.add(next)
	invaders.shots = []


# final inits
state = menu
laststate = game # just needs to be something else than state
events = []

if DEBUG: print("entering main game loop")
# main game loop
while state:

	# event handling
	for e in pygame.event.get():
		# quit event
		if e.type == QUIT:
			state = None
			continue

		# skip event
		if e.type not in [KEYDOWN, KEYUP] or e.key not in KEYS:
			continue

		# store events
		if e.type == KEYDOWN:
			events.append(e.key)
		elif e.key in events:
			events.remove(e.key)

	# start game
	if state is menu and K_RETURN in events:
		if DEBUG: print("entering game")
		initialize_game()
		#playsound('menu-confirm')
		state = game
		continue

	# back to menu
	if state is game and K_ESCAPE in events:
		#cleanup_game() # ?
		if DEBUG: print("leaving game")
		state = menu
		continue

	if (MUSIC['active']):
		if laststate != state:
			try:
				#pygame.mixer.music.fadeout(200) # TODO: BLOCKS WHILE FADING OUT
				pygame.mixer.music.load(MUSIC[str(state.__name__)])
				pygame.mixer.music.play()
				if DEBUG: print("current music: %s" % MUSIC[str(state.__name__)])
				laststate = state
			except AttributeError:
				pass

	if state is game:
		# move player
		if K_LEFT in events and player.xUnits > 0:
			player.xUnits -= 1


		elif K_RIGHT in events and player.xUnits < 112:
			player.xUnits += 1


		# shoot player
		if K_SPACE in events and player.thunder > 0 and player.cooldown == 0:

			player.thunder -= 1
			player.reload = 0
			player.cooldown = 7

			#player.shots.append((player.xUnits, 0))
			newshot = pygame.sprite.Sprite()
			newshot.image = getsurface('playershot')
			newshot.rect = newshot.image.get_rect()
			newshot.rect.topleft = (55+7*player.xUnits, 440)
			player.shots.add(newshot)
			if DEBUG: print("player fired a shot at x=%d" % newshot.rect.x)
			playsound('laser_single')

		# It'z time to make the magicz...
		# noo, just doing the collision detection and dying in one line
		enemies_hit = len(pygame.sprite.groupcollide(player.shots, invaders.mob, True, True))
		player.score += enemies_hit
		player.thunder = min(9, enemies_hit + player.thunder)

	render() # waiting is done in render
	tick = tick % 3000 + 1 # avoid overflow


# tidy up and quit
if DEBUG: print("quitting")
pygame.quit()

