# -*- coding: utf-8 *-*
import pygame
from pygame.locals import *
from pyinspacelib import *
from entity import entity
from shot import shot

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

