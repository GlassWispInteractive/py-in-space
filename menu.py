# -*- coding: utf-8 *-*
import pygame
from pygame.locals import *
from pyinspacelib import *

def render_menu(surface, textfont):
	''' Render start screen '''

	surface.blit(getimageobject('logo'), (157, 100))
	pygame.draw.rect(surface, (192, 192, 192), (250, 300, 400, 60))
	pygame.draw.rect(surface, (80, 80, 80), (255, 305, 390, 50))

	# label
	label = textfont.render("Press ENTER to start", 1, (200,200,200))
	labelPos = label.get_rect(centerx = 450, centery = 330)
	surface.blit(label, labelPos)
