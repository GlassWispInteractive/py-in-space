import pygame, sys
from pygame.locals import *

# start it
pygame.init()

# manage window
DISPLAYSURF = pygame.display.set_mode((900, 500))
pygame.display.set_caption('PyInSpace!')

# clock object for fps
fpsClock = pygame.time.Clock() 
# list of objects to render
renderList = []

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
def button(stuff):
	pass

while True: # main game loop
	eventList = pygame.event.get()
	
	# check for quit event
	if any(e.type == QUIT for e in eventList): break
	# reduce events up to key strokes
	eventList = [e for e in eventList if e.type == KEYDOWN and e.key in keys]
	# just accepts the first movement
	
	# graphics
	DISPLAYSURF.blit(logoImg, logoPos)
	pygame.draw.rect(DISPLAYSURF, silver, (250, 300, 400, 60))
	pygame.draw.rect(DISPLAYSURF, grey, (260, 305, 380, 50))
	
	# label
	label = textfont.render("Start game!", 1, (200,200,200))
	labelPos = label.get_rect(centerx=450, centery = 330)
	DISPLAYSURF.blit(label, labelPos)
	
	pygame.display.update()
	# upper limit to frames
	fpsClock.tick(30)

# halt the game
pygame.quit()
sys.exit()
