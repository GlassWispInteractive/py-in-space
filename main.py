#!/usr/bin/env python
# -*- coding: utf-8 *-*
import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE, K_RETURN, K_ESCAPE, K_p, KEYUP, KEYDOWN, QUIT
from random import randint, randrange
import os.path as path
from glob import glob

DEBUG = False
X = 900
Y = 500
FPS = 30
R = lambda x: int(round(x)) # wrapper for rounding

pygame.init()
pygame.mixer.init() # exe doesnt work without it and it doesnt hurt on linux

MENU_FONT = pygame.font.Font("res/starcraft.ttf", 22)
HUD_FONT = pygame.font.Font("res/pixel.ttf", 20)
MSG_FONT = pygame.font.Font("res/pixel.ttf", 54)
LOST_FONT = pygame.font.Font("res/pixel.ttf", 120)

MUSIC = {	'active': True,
			'menu': "res/ObservingTheStar.ogg",
			'game': "res/DataCorruption.ogg",
			'lost': "res/TragicAmbient.ogg"
		}
TIMER = pygame.time.Clock()
tick = 0

MOVEMENT_KEYS = [K_LEFT, K_RIGHT, K_SPACE]
CONTROL_KEYS = [K_RETURN, K_ESCAPE, K_p]
KEYS = MOVEMENT_KEYS + CONTROL_KEYS

# pygame inits
if DEBUG: print("initializing")
pygame.display.set_caption('PyInSpace!')
DISPLAY = pygame.display.set_mode((X, Y))

# load all sprites at the beginning
SPRITES = { path.basename(path.splitext(s)[0])
			: pygame.image.load(s).convert_alpha() for s in glob("res/*.png") }

# load sounds
SOUNDS = {s : pygame.mixer.Sound('res/' + str(s) + '.ogg')
			for s in [ 'laser_single.ogg', 'confirm.ogg', 'menu-confirm.ogg',
				'playerdeath.ogg', 'playerhit.ogg', 'enemydeath.ogg', 'ufodeath.ogg']
		 }

# helper functions
getsurface = lambda s: SPRITES[s]
getogg = lambda s: SOUNDS[s] if s in SOUNDS else pygame.mixer.Sound('res/' + s + '.ogg')
playsound = lambda s: getogg(s).play()
def PyInSpaceSprite(pic='empty', x=0, y=0):
	newsprite = pygame.sprite.Sprite()
	newsprite.image = getsurface(pic)
	newsprite.rect = newsprite.image.get_rect()
	newsprite.rect.topleft = (x,y)
	return newsprite
def draw_text(text, font, pos, color):
	label = font.render(text, 1, color)
	posi = label.get_rect(centerx = pos[0], centery = pos[1])
	DISPLAY.blit(label, posi)


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
			if not hasattr(f, 'render') or state in f.render:
				f()
		TIMER.tick(FPS)
		pygame.display.update()
render.funcs = []


@render
def starsky():
	''' render astonishing star sky. '''
	if tick % 100 == 0:
		for _ in range(randint(0, 25 - len(starsky.stars))):
			starsky.stars.append((randint(R(X*0.02), R(X*0.98)), randint(-Y, 0), 0))
	# update and delete stars
	if tick % 3 == 0:
		starsky.stars = [(x, y + 1, z if z == 0 or z > 190 else z + 7)
						for x, y, z in starsky.stars if y < Y]
	if tick % 100 == 0:
		r = randint(0, len(starsky.stars) - 1)
		if starsky.stars[r][2] == 0: starsky.stars[r] = (starsky.stars[r][0], starsky.stars[r][1], 1)

	# render stars
	for x, y, z in starsky.stars:
		b = 60 + z % 190
		pygame.draw.circle(DISPLAY, (b, b, b), (x, y), 2)
# mode doesn't matter for the bg, so initialsing it once is ok
starsky.stars = [(randint(R(X*0.02), R(X*0.98)), randint(R(Y*0.1), R(Y*0.9)), 0) for _ in range(randint(8, 12))]


@render
def game():
	''' Render Heads Up Display '''
	info = list(zip(list(map(getsurface, ['heart', 'lightning', 'coin_stacks'])),
			[0, R(X*0.0888), R(X*0.9111)],
			list(map(str, [player.health, player.thunder, player.score]))))
	for img, px, txt in info:
		DISPLAY.blit(img, (R(X*0.0044)+px, R(Y*0.008)))
		label = HUD_FONT.render(txt, 1, (200, 200, 200))
		pos = label.get_rect(left = R(X*0.0444)+px, centery = R(Y*0.04))
		DISPLAY.blit(label, pos)
game.render = [game]


