# -*- coding: utf-8 *-*
import pygame

def getimageobject(img):
	if img.endswith('.png'):
		return pygame.image.load(img)
	else:
		return pygame.image.load('res/' + str(img) + '.png')

def isDownPress(e):
	return True if e.type == pygame.KEYDOWN else False if e.type == pygame.KEYUP else None

def enum(**enums):
	return type('Enum', (), enums)
