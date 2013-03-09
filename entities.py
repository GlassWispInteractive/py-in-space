# -*- coding: utf-8 *-*
import pygame
from pygame.locals import *
from pyinspacelib import *
from random import randint

class entity:
	Dir = enum(Idle=0, Left=1, Down=2, Up=3, Right=4)

	def __init__(self, (x, y), sprite):
		self.x = x
		self.y = y
		self.sprite = sprite
		self.model = getimageobject(self.sprite)
		self.dead = False

	def render(self, surface):
		surface.blit(self.model, (self.x, self.y))

	def die(self):
		self.dead = True


class player(entity):
	ShootCooldown = 15 # player can shoot every half second
	MovementSpeed = 7

	def __init__(self):
		self.sprite = "player"
		entity.__init__(self, (418, 440), self.sprite)
		self.health = 100
		self.shield = 100
		self.thunder = 0
		self.score = 0
		self.offset = 0

		self.left = False
		self.right = False
		self.lastdir = None
		self.direction = entity.Dir.Idle
		self.shooting = False
		self.cooldown = 0

	def tick(self, tick, entities, events):
		# decrease shoot cooldown every frame by 1
		# that way you can shoot every full second
		self.cooldown = self.cooldown - 1 if self.cooldown > 0 else 0

		# figure out wheter to fire
		for e in filter(lambda e: e.key == K_SPACE, events):
			if e.type == KEYUP:
				self.shooting = False
			if e.type == KEYDOWN:
				self.shooting = True
				self.spawnShot(entities)
		# nothing was pressed but the key is being held down
		if self.shooting:
			self.spawnShot(entities)

		# figure out designated direction
		for e in events:
			if e.key == K_LEFT: self.left = isDownPress(e)
			if e.key == K_RIGHT: self.right = isDownPress(e)
			if isDownPress(e): self.lastdir = e.key

		#print "l:", self.left, "r:", self.right, "lastdir:", self.lastdir, "direction:", self.direction

		if not self.left and not self.right : self.direction = entity.Dir.Idle
		if self.left: self.direction = entity.Dir.Left
		if self.right: self.direction = entity.Dir.Right
		if self.left and self.lastdir == K_LEFT: self.direction = entity.Dir.Left
		if self.right and self.lastdir == K_RIGHT: self.direction = entity.Dir.Right

		if self.offset > -56 * 7 and self.direction == entity.Dir.Left:
			self.offset -= player.MovementSpeed
		elif self.offset < 56 * 7 and self.direction == entity.Dir.Right:
			self.offset += player.MovementSpeed
		self.x = 418 + self.offset

	def spawnShot(self, entities):
		if self.cooldown < 1:
			self.cooldown = player.ShootCooldown
			entities.append(shot(self))


class enemy(entity):
	def __init__(self, x, y, type):
		self.sprite = "enemy" + str(type)
		entity.__init__(self, (x, y), self.sprite)
		self.direction = entity.Dir.Right

	def tick(self, tick, entities, events):
		pass
		# TODO: move and fire

def populate(count):
	enemies = list()
	border = (30,40) # (x,y)
	offset = (70,0) # (x,y)
	for i in range(1,count):
		enemies.append(enemy((i*offset[0]+border[0]), (i+border[1]), i%3+1))
	return enemies


class shot(entity):
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
		if isinstance(self.origin, player):
			y = y - orig_rect.height / 2 + model_rect.height / 2
			self.direction = entity.Dir.Up
		elif isinstance(self.origin, enemy):
			y = y + orig_rect.height / 2 - model_rect.height / 2
			self.direction = entity.Dir.Down

		entity.__init__(self, (x,y), self.sprite)

		print orig.sprite, "fired a shot at", x, y

	def tick(self, tick, entities, events):
		# fly up or down
		if self.direction == entity.Dir.Up:
			self.y -= shot.PlayerShotSpeed
		elif self.direction == entity.Dir.Down:
			self.y += shot.PlayerShotSpeed

		if self.x < -100 or self.x > 1000 or self.y < -100 or self.y > 600:
			self.die() # out of screen

		# TODO: check for collision and call die methods of self and target
		# Use this:
		#	Rect.colliderect(Rect): return bool - test if two rectangles overlap
