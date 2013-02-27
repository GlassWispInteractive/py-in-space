import pygame, sys
from pygame.locals import *
from random import randint
import math

def draw_star(surface, (x,y), color, kind=0, scale=1):
	position = lambda (a,b) : (int(a*scale+x), int(b*scale+y))
	
	if kind == 0:
		surface.set_at((x, y), color)
	
	elif kind == 1:
		r = randint(1,4)
		pygame.draw.circle(surface, color, (x, y), r)
		
	elif kind == 2:
		"""handdrawn 'dot'"""
		colors = {
			'out' : (color[0],color[1],color[2], int(0.5*255)),
			'mid' : (color[0],color[1],color[2], int(0.3*255)),
			'inn' : (color[0],color[1],color[2], int(0.1*255))
		}
		
		outer = [(2,0),(4,2),(2,4),(0,2)]
		outer = list(map(position,outer))
		for p in outer: surface.set_at(p, colors['out'])

		middle = [(1,1),(3,1),(3,3),(1,3)]
		middle = list(map(position,middle))
		for p in middle: surface.set_at(p, colors['mid'])

		inner = [(2,1),(1,2),(2,2),(3,2),(2,3)]
		inner = list(map(position,inner))
		for p in inner: surface.set_at(p, colors['inn'])
		
	elif kind == 3:
		"""the real polygon thing"""
		
		# karo
		karo = [(10,0),(20,10),(10,20),(0,10)]
		karo = list(map(position,karo))
		pygame.draw.polygon(surface, color, karo)
		
		# quadrat
		quadrat = [(3,3),(17,3),(17,17),(3,17)]
		quadrat = list(map(position,quadrat))
		pygame.draw.polygon(surface, color, quadrat)
		
	elif kind == 4:
		"""wrapper for 2 and 3 based on scaling factor"""
		if scale <= 2:
			draw_star(surface, (x,y), color, kind=2, scale=scale)
		else:
			draw_star(surface, (x,y), color, kind=3, scale=scale)

def draw_random_star(surface, scale=1):
	x = randint(0,899)
	y = randint(0,599)
	c = randint(200,255)
	kind = randint(0,4)
	scale = randint(1,10) # ?
	draw_star(surface, (x,y), (c,c,c), kind, scale)
		
def draw_poligon_star(surface, c, (x,y), scale=1):
	draw_star(surface, c, (x,y), kind=4, scale=scale)
