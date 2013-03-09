# -*- coding: utf-8 *-*
import pygame
from pygame.locals import *
from pyinspacelib import *
from random import randint

def init_starsky():
	return [(randint(50, 850), randint(50, 450), 0) for i in range(randint(5, 10))]

def tick_starsky(paramstars, tick):
	stars = list(paramstars)

	# create new stars
	if tick % 100 == 0:
		for i in range(randint(0, 25 - len(stars))):
			stars.append((randint(22, 882), randint(-500, 0), 0))
	# update and delete stars
	if tick % 3 == 0:
		stars = [(x, y + 1, z if z == 0 or z > 190 else z + 7) for x, y, z in stars if y < 500]
	if tick % 100 == 0:
		r = randint(0, len(stars) - 1)
		if stars[r][2] == 0: stars[r] = (stars[r][0], stars[r][1], 1)

	return stars

def render_starsky(surface, stars):
	''' render astonishing star sky. '''
	# render stars
	for x, y, z in stars:
		draw_star(surface, (x,y), (60+z%190, 60+z%190, 60+z%190), kind=1, scale=2)

def draw_star(surface, (x,y), color, kind=0, scale=1):
	position = lambda (a,b): (int(a*scale+x), int(b*scale+y))
	def darken((a,b,c),x): return (a,b,c,300-x*60)

	if kind == 0:
		surface.set_at((x, y), color)

	elif kind == 1:
		pygame.draw.circle(surface, color, (x, y), scale)

	elif kind == 2:
		alphasurface = surface.convert_alpha()
		""" handdrawn 'dot' """

		colors = dict()
		for i in range(1,4):
			colors[i] = darken((color[0], color[1], color[2]), i)

		inner = [(2, 1), (1, 2), (2, 2), (3, 2), (2, 3)]
		inner = map(position,inner)
		for p in inner: alphasurface.set_at(p, colors[1])

		middle = [(1,1),(3,1),(3,3),(1,3)]
		middle = map(position,middle)
		for p in middle: alphasurface.set_at(p, colors[2])

		outer = [(2,0),(4,2),(2,4),(0,2)]
		outer = map(position,outer)
		for p in outer: alphasurface.set_at(p, colors[3])

		surface.blit(alphasurface, (0,0))

	elif kind == 3:
		"""the real polygon thing"""
		karo = [(10,0),(20,10),(10,20),(0,10)]
		karo = list(map(position,karo))
		pygame.draw.polygon(surface, color, karo)
		quadrat = [(3,3),(17,3),(17,17),(3,17)]
		quadrat = list(map(position,quadrat))
		pygame.draw.polygon(surface, color, quadrat)

