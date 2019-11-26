import pygame, sys
from pygame.locals import *
import pokeBallAssets as assets



FPS = 30
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768

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

        messages = ("He's", "She's", "It's", "Tom is", "They're", "I'm")

        cellHeight = 192
        cellWidth =  170


        locations = ((cellWidth,cellHeight*2),(cellWidth*2,cellHeight), (cellWidth*4, cellHeight), (cellWidth*5, cellHeight*2), (cellWidth*4, cellHeight*3), (cellWidth*2, cellHeight*3))

        pokeBalls = [assets.pokeball(assets.pokeballImgs) for _ in range(6)]

        pokeObjs = []
        for n in range(0, 6):
            current = pokeBalls[n]
            current.message = messages[n]
            pokeballImg = current.surface
            pokeRect = current.rect
            pokeRect.center = locations[n]
            pokeObjs.append((pokeballImg, pokeRect))

        for pair in pokeObjs:
            DISPLAYSURF.blit(pair[0], pair[1])


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


     


main()