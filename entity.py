# -*- coding: utf-8 *-*
import pygame
from pygame.locals import *
from pyinspacelib import *

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
