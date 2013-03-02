# -*- coding: utf-8 *-*
import entity

class player(entity):
	pass

	def __init__(self, x, y, model, health, shield, thunder, score):
		entity.__init__(self, 418, 440, model)
		self.health = health
		self.shield = shield
		self.thunder = thunder
		self.score = score
		self.offset = 0
		self.shootCooldown = 30

	def tick(self, events):
		if any(e.type == KEYDOWN and e.key == K_UP for e in eventList):
			shoot = True

		# iterate over events
		for e in eventList:
			if e.type == KEYDOWN: trigger = e.key
			elif e.type == KEYUP and e.key == trigger: trigger = None

		if offset > -55 * 7 and trigger == K_LEFT: offset -= 7
		elif offset < 55 * 7 and trigger == K_RIGHT: offset += 7



	def render(self, surface):
		''' Render battle ship. '''
		surface.blit(renderImg['player'], (418+self.offset, 440))
