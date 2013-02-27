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
menu = ["Start", "Highscore", "Help", "Training", "Quit"]
keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_RETURN, K_p]

# some colors
silver = pygame.Color(192, 192, 192)
darkbrown = pygame.Color(46, 31, 7)

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
    
    # update graphics
    pygame.draw.rect(DISPLAYSURF, darkbrown, (200, 150, 100, 50))

    pygame.display.update()
    # upper limit to frames
    fpsClock.tick(30)

# halt the game
pygame.quit()
sys.exit()
