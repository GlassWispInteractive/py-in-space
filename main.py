# -*- coding: utf-8 *-*
import pygame
#from pygame.locals import *		# import pygame.locals as pyloc
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE, K_RETURN, K_ESCAPE, K_p, KEYUP, KEYDOWN, QUIT
from random import randint

pygame.init()

FONT = pygame.font.Font("res/starcraft.ttf", 20)
MUSIC = { 'active' : True,
			'menu' : "res/ObservingTheStar.ogg",
			'game' : "res/DataCorruption.ogg"
		}
TIMER = pygame.time.Clock()
FPS = 30 # 30 frames per second seems reasonable
tick = 0
TEXT_COLOR = (200, 200, 200)
MOVEMENT_KEYS = [K_LEFT, K_RIGHT, K_SPACE]
CONTROL_KEYS = [K_RETURN, K_ESCAPE, K_p]
KEYS = MOVEMENT_KEYS + CONTROL_KEYS

# pygame inits
pygame.display.set_caption('PyInSpace!')
DISPLAY = pygame.display.set_mode((900, 500))

# load all sprites at the beginning
SPRITES = {s : pygame.image.load('res/' + str(s) + '.png').convert_alpha()
			for s in [ 'award_bronze', 'award_silver', 'award_gold',
				'coin_bronze', 'coin_silver', 'coin_gold',
				'coin_stack', 'coin_stacks',
				'enemy1', 'enemy1a', 'enemy1b', 'enemy1shot',
				'enemy2', 'enemy2a', 'enemy2b', 'enemy2shot',
				'enemy3', 'enemy3a', 'enemy3b', 'enemy3shot',
				'player', 'playerold', 'playershot',
				'ufo', 'ufoold', 'ufooldshot',
				'empty', 'logo',
				'heart', 'shield', 'lightning',
				'fire', 'diamond', 'ruby' ]
		  }
SOUNDS = {s : pygame.mixer.Sound('res/' + str(s) + '.ogg')
			for s in ['laser_single', 'menu-confirm', 'confirm', 'playerdeath',
					  'enemy123deathA', 'enemy123deathB', 'ufodeath']
		 }

# helper functions
getsurface = lambda s: SPRITES[str(s)] if str(s) in SPRITES else pygame.image.load('res/' + str(s) + '.png').convert_alpha()
getogg = lambda s: SOUNDS[str(s)] if str(s) in SOUNDS else pygame.mixer.Sound('res/' + str(s) + '.ogg')


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
		for _ in xrange(randint(0, 25 - len(starsky.stars))):
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
starsky.stars = [(randint(50, 850), randint(50, 450), 0) for _ in xrange(randint(5, 10))]


@render
def menu():
	''' render the menu '''
	# no rendering when not in menu
	if state is not menu: return

	DISPLAY.blit(getsurface('logo'), (157, 100))
	pygame.draw.rect(DISPLAY, (192, 192, 192), (250, 300, 400, 60))
	pygame.draw.rect(DISPLAY, (80, 80, 80), (255, 305, 390, 50))
	label = FONT.render("Press ENTER to start", 1, TEXT_COLOR)
	pos = label.get_rect(centerx = 450, centery = 330)
	DISPLAY.blit(label, pos)


@render
def game():
	''' Render Heads Up Display '''
	# no rendering if not in-game
	if state is not game: return

	info = zip(map(getsurface, ['heart', 'shield', 'lightning', 'coin_stacks']),
			[0, 80, 160, 800],
			map(str, [player.health, player.shield, player.thunder, player.score]))

	for img, px, txt in info:
		DISPLAY.blit(img, (4+px, 4))
		label = FONT.render(txt, 1, TEXT_COLOR)
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
		if shot.rect.y < -20: player.shots.remove(shot) # TODO: PROBABLY DANGEROUS

	# reload thunder
	player.reload = (player.reload + 1) % 40
	if player.reload == 39 and player.thunder < 9:
		player.thunder += 1

	# release cooldown
	if player.cooldown > 0:
		player.cooldown -= 1

	# render stuff
	DISPLAY.blit(getsurface('player'), (32+7*player.xUnits, 440))

	player.shots.draw(DISPLAY) # these shots look ok when rendered by the group


@render
def invaders():
	''' Renders enemies and their shots '''
	# no rendering if not in-game
	if state is not game: return

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

	for invader in invaders.mob:
		n = invader.n
		invader.n += 1
		x, y = f(n)
		invader.rect.topleft = (26+8*x, 45+8*y)
		DISPLAY.blit(invader.image, (invader.rect.x, invader.rect.y))
		#invaders.mob.draw(DISPLAY) # TODO: flashes...?!


def initialize_game():
	player.health	= 5
	player.shield	= 0
	player.thunder	= 9
	player.shots	= pygame.sprite.OrderedUpdates() # do these need to be ordered?
	player.xUnits	= 56
	player.movement	= 7
	player.cooldown	= 0
	player.score	= 0
	player.reload	= 0
	invaders.mob = pygame.sprite.OrderedUpdates() # do these need to be ordered?
	for i in xrange(0, 4000, 80):
		next = pygame.sprite.Sprite()
		next.image = getsurface('enemy'+str((i/80)%3+1)+'a')
		next.rect = next.image.get_rect()
		next.n = i
		invaders.mob.add(next)
	invaders.shots = []
	invaders.movement = 7
	

# final inits
state = menu
laststate = game # just needs to be something else than state in the beginning
events = []

# main game loop
while state:

	# event handling
	for e in pygame.event.get():
		# quit event
		if e.type == QUIT:
			state = None

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
		initialize_game()
		#getogg('menu-confirm').play()
		state = game
		continue

	# back to menu
	if state is game and K_ESCAPE in events:
		#cleanup_game() # ?
		state = menu
	
	if (MUSIC['active']):
		if laststate != state:
			pygame.mixer.music.load(MUSIC[str(state.__name__)])
			pygame.mixer.music.play()
		laststate = state

	if state is game:
		# move player
		if K_LEFT in events and player.xUnits > 0:
			player.xUnits -= 1
		elif K_RIGHT in events and player.xUnits < 112:
			player.xUnits += 1

		# shoot player
		if K_SPACE in events and player.thunder > 0 and player.cooldown == 0:
			# TODO: workout a good balance between infinity shooting and having less ammo
			#player.thunder -= 1
			player.reload = 20
			player.cooldown = 7

			#player.shots.append((player.xUnits, 0))
			newshot = pygame.sprite.Sprite()
			newshot.image = getsurface('playershot')
			newshot.rect = newshot.image.get_rect()
			newshot.rect.topleft = (54+7*player.xUnits, 440)
			player.shots.add(newshot)
			getogg('laser_single').play()

		# It'z time to make the magicz...
		# noo, just doing the collision detection and dying in one line
		pygame.sprite.groupcollide(player.shots, invaders.mob, True, True)

	render() # waiting is done in render
	tick = tick % 3000 + 1 # avoid overflow


# tidy up and quit
pygame.quit()

