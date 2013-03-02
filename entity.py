# -*- coding: utf-8 *-*
import pygame

class entity:

	SpriteImages = [
			"empty", "logo",
			"player", "playershot",
			"enemy1", "enemy1shot", "enemy2", "enemy2shot", "enemy3", "enemy3shot", "enemy4", "enemy4shot",
			"coin_bronze", "coin_gold", "coin_silver", "coin_stack", "coin_stacks",
			"award_bronze", "award_gold", "award_silver",
			"heart", "shield", "lightning",
			"fire", "diamond", "ruby"
			]

	Sprites = dict()
	for e in SpriteImages:
		Sprites[e] = pygame.image.load('res/' + e + '.png')

	def __init__(self, (x, y), model):
		self.x = x if x in range(0,900) else 0
		self.y = y if y in range(0,500) else 0
		self.model = model if model in ["player","enemy","playershot","enemyshot","star"] else "empty"
		self.model = pygame.image.load('res/' + self.model + '.png')
		self.dead = False

	def tick(self):
		pass

	def render(self, surface):
		surface.blit(self.model, (self.x, self.y))

	def die(self):
		self.dead = True
