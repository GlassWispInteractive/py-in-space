# -*- coding: utf-8 *-*
import pygame
from pyinspacelib import *
from entity import entity

class shot(entity):
	pass

	def __init__(self, orig):
		self.origin = orig

	def tick(self, entities, eventList):

		if self.model[:-4] == "player":
			self.y -= 7
		elif self.model[:-4] == "enemy":
			self.y += 7

	def render(self, surface):
		graphics.blit(self.models, (x, y))