@render
def lost():
	global state

	# game over screen
	if lost.show > 0:
		info = zip( ["Spring von der Bruecke!", "GAME OVER!", "Your Score:", str(player.score)],
					[MSG_FONT, LOST_FONT, MSG_FONT, MSG_FONT],
					[(R(X*0.5), R(X*0.15)), (R(X*0.5),R(Y*0.4)), (R(X*0.5),R(Y*0.7)), (R(X*0.5), R(Y*0.8))],
					[(200,20,20), (200,50,50), (200,200,200), (200,200,200)]
				)
		for text, font, pos, color in info:
			draw_text(text, font, pos, color)
		lost.show -= 1

		DISPLAY.blit(getsurface('danny'), (R(X*0.05), R(Y*0.6)))

		if lost.show == 0:
			state = menu
	# end game
	elif player.health < 0:
		playsound('playerdeath')
		lost.show = FPS*20 # show for 20 seconds at max
		state = lost
lost.render = [game, lost]
lost.show = 0


@render
def milestone():
	''' shows milestone '''
	# show level label
	if milestone.show > 0:
		milestone.show -= 1
		label = MSG_FONT.render("LEVEL " + str(milestone.level+1), 1, (200, 50, 50))
		pos = label.get_rect(centerx = R(X*0.5), centery = R(Y*0.7))
		DISPLAY.blit(label, pos)

	# leave if next level isn't reached yet
	if player.score < milestone.limits[milestone.level]: return

	# initializing
	milestone.level += 1
	milestone.show = R(FPS*1.5)
	milestone.limits.pop(0)

	# less shots
	player.thunderMax = 9 - milestone.level
milestone.render = [game]


@render
def menu():
	''' render the menu '''
	logorect = getsurface('logo').get_rect()
	logorect.center = (R(X*0.5), R(Y*0.3))
	DISPLAY.blit(getsurface('logo'), logorect)
	pygame.draw.rect(DISPLAY, (192, 192, 192), (R(X*0.2778), R(Y*0.6), R(X*0.4444), R(Y*0.12)))
	pygame.draw.rect(DISPLAY, (80, 80, 80), (R(X*0.2833), R(Y*0.61), R(X*0.4333), R(Y*0.1)))
	label = MENU_FONT.render("Press ENTER to start", 1, (200, 200, 200))
	pos = label.get_rect(centerx = R(X*0.5), centery = R(Y*0.66))
	DISPLAY.blit(label, pos)
menu.render = [menu]
menu.notgame = 0 # blocker. you have to wait a second after you come from the game over screen


@render
def player():
	''' Player function which renders the player and holds its state '''
	# reload thunder
	player.reload += 1
	if tick % 150 == 0 and player.thunder < player.thunderMax: # give a shot every 5 seconds
		player.thunder += 1 % (player.thunderMax+1)

	if player.reload == 99 and player.thunder < player.thunderMax:
		player.thunder += 1
		player.reload = 0

	# release cooldown
	if player.cooldown > 0:
		player.cooldown -= 1

	# move shots
	for shot in player.shots:
		shot.rect.y -= player.shotspeed
		if shot.rect.y < -20:
			player.shots.remove(shot)

	# rendering
	player.grp.draw(DISPLAY)
	player.shots.draw(DISPLAY)
player.xUnits = 56
#player.speed = 7
player.shotspeed = 7
player.render = [game]


@render
def invaders():
	''' Renders enemies and their shots '''
	def move(e, x, y):
		e.pos = (e.pos[0] + x, e.pos[1] + y)

	# no rendering if not in-game
	if state is not game or len(invaders.mob)+len(invaders.corpses) < 1: return

	# This method also needs to work if there are no living enemies.
	# After the player killed the last enemy on the screen there are
	# only entities in invader.corpses for about half a second.
	# So we only move stuff if there is at least 1 living invader.
	if invaders.mob:
		# mob variables
		xMin = min(map(lambda e: e.pos[0], invaders.mob))
		xMax = max(map(lambda e: e.pos[0], invaders.mob))
		yMax = max(map(lambda e: e.pos[1], invaders.mob))

		if tick % 10 == 0:
			if invaders.dir == (True, 0):
				if xMax >= 150: invaders.dir = (True, 3)
			elif invaders.dir == (False, 0):
				if xMin <= 0: invaders.dir = (False, 3)
			else:
				a, b = invaders.dir
				invaders.dir = (not a, b - 1)

		# move all invaders and corpses
		for mob in [invaders.mob, invaders.corpses]:
			for inv in mob:
				x, y = inv.pos
				# move
				if tick % 10 == 0:
					if invaders.dir == (True, 0):
						if xMax < 150: x += 1
					elif invaders.dir == (False, 0):
						if xMin > 0: x -= 1
					else:
						if yMax < 150: y += 1
					inv.pos = (x, y)
				inv.rect.center = (70+5*x, 100+2*y)
				#inv.rect.center = (R(X*0.0778)+R(X*0.005)*x, R(Y*0.2)+R(Y*0.004)*y) # non-optimal..

		# animate and draw the living invaders
		for inv in invaders.mob:
			inv.animcnt += randint(1,1) # animation: (0,0)=none  (0,1)=indiviual (1,1)=uniform
			if inv.animcnt >= 20:
				inv.image = getsurface('enemy'+str(inv.kind)+'a'+'3')
			if inv.animcnt >= 40:
				inv.image = getsurface('enemy'+str(inv.kind)+'b'+'3')
				inv.animcnt = 0
		invaders.mob.draw(DISPLAY)

	# timeout for corpses
	for corp in invaders.corpses:
		if corp.ttl > 0:
			corp.ttl -= 1
		else:
			invaders.corpses.remove(corp)
	invaders.corpses.draw(DISPLAY)

	# move and render all shots
	for shot in invaders.shots:
		shot.rect.y += invaders.shotspeed
		if shot.rect.y > Y+20:
			invaders.shots.remove(shot)
	invaders.shots.draw(DISPLAY)
