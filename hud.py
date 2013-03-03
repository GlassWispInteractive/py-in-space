# -*- coding: utf-8 *-*
import pygame

def render_hud(surface, player):
	''' Render Heads Up Display '''
	header_surface = pygame.Surface((900,32))
	header_sprites = dict()
	for e in ['heart', 'shield', 'lightning', 'coin_stacks']:
		header_sprites[e] = pygame.image.load('res/' + e + '.png')
		header_sprites[e] = header_sprites[e].convert_alpha()
	header_surface.blit(header_sprites['heart'], (0, 0))
	header_surface.blit(header_sprites['shield'], (80, 0))
	header_surface.blit(header_sprites['lightning'], (164, 0))
	header_surface.blit(header_sprites['coin_stacks'], (860, 0))

	# TODO: 4 attribute als text rendern

	surface.blit(header_surface, (4,4))
