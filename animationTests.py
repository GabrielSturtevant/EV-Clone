import pygame, sys, math, random
from pygame.locals import *

pygame.init()

WINWIDTH = 650
WINHEIGHT = 500
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)
PADDING = 10
GAMEOVERMODE = False
NUMBEROFSTARS = 500  #Stars in a given area. helps with motion
MAX_MOVERATE = 100
MIN_MOVERATE = 0

SHIPWIDTH = 150
SHIPHEIGHT = 150
SHIPSIZE = 150

BACKDROPWIDTH = 1920
BACKDROPHEIGHT = 1080

SPINRATE = 20

STARTX = int(WINWIDTH / 2) - int(SHIPWIDTH / 2)
STARTY = int(WINHEIGHT / 2) - int(SHIPHEIGHT / 2)
BACKX = int(WINWIDTH / 2) - int(BACKDROPWIDTH / 2)
BACKY = int(WINHEIGHT / 2) - int(BACKDROPHEIGHT / 2)

FPS = 60
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0, 32)
pygame.display.set_caption('animationTest')

BLACK = (0,0,0)




def main():
	global shipImage, background, stars, shipImage
	
	shipImage = pygame.image.load('test.png')
	background = pygame.image.load('backdrop.png')
	stars = []
	for i in range(1,5):
		stars.append(pygame.image.load('stars%s.png' %i))
	shipImage = pygame.transform.rotate(shipImage, 0)	
	
	while True:
		playGame()

def playGame():	
	LEFTKEY = False
	RIGHTKEY = False
	ACCELERATION = False
	DECCELERATION = False
	
	starObjs = []
	
	SHIPANGLE = 0
	MOVERATEX = 0
	MOVERATEY = 0
	
	x = STARTX
	y = STARTY
	STARX = BACKX
	STARY = BACKY
	LASTxANGLE = 0
	LASTyANGLE = 0
	
	camerax = 0
	cameray = 0
	
	tempX, tempY = 0,0

	####
	shipCopy = shipImage
	var = shipCopy.get_rect()
	
	###PLAYER Object:
	playerObj = {	'x': STARTX,
					'y': STARTY}
	
	#put stars on the screen
	for i in range(10):
		starObjs.append(makeNewStars(camerax, cameray))
		starObjs[i]['x'] = random.randint(0, WINWIDTH)
		starObjs[i]['y'] = random.randint(0, WINHEIGHT)
	
	while True:
		DISPLAYSURF.fill(BLACK)
		DISPLAYSURF.blit(background, (BACKX, BACKY))
		
		#delete stars outside of the screen area
		for i in range(len(starObjs)-1, -1, -1):
			if isOutsideActiveArea(camerax, cameray, starObjs[i]):
				del starObjs[i]
		
		#add more stars if needed
		while len(starObjs) < NUMBEROFSTARS:
			starObjs.append(makeNewStars(camerax, cameray))
		
		#draw the stars
		for sObj in starObjs:
			sRect = pygame.Rect( (sObj['x'] - camerax,
									sObj['y'] - cameray,
									sObj['width'],
									sObj['height']) )
			DISPLAYSURF.blit(stars[sObj['starImage']], sRect)
		
		#adjust the camera
		playerCenterX = playerObj['x'] + int(SHIPSIZE / 2)
		playerCenterY = playerObj['y'] + int(SHIPSIZE / 2)
		camerax = playerCenterX - HALF_WINWIDTH
		cameray = playerCenterY - HALF_WINHEIGHT
		
		#draw the player
		if not GAMEOVERMODE:
		
			playerObj['rect'] = pygame.Rect((	playerObj['x'] - camerax,
												playerObj['y'] - cameray,
												SHIPSIZE,
												SHIPSIZE))
			
			DISPLAYSURF.blit(shipCopy, playerObj['rect'])
		
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key in (K_LEFT, K_a):
					LEFTKEY = True
				elif event.key in (K_RIGHT, K_d):
					RIGHTKEY = True
				elif event.key in (K_UP, K_w):
					ACCELERATION = True
				elif event.key in (K_DOWN, K_s):
					DECCELERATION = True
		
			elif event.type == KEYUP:
				if event.key in (K_LEFT, K_a):
					LEFTKEY = False
				elif event.key in (K_RIGHT, K_d):
					RIGHTKEY = False
				elif event.key in (K_UP, K_w):
					ACCELERATION = False
				elif event.key in (K_DOWN, K_s):
					DECCELERATION = False
			elif event.type == QUIT:
				pygame.quit()
				sys.exit()
				
		if not GAMEOVERMODE:
			
			if LEFTKEY:
				SHIPANGLE += SPINRATE
				if math.fabs(SHIPANGLE) == 360:
					SHIPANGLE = 0
				shipCopy = rot_center(shipImage, SHIPANGLE)
			if RIGHTKEY:
				SHIPANGLE -= SPINRATE
				if math.fabs(SHIPANGLE) == 360:
					SHIPANGLE = 0
				shipCopy = rot_center(shipImage, SHIPANGLE)
			if ACCELERATION:
				if MOVERATEX < MAX_MOVERATE or MOVERATEY < MAX_MOVERATE:
					tempX, tempY = backgroundScroll(SHIPANGLE)
					if tempX >= LASTxANGLE:
						MOVERATEX +=  1
					else:
						MOVERATEX -=  1
					if tempY >= LASTyANGLE:
						MOVERATEY += 1
					else:
						MOVERATEY -=1
					
					if MOVERATEX > MAX_MOVERATE:
						MOVERATEX = MAX_MOVERATE
					if MOVERATEY > MAX_MOVERATE:
						MOVERATEY = MAX_MOVERATE
					
			if DECCELERATION:
				MOVERATEX = MIN_MOVERATE
				MOVERATEY = MIN_MOVERATE
				'''
				if MOVERATEX > 0 or MOVERATEY > 0:
				
					MOVERATEX -= 10 * tempX
					MOVERATEY -= 10 * tempY
					if MOVERATEX < 0:
						MOVERATEX = 0
					if MOVERATEY < 0:
						MOVERATEY = 0
				'''
			if MOVERATEX > 0 or MOVERATEY > 0:
				playerObj['x'] -= MOVERATEX
				playerObj['y'] -= MOVERATEY
			
	
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
	
		pygame.display.update()
		fpsClock.tick(FPS)

