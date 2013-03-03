# -*- coding: utf-8 *-*
import pygame
from pygame.locals import *
from entity import entity
from enum import enum

class player(entity):

	Dir = enum(Idle=0, Left=1, Right=2)
	ShootCooldown = 60 # that way the player can shoot every 2 seconds
	MovementSpeed = 7

	def __init__(self, health, shield, thunder, score):
		entity.__init__(self, (418, 440), "player")
		self.health = health
		self.shield = shield
		self.thunder = thunder
		self.score = score
		self.offset = 0

		self.left = False
		self.right = False
		self.lastdir = None
		self.direction = player.Dir.Idle
		self.shooting = False

		self.cooldown = player.ShootCooldown

	def tick(self, entities, events=[]):
		# decrease shoot cooldown every frame by 1
		# that way you can shoot every full second
		self.cooldown = self.cooldown-1 if self.cooldown>0 else 0

		# figure out wheter to fire
		if any(e.type == KEYUP and e.key == K_SPACE for e in events):
			events.remove(e) # that event is handled
			shooting = False
		if any(e.type == KEYDOWN and e.key == K_SPACE for e in events):
			events.remove(e) # that event is handled
			shooting = True
			if self.cooldown < 1:
				spawnShot(entities)
		# nothing was pressed but the key is being held down
		if self.shooting and self.cooldown < 1:
			spawnShot(entities)

		# figure out designated direction
		# last event per frame counts
		for e in filter(lambda e: e.key in [K_LEFT, K_RIGHT], events):
			if e.type == KEYUP and e.key == K_LEFT: self.left = False
			if e.type == KEYUP and e.key == K_RIGHT: self.right = False
			if e.type == KEYDOWN and e.key == K_LEFT:
				self.left = True
				self.lastdir = K_LEFT
			if e.type == KEYDOWN and e.key == K_RIGHT:
				self.right = True
				self.lastdir = K_RIGHT


		if self.left: self.direction = player.Dir.Left
		if self.right: self.direction = player.Dir.Right

		if self.left and self.lastdir == K_LEFT: self.direction = player.Dir.Left
		if self.right and self.lastdir == K_RIGHT: self.direction = player.Dir.Right


		if self.offset > -55 * 7 and self.direction == player.Dir.Left:
			self.offset -= player.MovementSpeed
		elif self.offset < 55 * 7 and self.direction == player.Dir.Right:
			self.offset += player.MovementSpeed

	def render(self, surface):
		''' Render battle ship. '''
		surface.blit(self.model, (418+self.offset, 440))

	def spawnShot(self, entities):
		self.cooldown = player.ShootCooldown
		entities.append(shot(self))