#invaders.speed = 7
invaders.render = [game]
invaders.shotspeed = 9


@render
def invaders_spawn():
	#if len(invaders.mob) > 0 or len(invaders.shots) > 0 or len(player.shots) > 0: return
	if (len(invaders.mob) + len(invaders.corpses)) > 0: return

	# full reload
	player.thunder = player.thunderMax

	# new invaders
	#for x in range(0,150,15):
	for x in range(0,R(X*0.1667),R(X*0.0167)):
		#for y in range(0, 90, 15):
		for y in range(0, R(Y*0.18), R(Y*0.03)):
			kind = y/R(Y*0.06)+1 # TODO: does this work on any resolution?
			anim = 'a'
			newenemy = PyInSpaceSprite('enemy'+str(kind)+anim+'3')
			newenemy.kind = kind
			newenemy.anim = anim
			newenemy.pos = (x, y) # pos is used to calculate the actual xy coords
			newenemy.ttl = -1
			newenemy.animcnt = 0
			invaders.mob.add(newenemy)
invaders_spawn.render = [game]


@render
def invaders_shots_spawn():
	if len(invaders.mob) == 0 or tick % 10 == 0: return

	# get the list of the bottom invaders
	bottom = {}
	for mob in invaders.mob:
		x, y = mob.pos
		if x not in bottom or y > bottom[x][1]:
			bottom[x] = (x, y)

	# randomly creates a shot
	if bottom and randint(1, 1000) > (800 - (milestone.level * 5)): # default 995
			elem = bottom.items()[randint(0, len(bottom)-1)][1]
			newshot = PyInSpaceSprite('enemyshot')
			newshot.rect.center = (70+5*elem[0], 100+2*elem[1]+8)
			#newshot.rect.center = (R(X*0.0778)+R(X*0.005)*elem[0], R(Y*0.2)+R(Y*0.004)*elem[1]+8) # non-optimal
			invaders.shots.add(newshot)
			if DEBUG: print('enemy fired a shot at ' + str(newshot.rect.center))
invaders_shots_spawn.render = [game]


@render
def ufo():
	if ( (len(ufo.group)+len(ufo.corpses)) == 0
	  and tick % (FPS*5) == 0
	  and randint(1, 1000) > 800): # 20% every 5 seconds
		newufo = PyInSpaceSprite('ufo')
		newufo.dir = randrange(-1,2,2) # -1=R->L 1=L->R
		newufo.rect.x = -64 if newufo.dir > 0 else X
		newufo.rect.y = R(Y*0.092)
		ufo.group.add(newufo)
		if DEBUG: print('ufo spawned')

	for u in ufo.group:
		if u.rect.x < -84 or u.rect.x > X+20:
			ufo.group.remove(u)
		else:
			u.rect.x += (ufo.speed * u.dir)

	for c in ufo.corpses:
		if c.ttl < 1:
			ufo.corpses.remove(c)
		else:
			c.ttl -= 1

	ufo.group.draw(DISPLAY)
	ufo.corpses.draw(DISPLAY)
ufo.render = [game]
ufo.speed = R(X*0.00556)


def initialize_game():
	if DEBUG: print("initializing game mode")
	player.health     = 3
	player.thunder    = 9 # current thunder
	player.thunderMax = 9 # maximum thunder in current game
	player.shots      = pygame.sprite.Group()
	player.cooldown   = 0
	player.score      = 0
	player.reload     = 0
	player.sprite     = PyInSpaceSprite('player', 0, R(Y*0.88))
	player.grp      = pygame.sprite.Group()
	player.grp.add(player.sprite)
	invaders.dir = (True, 0)
	invaders.mob = pygame.sprite.Group()
	invaders.corpses = pygame.sprite.Group()
	invaders.shots = pygame.sprite.Group()
	ufo.group = pygame.sprite.Group()
	ufo.corpses = pygame.sprite.Group()
	milestone.level = 0 # initially show level 1
	milestone.limits = [10, 50, 100, 200, 500, 1000, 2000, 5000]
	milestone.show = R(FPS*1.5)


