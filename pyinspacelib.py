# -*- coding: utf-8 *-*
import pygame

import socket
if socket.gethostname() == 'T430':
	MUSIC = SOUND = False
else:
	MUSIC = SOUND = True

def getimageobject(img):
	if img.endswith('.png'):
		return pygame.image.load(img)
	else:
		return getimageobject('res/' + str(img) + '.png')

def getogg(snd):
	return pygame.mixer.Sound('res/' + str(snd) + '.ogg')

def isDownPress(e):
	return e.type == pygame.KEYDOWN

