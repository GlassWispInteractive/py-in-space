# -*- coding: utf-8 *-*
import pygame
import sys


def draw_header(surface, life, shield, bonus, pts):
	header_sprites = dict()
	for e in ['heart', 'shield', 'lightning', 'coins']:
		header_sprites[e] = pygame.image.load('res/' + e + '.png')
	surface.blit(header_sprites['heart'], (4, 4))
	surface.blit(header_sprites['shield'], (84, 4))
	surface.blit(header_sprites['lightning'], (168, 4))
	surface.blit(header_sprites['coins'], (864, 4))
