# -*- coding: utf-8 *-*

import pygame
from pygame.locals import *

# No game logic here, just helper functions

def getimagepath(img):
	return 'res/' + str(img) + '.png'

def getimageobject(img):
	if img[-4:] == ".png":
		return pygame.image.load(img)
	else:
		return pygame.image.load(getimagepath(img))

def isDownPress(e):
	return True if e.type == KEYDOWN else False if e.type == KEYUP else None

def enum(**enums):
	return type('Enum', (), enums)

