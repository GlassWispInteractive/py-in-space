import pygame, sys
from random import randint
from pygame.locals import *


# start it
pygame.init()

# manage window
DISPLAYSURF = pygame.display.set_mode((900, 500))
pygame.display.set_caption('PyInSpace!')

# clock object for fps
fpsClock = pygame.time.Clock() 
tick = 0

# list of objects to render
renderList = []
stars = [(randint(50, 850), randint(50, 450)) for i in range(randint(10, 25))]

# definitions
menu = True
keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_RETURN, K_p]

# some colors
grey = (80, 80, 80)
silver = (192, 192, 192)

textfont = pygame.font.SysFont("monospace", 28)


logoImg = pygame.image.load('res/logo.png')
logoPos = (157, 100)

# menu
def menu():
	DISPLAYSURF.blit(logoImg, logoPos)
	pygame.draw.rect(DISPLAYSURF, silver, (250, 300, 400, 60))
	pygame.draw.rect(DISPLAYSURF, grey, (260, 305, 380, 50))
	
	# label
	label = textfont.render("Start game!", 1, (200,200,200))
	labelPos = label.get_rect(centerx=450, centery = 330)
	DISPLAYSURF.blit(label, labelPos)

def starsky(stars):
	# create new
	if tick % 50 == 0:
		for i in range(randint(0, 25 - len(stars))):
			stars.append((randint(50, 850), 1))
	
	# move stars
	if tick % 3 == 0: stars = [(x, y + 1) for x, y in stars if y < 500]
	
	# render stars
	for pos in stars:
		pygame.draw.circle(DISPLAYSURF, (130, 130, 130), pos, 3, 0)
	
	return stars
	
while True: # main game loop
	eventList = pygame.event.get()
	
	# check for quit event
	if any(e.type == QUIT for e in eventList): break
	# reduce events up to key strokes
	eventList = [e for e in eventList if e.type == KEYDOWN and e.key in keys]
	# just accepts the first movement
	
	DISPLAYSURF.fill((0, 0, 0))
	stars = starsky(stars)
	menu()


	pygame.display.update()
	# upper limit to frames
	tick = tick + 1
	fpsClock.tick(30)

# halt the game
pygame.quit()
sys.exit()
