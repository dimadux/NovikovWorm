import random, pygame, sys, math
from pygame.locals import *

FPS=12
WINDOWWIDTH = 840
WINDOWHEIGHT = 680
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
GRAY      = (128, 128, 128)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random0 start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    wormRecorded=[]
    direction = RIGHT
    holeImg=pygame.image.load('hole.png')
    holeExit=pygame.image.load('hole.png')
    # Start the apple in a random place.
    apple = getRandomLocation()
    holeCoords = getRandomLocation()
    holeExitCoords = getRandomLocation()
    recordApple={'x':-1,'y':-1}
    holeCoords={'x':-1,'y':-1}
    holeExitCoords={'x':-1,'y':-1}
    eatenApples=0
    startHole=False
    creatingExit=False
    throughTheTime=False
    recording=False
    countTown=0
    highSpeed=False
    key=1
    #pygame.mixer.init(44100, -16,2,2048)
    #soundXFiles=pygame.mixer.music.load('xfiles.mp3')
    recordWormLen=6
    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        #if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT and not creatingExit:
        #    return # game over
        if wormCoords[HEAD]['x']==-1:
          wormCoords[HEAD]['x']=CELLWIDTH-1
          direction=LEFT
        if wormCoords[HEAD]['x']==CELLWIDTH:
          wormCoords[HEAD]['x']=0
          direction=RIGHT
        if wormCoords[HEAD]['y']==-1:
          wormCoords[HEAD]['y']=CELLHEIGHT-1
          direction=UP
        if wormCoords[HEAD]['y']==CELLHEIGHT:
          wormCoords[HEAD]['y']=0
          direction=DOWN
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y'] and not creatingExit:
                return # game over

        # check if worm has eaten an apply
        if holeCoords['x'] in {wormCoords[HEAD]['x'],wormCoords[HEAD]['x']+1,wormCoords[HEAD]['x']-1} and holeCoords['y'] in {wormCoords[HEAD]['y']-1,wormCoords[HEAD]['y'],wormCoords[HEAD]['y']+1}:
            if(not creatingExit):
              holeExitCoords=getRandomLocation()
              creatingExit=True
              throughTheTime=True
              highSpeed=True
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            if recording:
            	recordApple=apple
            apple = getRandomLocation() # set a new apple somewhere
            eatenApples+=1;
            if eatenApples==3:
              startHole=True
              holeCoords=getRandomLocation()
             # pygame.mixer.music.play(1,0.0)
        else:
            del wormCoords[-1] # remove worm's tail segment
        # move the worm by adding a segment in the direction it is moving
        if eatenApples>=3:
            wormRecorded.append(wormCoords[HEAD])
        if creatingExit:
        	newHead=holeExitCoords
        	creatingExit=False
        else:
          if direction == UP:
              newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
          elif direction == DOWN:
              newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
          elif direction == LEFT:
              newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
          elif direction == RIGHT:
              newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        if recording:
          for dtp in wormRecorded[0:9]:
            if dtp['y']-wormCoords[HEAD]['y']<5 and direction==UP and dtp['y']-wormCoords[HEAD]['y']>-2 and dtp['x']==wormCoords[HEAD]['x']:
              if wormCoords[HEAD]['x']>CELLWIDTH/2:
                direction=LEFT
              else:
                direction=RIGHT
            if wormCoords[HEAD]['y']-dtp['y']<5 and direction==DOWN and wormCoords[HEAD]['y']-dtp['y']>-2 and dtp['x']==wormCoords[HEAD]['x']:
              if wormCoords[HEAD]['x']>CELLWIDTH/2:
                direction=LEFT
              else:
                direction=RIGHT
            if dtp['x']-wormCoords[HEAD]['x']<5 and direction==RIGHT and dtp['x']-wormCoords[HEAD]['x']>-2 and dtp['y']==wormCoords[HEAD]['y']:
              if wormCoords[HEAD]['x']>CELLHEIGHT/2:
                direction=UP
              else:
                direction=DOWN
            if wormCoords[HEAD]['x']-dtp['x']<5 and direction==LEFT and wormCoords[HEAD]['x']-dtp['x']>-2 and dtp['y']==wormCoords[HEAD]['y']:
              if wormCoords[HEAD]['x']>CELLHEIGHT/2:
                direction=UP
              else:
                direction=DOWN
        drawApple(recordApple)
        if startHole:
          DISPLAYSURF.blit(holeImg,(holeCoords['x']*CELLSIZE,holeCoords['y']*CELLSIZE))
        if throughTheTime:
          DISPLAYSURF.blit(holeExit,(holeExitCoords['x']*CELLSIZE,holeExitCoords['y']*CELLSIZE))
          countTown+=1
          if countTown>=len(wormCoords)+1:
            startHole=True
            throughTheTime=True
            recording=True
            highSpeed=False
        if highSpeed:
          drawWorm(wormCoords,CELLSIZE,key,GREEN,DARKGREEN)
          key+=1
        else:
            drawWorm(wormCoords,CELLSIZE,key,GREEN,DARKGREEN)
        if recording:
        	drawWorm(wormRecorded[0:recordWormLen],CELLSIZE,key,WHITE,GRAY)
        	wormRecorded=wormRecorded[1:]
        	if wormRecorded[0]['x']==recordApple['x'] and wormRecorded[0]['y']==recordApple['y']:
        	  recordApple={'x':-1,'y':-1}
        	  recordWormLen+=1

        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        if highSpeed:
        	FPSCLOCK.tick(FPS*2)
        else:
            FPSCLOCK.tick(FPS)

def getThinner():
	wormCoords

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('WORM HOLES', True, GRAY)

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedRect1 = titleSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(titleSurf1, rotatedRect1)
        drawPressKeyMsg()


        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
  x=-600
  y=300
  #soundForOver=pygame.mixer.music.load('chimai.mp3')
  #pygame.mixer.music.play(1,8.8)
  BELMONDO=pygame.image.load('belmondo.png')
  gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
  gameSurf = gameOverFont.render('Game', True, WHITE)
  overSurf = gameOverFont.render('Over', True, WHITE)
  gameRect = gameSurf.get_rect()
  overRect = overSurf.get_rect()
  gameRect.midtop = (WINDOWWIDTH / 2, 10)
  overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

  DISPLAYSURF.blit(gameSurf, gameRect)
  DISPLAYSURF.blit(overSurf, overRect)
  drawPressKeyMsg()
  while x<-100:
    DISPLAYSURF.blit(BELMONDO,(x,y))
    x+=1
    pygame.display.update()
  pygame.time.wait(500)
  checkForKeyPress() # clear out any key presses in the event queue

  while True:
    x+=10
    if checkForKeyPress():
      pygame.event.get() # clear event queue
      return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords,SIZE,key,color,bgcolor):
  localKey=0
  for coord in wormCoords:
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    wormSegmentRect = pygame.Rect(x, y,SIZE,SIZE)
    pygame.draw.rect(DISPLAYSURF, bgcolor, wormSegmentRect)
    wormInnerSegmentRect = pygame.Rect(x + 4, y + 4,SIZE - 8,SIZE - 8)
    pygame.draw.rect(DISPLAYSURF, color, wormInnerSegmentRect)
    if key==localKey and SIZE==10:
      SIZE*=2
      key=False
    localKey+=1;


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
