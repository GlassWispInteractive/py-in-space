# -*- coding: utf-8 *-*
import pygame
from pygame.locals import *
from pyinspacelib import *

border = (4,4)
offset = 90
textborder = 20
textcolor = (200,200,200)

def render_hud(surface, hudfont, player):
	''' Render Heads Up Display '''
	header_sprites = dict()
	for e in ['heart', 'shield', 'lightning', 'coin_stacks']:
		header_sprites[e] = getimageobject(e)
	surface.blit(header_sprites['heart'], (0+border[0], border[1]))
	surface.blit(header_sprites['shield'], (offset+border[0], border[1]))
	surface.blit(header_sprites['lightning'], (2*offset+border[0], border[1]))
	surface.blit(header_sprites['coin_stacks'], (864, border[1]))

	label = hudfont.render(str(player.health), 1, textcolor)
	labelPos = label.get_rect(left = 45, centery = textborder)
	surface.blit(label, labelPos)

	label = hudfont.render(str(player.shield), 1, textcolor)
	labelPos = label.get_rect(left = 135, centery = textborder)
	surface.blit(label, labelPos)

	label = hudfont.render(str(player.thunder), 1, textcolor)
	labelPos = label.get_rect(left = 225, centery = textborder)
	surface.blit(label, labelPos)

	label = hudfont.render(str(player.score), 1, textcolor)
	labelPos = label.get_rect(right = 855, centery = textborder)
	surface.blit(label, labelPos)
