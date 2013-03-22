import math

x = 944

def f(n):
	x, y = 0, 0
	while n > 0:
		print 
		while x < 100 * (1 + y / 36) and n > 0:
			x += 1
			n -= 8
		while y < 36 * (1 + x / 100) and n > 0:
			y += 1
			n -= 8
	return abs(100*int(math.ceil(y/36.)%2 == 1) - x%100), y
	
print f(x)
