# -*- coding: utf-8 *-*
import pygame

def getimageobject(img):
	if img.endswith('.png'):
		return pygame.image.load(img)
	else:
		return pygame.image.load('res/' + str(img) + '.png')

def isDownPress(e):
	return e.type == pygame.KEYDOWN

