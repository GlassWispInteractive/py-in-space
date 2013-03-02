# -*- coding: utf-8 *-*
import entity
import enum

class enemy(entity):

	Dir = enum(Left=1, Right=2)

	def __init__(self, x, y, model, health=100, dir=enemy.Dir.Right):
		entity.__init__(self, x, y, model)
		self.health = health

	def tick(self):
		pass

	def render(self, surface):
		pass

	def __eq__(self, other):
		return True if self.x == other.x
			and self.y == other.y
			and self.model == other.model
			and self.health == other.health
		else False
