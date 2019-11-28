import pygame, sys, random, openpyxl, os
from pygame.locals import *
import pokeBallAssets as assets



FPS = 30
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768

gridHeight = 192
gridWidth =  170

BLACK = (0, 0, 0)

animationSpeed = 15
centerOffset = 200

locationAngles = [0, 60, 120, 180, 240, 300]


locations = [
    assets.getTrigoFromCenter(0, centerOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(60, centerOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(120, centerOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(180, centerOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(240, centerOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(300, centerOffset, WINDOWWIDTH, WINDOWHEIGHT)
    ]






def main():
    global FPSCLOCK
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
    DISPLAYSURF.fill(BLACK)
    pygame.display.set_caption('The PokeBall Game')

    book = 'EB2'
    unit = 'U3'

    questions = excelGetQuestionMessage(book, unit)

    
    correctQAPair = random.choice(questions)

    messages = [question.answer for question in questions]

    
    pokeBalls = generatePokeballs(messages)


    spinAnimation(pokeBalls, locationAngles, animationSpeed, DISPLAYSURF)
    DISPLAYSURF.fill(BLACK)

    while True:
        mouseClick = False

        checkForQuit()

        

        alakazamImg = assets.alakazam.surface
        alakazamRect = assets.alakazam.rect

        alakazamRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

        
        
        

        # for ball in pokeBalls:
        #     DISPLAYSURF.blit(ball.surface, ball.rect)

        DISPLAYSURF.blit(alakazamImg, alakazamRect)



        mouseX, mouseY = pygame.mouse.get_pos()

         
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mouseClick = True
            

        for ball in pokeBalls:
            if ball.rect.collidepoint(mouseX, mouseY):
                if mouseClick:
                    if ball.state == 'closed':
                        ball.state = 'open'
                    elif ball.state == 'open':
                        ball.state = 'closed'


        # DISPLAYSURF.blit(pokeBallImg, pokeBallRect)

        # spinAnimation(pokeBalls, locationAngles, animationSpeed, DISPLAYSURF)

        drawPokeBallDefaultLocations(pokeBalls, locationAngles, DISPLAYSURF)
        

        pygame.display.flip()

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

    pokeObjs = []
    for n in range(len(messages)):
        current = assets.pokeball(assets.pokeballImgs)
        current.message = messages[n]
        current.state = 'closed'
        pokeObjs.append(current)

    return pokeObjs


def drawPokeBallDefaultLocations(pokeballs, locations, targetSurf):
    for n in range(len(pokeballs)):
        current = pokeballs[n]
        current.rect.center = assets.getTrigoFromCenter(locations[n], centerOffset, WINDOWWIDTH, WINDOWHEIGHT)
        targetSurf.blit(current.surface, current.rect)

def spinAnimation(pokeballs, locations, animationSpeed, targetSurf, rotateTimes=3 ):
    totalRotation = 360 * rotateTimes
    origSurf = targetSurf.copy()

    for rotationStep in range(0, totalRotation, animationSpeed):
        targetSurf.blit(origSurf, (0, 0))
        for n in range(len(pokeballs)):
            location = assets.getTrigoFromCenter((locations[n]+rotationStep), centerOffset, WINDOWWIDTH, WINDOWHEIGHT)
            pokeballs[n].rect.center = location
            targetSurf.blit(pokeballs[n].surface, pokeballs[n].rect)
            pygame.display.update()
        FPSCLOCK.tick(FPS)
            

def excelGetQuestionMessage(book, unit):
    path = r'C:\Users\Administrator\Google 드라이브\ASPython\Pokemon Game\pokemonGame\quiz'
    bookPath = f'{book}.xlsx'
    excelPath = os.path.join(path, bookPath)
    questions = []

    wb = openpyxl.load_workbook(excelPath)
    sheet = wb[unit]
    for row in range(1, 7):
        questionCell = sheet.cell(row=row, column=1).value
        answerCell = sheet.cell(row=row, column=2).value
        questions.append(assets.question(questionCell, answerCell))

    return questions


            




main()