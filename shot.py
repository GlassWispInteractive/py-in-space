# -*- coding: utf-8 *-*
import entity

class shot(entity):
	pass

	def __init__(self, x, y, model):
		entity.__init__(self, x, y, model)

	def tick(self):
		if self.model[:-4] == "player":
			self.y -= 7
		elif self.model[:-4] == "enemy":
			self.y += 7

	def render(self, surface):
		graphics.blit(renderImg['playershot'], (418+self.offset+29, 440-23))
