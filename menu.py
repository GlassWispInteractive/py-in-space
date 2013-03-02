# -*- coding: utf-8 *-*
import entity

class menu(entity):

	def __init__(self, x, y, model, health, shield, thunder, score):
		entity.__init__(self, 418, 440, model)
		self.health = health
		self.shield = shield
		self.thunder = thunder
		self.score = score

	def tick(self):
		pass

	def render(self, surface):
		''' Render start screen. '''
		graphics.blit(renderImg['logo'], (157, 100))
		pygame.draw.rect(graphics, (192, 192, 192), (250, 300, 400, 60))
		pygame.draw.rect(graphics, (80, 80, 80), (255, 305, 390, 50))

		# label
		label = textfont.render("Start game!", 1, (200,200,200))
		labelPos = label.get_rect(centerx = 450, centery = 330)
		graphics.blit(label, labelPos)
