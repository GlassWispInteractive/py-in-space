# -*- coding: utf-8 *-*
import pygame
from pyinspacelib import *
from entity import entity
from random import randint

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

