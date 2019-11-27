import pygame, sys, random
from pygame.locals import *
import pokeBallAssets as assets



FPS = 30
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768

gridHeight = 192
gridWidth =  170

BLACK = (0, 0, 0)

def main():
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
    DISPLAYSURF.fill(BLACK)
    pygame.display.set_caption('The PokeBall Game')




    while True:

        checkForQuit()

        alakazamImg = assets.alakazam.surface
        alakazamRect = assets.alakazam.rect

        alakazamRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

        messages = ["He's", "She's", "It's", "Tom is", "They're", "I'm"]
        
        pokeBalls = generatePokeballs(messages)

        for ball in pokeBalls:
            DISPLAYSURF.blit(ball.surface, ball.rect)


        # DISPLAYSURF.blit(pokeBallImg, pokeBallRect)

        DISPLAYSURF.blit(alakazamImg, alakazamRect)
        

        pygame.display.update()

        FPSCLOCK.tick(FPS)


def terminate():
    print('Terminating game...')
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate()
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def generatePokeballs(messages):
    random.shuffle(messages)

    locations =((gridWidth*2,gridHeight*2),
                (gridWidth*2.5,gridHeight), 
                (gridWidth*3.5, gridHeight), 
                (gridWidth*4, gridHeight*2), 
                (gridWidth*3.5, gridHeight*3), 
                (gridWidth*2.5, gridHeight*3))

 
    pokeObjs = []
    for n in range(len(locations)):
        current = assets.pokeball(assets.pokeballImgs)
        current.message = messages[n]
        current.state = 'open'
        pokeRect = current.rect
        pokeRect.center = locations[n]
        pokeObjs.append(current)

    return pokeObjs



     


main()