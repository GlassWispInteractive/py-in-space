# -*- coding: utf-8 *-*
import pygame
from pyinspacelib import *

from entity import entity
import player
import enemy

class shot(entity):

	ShotSpeed = 7

	def __init__(self, orig):

		self.origin = orig
		orig_rect = self.origin.model.get_rect()

		self.sprite = self.origin.sprite + "shot"
		model = getimageobject(self.sprite)
		model_rect = model.get_rect()

		x = int(self.origin.x + orig_rect.width / 2 - model_rect.width/2 + 1)

		y = self.origin.y
		if isinstance(self.origin, player.player):
			y -= orig_rect.height/2
			y += model_rect.height/2
		elif isinstance(self.origin, enemy.enemy):
			y += orig_rect.height/2
			y -= model_rect.height/2

		entity.__init__(self, (x,y), self.sprite)

		print orig.sprite, "fired a shot at", x, y

	def tick(self, tick, entities, events):
		# fly up or down
		if isinstance(self.origin, player.player):
			self.y -= shot.ShotSpeed
			if self.y < -100:
				self.die()
		elif isinstance(self.origin, enemy.enemy):
			self.y += shot.ShotSpeed
			if self.y > 600:
				self.die()

		# TODO: check for collision and call die methods of self and target
		# also die when flying out of the screenq

	# inherited render and die methods work fine
