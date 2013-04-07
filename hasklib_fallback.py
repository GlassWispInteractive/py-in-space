#!/usr/bin/env python
# -*- coding: utf-8 *-*

def star_brightness(z):
	return 60 + z % 190

def player_pos_x(xunits):
	return 32 + 7 * xunits

def new_shot_pos_x(xunits):
	return 55 + 7 * xunits
