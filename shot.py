# -*- coding: utf-8 *-*
import pygame
from pyinspacelib import *

from entity import entity
import player
import enemy

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
		if isinstance(self.origin, player.player):
			y = y - orig_rect.height / 2 + model_rect.height / 2
			self.direction = entity.Dir.Up
		elif isinstance(self.origin, enemy.enemy):
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
