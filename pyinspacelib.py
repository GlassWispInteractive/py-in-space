# -*- coding: utf-8 *-*
import pygame

def getimagepath(img):
	return 'res/' + img + '.png'

def getimageobject(img):
	if img[-4:] == ".png":
		return pygame.image.load(img)
	else:
		return pygame.image.load(getimagepath(img))

