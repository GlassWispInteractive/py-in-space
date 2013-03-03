# -*- coding: utf-8 *-*
import pygame
from pygame.locals import *
from pyinspacelib import *

class entity:

	SpriteImages = [
			"empty", "logo",
			"player", "playershot",
			"enemy1", "enemy2", "enemy3", "enemy4",
			"enemy1shot", "enemy2shot", "enemy3shot", "enemy4shot",
			"coin_bronze", "coin_gold", "coin_silver", "coin_stack", "coin_stacks",
			"award_bronze", "award_gold", "award_silver",
			"heart", "shield", "lightning",
			"fire", "diamond", "ruby"
			]

	Sprites = dict()
	for e in SpriteImages:
		Sprites[e] = getimageobject(e)

	def __init__(self, (x, y), model):
		self.x = x if x in range(0,900) else 0
		self.y = y if y in range(0,500) else 0
		self.model = model if model in self.__class__.SpriteImages else "empty"
		self.model = getimageobject(self.model)
		self.dead = False

	def tick(self, entities, events=[]):
		pass

	def render(self, surface):
		surface.blit(self.model, (self.x, self.y))

	def die(self):
		self.dead = True