def rot_center(image, angle):
    #rotate an image while keeping its center and size
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def backgroundScroll(angle):
	x = math.sin(math.radians(angle))
	y = math.cos(math.radians(angle))
	return x,y


def getRandomOffCameraPos(camerax, cameray, objWidth, objHeight):
    # create a Rect of the camera view
    cameraRect = pygame.Rect(camerax, cameray, WINWIDTH, WINHEIGHT)
    while True:
        x = random.randint(round(camerax - WINWIDTH), round(camerax + (2 * WINWIDTH)))
        y = random.randint(round(cameray - WINHEIGHT), round(cameray + (2 * WINHEIGHT)))
        # create a Rect object with the random coordinates and use colliderect()
        # to make sure the right edge isn't in the camera view.
        objRect = pygame.Rect(x, y, objWidth, objHeight)
        if not objRect.colliderect(cameraRect):
            return x, y


def makeNewStars(camerax, cameray):
	st = {}
	num = random.randint(0, len(stars) - 1)
	st['starImage'] = num
	st['width'] = stars[num].get_width()
	st['height'] = stars[num].get_height()
	st['x'], st['y'] = getRandomOffCameraPos(camerax, cameray, st['width'], st['height'])
	st['rect'] = pygame.Rect((st['x'], st['y'], st['width'], st['height']))
	return st


def isOutsideActiveArea(camerax, cameray, obj):
    # Return False if camerax and cameray are more than
    # a half-window length beyond the edge of the window.
    boundsLeftEdge = camerax - WINWIDTH
    boundsTopEdge = cameray - WINHEIGHT
    boundsRect = pygame.Rect(boundsLeftEdge, boundsTopEdge, WINWIDTH * 3, WINHEIGHT * 3)
    objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return not boundsRect.colliderect(objRect)


if __name__ == '__main__':
	main()
