import pokeBallAssets as ast
import pygame, sys, random
import pytweening as tween
from pygame.locals import *

teams = [ast.TeamA(), ast.TeamB()]
random.shuffle(teams)

firstTeam = teams[0]
secondTeam = teams[1]



secondTeam.addGreatPoint()

firstTeam.isTurn = True
print(firstTeam)

FPS = 30
# To change 
WINDOWWIDTH = ast.WINDOWWIDTH
WINDOWHEIGHT = ast.WINDOWHEIGHT

BLACK           =(  0,   0, 0)
WHITE           =(255, 255, 255)

BKGCOLOR = WHITE
MAINTEXTCOLOR = BLACK

throwTween = tween.easeInSine
dropTween = tween.easeInSine
wobbleTween = tween.easeInCirc
bounceTween = tween.easeOutBounce
animationSpeed = 10

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


def throwAnimation(animationSpeed, targetSurf, teams, currentTeam):
    pokeBallImg = pygame.transform.scale(ast.pokeballImgs['closed'], (50,50))
    pokeBallRect = pokeBallImg.get_rect()

    totalRotation = 100
    dropDistance = 300
    bounceHeight = 100

    if currentTeam.name == 'A':
        startingLocation = -100
        arcCentreX = 500
        arcCentreY = 600
        reverseMode = -1
    else:
        startingLocation = 100
        arcCentreX = WINDOWWIDTH - 500
        arcCentreY = 600
        reverseMode = 1

    # Throw Arc Animation part
    for rotationStep in range(0, totalRotation, animationSpeed):
        checkForQuit()        
        offset = (throwTween(rotationStep / totalRotation) * 80)
        offset *= reverseMode
        targetSurf.fill(BKGCOLOR)
        copySurf = targetSurf.copy()
        distFromRotationalCentre = 400

        location = ast.getTrigoForArc(startingLocation + offset, distFromRotationalCentre, arcCentreX, arcCentreY)
        pokeBallRect.center = location
        copySurf.blit(pokeBallImg, pokeBallRect)


            
        targetSurf.blit(copySurf, (0, 0))
        for team in teams:
            team.drawTeamLabel(targetSurf)
        pygame.display.flip()
        FPSCLOCK.tick(FPS)
    
    startingCentery = pokeBallRect.centery

    # Drop and bounce animation 
    for dropStep in range(1, 100, animationSpeed):
        checkForQuit()
        offset =  dropDistance * (bounceTween(dropStep/100))

        targetSurf.fill(BKGCOLOR)
        copySurf = targetSurf.copy()
        pokeBallRect.centery = startingCentery + offset
        copySurf.blit(pokeBallImg, pokeBallRect)

        targetSurf.blit(copySurf, (0, 0))
        for team in teams:
            team.drawTeamLabel(targetSurf)
        pygame.display.flip()
        FPSCLOCK.tick(FPS)
    
    # Waiting animation
    waitTime = random.randint(6, 30)
    for waitStep in range(1, waitTime):
        checkForQuit()
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

    # Wobble Animation
    jumpStartY = pokeBallRect.centery
    jumpHeight = 40
    jumpTimes = random.randint(1, 3)
    for _ in range(0, jumpTimes):

        for jumpStep in range(1, 100, animationSpeed*6):

            checkForQuit()

            offset =  (jumpHeight * (wobbleTween(jumpStep/100)))
            print(offset)
            targetSurf.fill(BKGCOLOR)
            copySurf = targetSurf.copy()
            pokeBallRect.centery = jumpStartY - offset
            copySurf.blit(pokeBallImg, pokeBallRect)

            targetSurf.blit(copySurf, (0, 0))
            for team in teams:
                team.drawTeamLabel(targetSurf)
            pygame.display.flip()
            FPSCLOCK.tick(FPS)
        
        for fallStep in range(1, 100, animationSpeed):

            checkForQuit()

            offset =  (jumpHeight * (bounceTween(fallStep/100))) - jumpHeight
            print(offset)
            targetSurf.fill(BKGCOLOR)
            copySurf = targetSurf.copy()
            pokeBallRect.centery = jumpStartY + offset
            copySurf.blit(pokeBallImg, pokeBallRect)

            targetSurf.blit(copySurf, (0, 0))
            for team in teams:
                team.drawTeamLabel(targetSurf)
            pygame.display.flip()
            FPSCLOCK.tick(FPS)
        
        waitTime = random.randint(6, 20)
        for waitStep in range(1, waitTime):
            checkForQuit()
            pygame.display.flip()
            FPSCLOCK.tick(FPS)




pygame.init()

FPSCLOCK = pygame.time.Clock()


DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
DISPLAYSURF.fill(BKGCOLOR)
pygame.display.set_caption('Team Test Game')

pygame.mixer.music.load(ast.music['johtoTrainerBattle']['intro'])
pygame.mixer.music.play()
pygame.mixer.music.set_endevent(pygame.USEREVENT)




while True:
    checkForQuit()
    for team in teams:
        team.drawTeamLabel(DISPLAYSURF)
        team.drawTurnIndicator(DISPLAYSURF)

    for event in pygame.event.get(pygame.USEREVENT):
        pygame.mixer.music.load(ast.music['johtoTrainerBattle']['main'])
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

    throwAnimation(6, DISPLAYSURF, teams, firstTeam)

    


    pygame.display.update()

    FPSCLOCK.tick(FPS)


