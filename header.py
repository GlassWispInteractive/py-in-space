# -*- coding: utf-8 *-*
import pygame
import sys

def draw_header(surface, life, shield, bonus, pts):
	header_surface = pygame.Surface((900,32))
	header_sprites = dict()
	for e in ['heart', 'shield', 'lightning', 'coins']:
		header_sprites[e] = pygame.image.load('res/' + e + '.png')
		header_sprites[e] = header_sprites[e].convert_alpha()
	header_surface.blit(header_sprites['heart'], (0, 0))
	header_surface.blit(header_sprites['shield'], (80, 0))
	header_surface.blit(header_sprites['lightning'], (164, 0))
	header_surface.blit(header_sprites['coins'], (860, 0))
	surface.blit(header_surface, (4,4))
