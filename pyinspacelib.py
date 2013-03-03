# -*- coding: utf-8 *-*

""" No game logic here, just helper functions"""

import pygame

def getimagepath(img):
	return 'res/' + str(img) + '.png'

def getimageobject(img):
	if img[-4:] == ".png":
		return pygame.image.load(img)
	else:
		return pygame.image.load(getimagepath(img))

def enum(**enums):
	return type('Enum', (), enums)
