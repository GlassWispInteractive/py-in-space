# -*- coding: utf-8 *-*
import pygame
from pygame.locals import *
from pyinspacelib import *
from entity import entity
from shot import shot

class player(entity):

	Dir = enum(Idle=0, Left=1, Right=2)
	ShootCooldown = 15
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
		self.direction = player.Dir.Idle
		self.shooting = False

		self.cooldown = 0

	def tick(self, entities, events=[]):
		# decrease shoot cooldown every frame by 1
		# that way you can shoot every full second
		self.cooldown = self.cooldown-1 if self.cooldown>0 else 0

		# figure out wheter to fire
		for e in filter(lambda e: e.key == K_SPACE, events):
			if e.type == KEYUP:
				events.remove(e) # that event is handled
				self.shooting = False
			if e.type == KEYDOWN:
				events.remove(e) # that event is handled
				self.shooting = True
				if self.cooldown < 1:
					self.spawnShot(entities)
		# nothing was pressed but the key is being held down
		if self.shooting and self.cooldown < 1:
			self.spawnShot(entities)

		# figure out designated direction
		# last event per frame counts
		for e in events:
			if e.type == KEYUP and e.key == K_LEFT:
				self.left = False
			if e.type == KEYUP and e.key == K_RIGHT:
				self.right = False
			if e.type == KEYDOWN and e.key == K_LEFT:
				self.left = True
				self.lastdir = K_LEFT
			if e.type == KEYDOWN and e.key == K_RIGHT:
				self.right = True
				self.lastdir = K_RIGHT
			events.remove(e)

		# events should be empty now
		#if len(events) != 0: print "UNHANDLED EVENTS IN PLAYER CLASS", events
		#print "l:", self.left, "r:", self.right, "lastdir:", self.lastdir, "direction:", self.direction

		if self.left: self.direction = player.Dir.Left
		if self.right: self.direction = player.Dir.Right
		if not self.left and not self.right : self.direction = player.Dir.Idle
		if self.left and self.lastdir == K_LEFT: self.direction = player.Dir.Left
		if self.right and self.lastdir == K_RIGHT: self.direction = player.Dir.Right

		if self.offset > -55 * 7 and self.direction == player.Dir.Left:
			self.offset -= player.MovementSpeed
		elif self.offset < 55 * 7 and self.direction == player.Dir.Right:
			self.offset += player.MovementSpeed
		self.x = 418 + self.offset

	def render(self, surface):
		''' Render battle ship. '''
		surface.blit(self.model, (self.x, self.y))

	def spawnShot(self, entities):
		self.cooldown = player.ShootCooldown
		entities.append(shot(self))
