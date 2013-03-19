# -*- coding: utf-8 *-*
import pygame

def getimageobject(img):
	if img.endswith('.png'):
		return pygame.image.load(img)
	else:
		return getimageobject('res/' + str(img) + '.png')

def getogg(snd):
	return pygame.mixer.Sound('res/' + str(snd) + '.ogg')

def isDownPress(e):
	return True if e.type == pygame.KEYDOWN else False if e.type == pygame.KEYUP else None

def enum(**enums):
	return type('Enum', (), enums)
