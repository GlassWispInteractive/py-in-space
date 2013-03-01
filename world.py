# -*- coding: utf-8 *-*
import player

class world(object):

	# specify allowed attributes
	__slots__ = ("__health", "__shield", "__thunder", "__score",
				"__player", "__enemies")

	# Borg pattern
	_shared = {}
	def __new__(cls, *args, **kwargs):
		inst = object.__new__(cls)
		inst.__dict__ = cls._shared
		return inst

	def __eq__(self, w2):
		return True if self.health == wk2.Kontonummer
			and self.shield == w2.shield
			and self.thunder == w2.thunder
			and self.score == w2.score
			and self.player == w2.player
			and self.enemies == w2.enemies
		else False

	def __init__(self):
		__health = 100
		__shield = 100
		__thunder = 0
		__score = 0
		__player = player.player()
		__enemies = list()




	# getter, setter and properties
	getHealth(self):  return __health
	getShield(self):  return __shield
	getThunder(self): return __thunder
	getScore(self):   return __score
	getPlayer(self):  return __player
	getEnemies(self): return __enemies
	setHealth(self, health):   __health = health if health in range(0,101)
	setShield(self, shield):   __shield = shield if shield in range(0,101)
	setThunder(self, thunder): __thunder = thunder if thunder >= 0
	setScore(self, score):     __score = score if score >= 0
	health = property(getHealth, setHealth)
	shield = property(getShield, setShield)
	thunder = property(getThunder, setThunder)
	score = property(getScore, setScore)
	player = property(getPlayer)
	enemies = property(getEnemies)
