# -*- coding: utf-8 *-*
import pygame
from pygame.locals import *
from pyinspacelib import *
from random import randint

class Entity:
	idle, left, down, up, right = range(5)

	def __init__(self, (x, y), sprite):
		self.x = x
		self.y = y
		self.sprite = sprite
		self.model = getimageobject(self.sprite)
		self.dead = False

	def render(self, surface):
		surface.blit(self.model, (self.x, self.y))

	def get_rect(self):
		rect = self.model.get_rect()
		rect.topleft = (self.x, self.y)
		return rect

	def die(self):
		self.dead = True

class Player(Entity):
	ShootCooldown = 15 # player can shoot every half second
	MovementSpeed = 7

	def __init__(self):
		Entity.__init__(self, (418, 440), "player")
		self.health = 100
		self.shield = 100
		self.thunder = 0
		self.score = 0
		self.offset = 0

		self.left = False
		self.right = False
		self.lastdir = None
		self.direction = Entity.idle
		self.shooting = False
		self.cooldown = 0

	def tick(self, tick, entities, events):
		# decrease shoot cooldown every frame by 1
		# that way you can shoot every full second
		self.cooldown = self.cooldown - 1 if self.cooldown > 0 else 0

		# figure out wheter to fire
		for e in [e for e in events if e.key == K_SPACE]:
			if e.type == KEYUP:
				self.shooting = False
			if e.type == KEYDOWN:
				self.shooting = True
				self.spawn_shot(entities)
		# nothing was pressed but the key is being held down
		if self.shooting:
			self.spawn_shot(entities)

		# figure out designated direction
		for e in events:
			if e.key == K_LEFT: self.left = isDownPress(e)
			if e.key == K_RIGHT: self.right = isDownPress(e)
			if isDownPress(e): self.lastdir = e.key

		if not self.left and not self.right: self.direction = Entity.idle
		if self.left: self.direction = Entity.left
		if self.right: self.direction = Entity.right
		if self.left and self.lastdir == K_LEFT: self.direction = Entity.left
		if self.right and self.lastdir == K_RIGHT: self.direction = Entity.right

		if self.offset > -56 * 7 and self.direction == Entity.left:
			self.offset -= Player.MovementSpeed
		elif self.offset < 56 * 7 and self.direction == Entity.right:
			self.offset += Player.MovementSpeed
		self.x = 418 + self.offset

	def spawn_shot(self, entities):
		if self.cooldown < 1:
			self.cooldown = Player.ShootCooldown
			entities.append(Shot(self))

class Enemy(Entity):
	def __init__(self, x, y, type):
		self.sprite = "enemy" + str(type)
		Entity.__init__(self, (x, y), self.sprite)
		self.direction = Entity.right

	def tick(self, tick, entities, events):
		pass
		# TODO: move and fire

	def populate(count):
		enemies = list()
		border = (30,40) # (x,y)
		offset = (70,0) # (x,y)
		for i in range(1,count):
			enemies.append(Enemy((i*offset[0]+border[0]), (i+border[1]), i%3+1))
		return enemies

	populate = staticmethod(populate)

class Shot(Entity):
	PlayerShotSpeed = 7
	EnemyShotSpeed = 8

	def __init__(self, orig):

		self.origin = orig
		orig_rect = self.origin.model.get_rect()

		self.sprite = self.origin.sprite + "shot"
		model = getimageobject(self.sprite)
		model_rect = model.get_rect()

		x = int(self.origin.x + orig_rect.width / 2 - model_rect.width/2 + 1)

		y = self.origin.y
		if isinstance(self.origin, Player):
			y = y - orig_rect.height / 2 + model_rect.height / 2
			self.direction = Entity.up
		elif isinstance(self.origin, Enemy):
			y = y + orig_rect.height / 2 - model_rect.height / 2
			self.direction = Entity.down

		Entity.__init__(self, (x,y), self.sprite)

		print orig.sprite, "fired a shot at", x, y

	def tick(self, tick, entities, events):
		# fly up or down
		if self.direction == Entity.up:
			self.y -= Shot.PlayerShotSpeed
		elif self.direction == Entity.down:
			self.y += Shot.PlayerShotSpeed

		if self.x < -100 or self.x > 1000 or self.y < -100 or self.y > 600:
			self.die() # out of screen

		# TODO: check for collision and call die methods of self and target
		# Use this: Rect.colliderect(Rect): return bool - test if two rectangles overlap

		enemies = [e for e in entities if isinstance(e, Enemy)]
		shots = [s for s in entities if isinstance(s, Shot)]

		for enemy in enemies:
			enemy_rect = enemy.get_rect()
			for shot in shots:
				shot_rect = shot.get_rect()
				if enemy_rect.colliderect(shot_rect):
					enemy.die()
					shot.die()
					print "enemy killed"
