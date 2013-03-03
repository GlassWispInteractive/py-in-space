# -*- coding: utf-8 *-*
import pygame
from entity import entity
from enum import enum
import pyinspacelib
from random import randint

class enemy(entity):

	Dir = enum(Idle=0, Left=1, Right=2)
	#EnemyType = enum(1=1, 2=2, 3=3, 4=4)

	def __init__(self, x, y, kind, health=100):
		self.health = health
		self.direction = enemy.Dir.Right # self.__class__.Dir.Right
		sprite = "enemy" + str(kind)	# + randint(1, 4)
		entity.__init__(self, (x, y), sprite)

	def tick(self, entities, eventList):
		pass

	def render(self, surface):
		surface.blit(self.model, (self.x, self.y))

def populate(count):
	enemies = list()
	border = (30,20) # (x,y)
	offset = (10,10) # (x,y)
	for i in range(1,count):
		enemies.append(enemy((i%offset[0]+border[0]), (i*offset[1]+border[1]), i%4+1))
	return enemies
