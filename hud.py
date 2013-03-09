# -*- coding: utf-8 *-*
import pygame
from pygame.locals import *
from pyinspacelib import *

def render_hud(surface, hudfont, player, textPadding=20, textColor=(200,200,200), iconPadding=4):
	''' Render Heads Up Display '''
	header_sprites = dict()
	for e in ['heart', 'shield', 'lightning', 'coin_stacks']:
		header_sprites[e] = getimageobject(e)
	surface.blit(header_sprites['heart'], (0+iconPadding, iconPadding))
	surface.blit(header_sprites['shield'], (1*90+iconPadding, iconPadding))
	surface.blit(header_sprites['lightning'], (2*90+iconPadding, iconPadding))
	surface.blit(header_sprites['coin_stacks'], (864, iconPadding))

	label = hudfont.render(str(player.health), 1, textColor)
	label_pos = label.get_rect(left = 0.5*90, centery = textPadding)
	surface.blit(label, label_pos)

	label = hudfont.render(str(player.shield), 1, textColor)
	label_pos = label.get_rect(left = 1.5*90, centery = textPadding)
	surface.blit(label, label_pos)

	label = hudfont.render(str(player.thunder), 1, textColor)
	label_pos = label.get_rect(left = 2.5*90, centery = textPadding)
	surface.blit(label, label_pos)

	label = hudfont.render(str(player.score), 1, textColor)
	label_pos = label.get_rect(right = 9.5*90, centery = textPadding)
	surface.blit(label, label_pos)