def adjust_music(state):
	if adjust_music.laststate != state:
		try:
			#pygame.mixer.music.fadeout(10) # TODO: BLOCKS WHILE FADING OUT
			pygame.mixer.music.load(MUSIC[str(state.__name__)])
			pygame.mixer.music.play(-1) # loop indefinitely
			if DEBUG: print("current music: %s" % MUSIC[str(state.__name__)])
			adjust_music.laststate = state
		except AttributeError:
			pass


# final inits
state = menu
adjust_music.laststate = game # just needs to be something else than state
events = []
pause = False

if DEBUG: print("entering main game loop")
# main game loop
while state:

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
	if state is menu and menu.notgame < 1 and K_RETURN in events:
		if DEBUG: print("entering game")
		initialize_game()
		#playsound('menu-confirm')
		state = game
		continue
	else:
		menu.notgame = menu.notgame - 1 if menu.notgame > 0 else 0

	# back to menu
	if state is game and K_ESCAPE in events:
		#cleanup_game() # ?
		if DEBUG: print("leaving game")
		state = menu
		continue

	if state is lost and (K_RETURN in events or K_ESCAPE in events):
		lost.show = 0
		state = menu
		menu.notgame = FPS # you have to wait a sec when u leave the lost screen by keypress
		continue

	if (MUSIC['active']):
		adjust_music(state)

	if state is game:
		if K_p in events:
			# pause mode
			pause = True
			label = LOST_FONT.render("PAUSED", 1, (200,50,50))
			pos = label.get_rect(centerx = R(X*0.5), centery = R(Y*0.5))
			DISPLAY.blit(label, pos)
			pygame.display.update()

			# wait for unpause
			while(pause):
				e = pygame.event.wait()
				if e.type == KEYDOWN and e.key == K_p:
					pause = False
			events.remove(K_p)

		# move player
		if K_LEFT in events and player.xUnits > 0:
			player.xUnits -= 1
		elif K_RIGHT in events and player.xUnits < 112:
			player.xUnits += 1
		player.sprite.rect.x = 32 + 7 * player.xUnits
		#player.sprite.rect.x = R(X*0.03556) + R(X*0.00778) * player.xUnits

		# player shoots
		if K_SPACE in events and player.thunder > 0 and player.cooldown == 0:
			player.thunder -= 1
			player.cooldown = 7
			newshot = PyInSpaceSprite('playershot', (55+7*player.xUnits), 440)
			#newshot = PyInSpaceSprite('playershot', (R(X*0.03556)+R(X*0.00778)*player.xUnits+23), R(Y*0.88))
			player.shots.add(newshot)
			if DEBUG: print("player fired a shot at %s" % str(newshot.rect.center))
			playsound('laser_single')

		# It'z time to make the magicz...
		# noo, just doing the collision detection in one line
		enemies_hit = pygame.sprite.groupcollide(invaders.mob, player.shots, False, True)
		player.score += len(enemies_hit)
		player.thunder = min(player.thunderMax, (len(enemies_hit) + player.thunder))
		if len(enemies_hit) > 0:
			player.reload = 0
		for enem in enemies_hit:
			playsound('enemydeath')
			invaders.mob.remove(enem)
			enem.image = getsurface('dead3')
			enem.rect = enem.image.get_rect() # potentially wider dead3 sprite
			enem.kind = 3 # dead3 is as wide as enemy3
			enem.ttl = R(FPS/3) # show explosion for 1/3 second
			invaders.corpses.add(enem)

		# ufo collision detection
		ufocollide = pygame.sprite.groupcollide(ufo.group, player.shots, False, True)
		if len(ufocollide) > 0:
			for u in ufocollide.keys():
				playsound('ufodeath')
				ufo.group.remove(u)
				u.image = getsurface('ufodead')
				u.ttl = R(FPS*1.5)
				ufo.corpses.add(u)
			player.health = player.health + 1 if player.health <= 10 else player.health
			player.score += 10

		# enemy shots hit the player
		playercollide = pygame.sprite.spritecollide(player.sprite, invaders.shots, True)
		if len(playercollide) > 0:
			if DEBUG: print("Hit player!")
			playsound('playerhit')
			player.health -= 1

	if DEBUG: show_fps(a)
	render() # waiting is done in render
	tick = tick % (FPS*100) + 1 # avoid overflow

pygame.quit()
