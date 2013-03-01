# -*- coding: utf-8 *-*

class entity:

	def __init__(self, model, x, y):
		self.model = model if model in ["player","enemy","playershot","enemyshot","star"]
		self.x = x if x in range(0,900) else 0
		self.y = y if y in range(0,500) else 0
		pass

	def tick(self)
		if self.model[-4:] == "shot":
			if self.model[:-4] == "player":
				self.y -= 7
			elif self.model[:-4] == "enemy":
				self.y += 7

	def render(self, surface):

