# -*- coding: utf-8 *-*
import pygame
import entity

class header(entity):

	Mode = enum(Menu=0, Game=1)

	def __init__(self, mode):
		#entity.__init__(self, 0, 0, "empty")
		self.mode = Mode.mode

	def tick(self):
		pass

	def render(self, surface):
		header_surface = pygame.Surface((900,32))
		header_sprites = dict()
		for e in ['heart', 'shield', 'lightning', 'coin_stacks']:
			header_sprites[e] = pygame.image.load('res/' + e + '.png')
			header_sprites[e] = header_sprites[e].convert_alpha()
		header_surface.blit(header_sprites['heart'], (0, 0))
		header_surface.blit(header_sprites['shield'], (80, 0))
		header_surface.blit(header_sprites['lightning'], (164, 0))
		header_surface.blit(header_sprites['coin_stacks'], (860, 0))
		surface.blit(header_surface, (4,4))

	def die(self):
		""" state cannot die """
		pass
