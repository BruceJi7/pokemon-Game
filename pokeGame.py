import pygame, sys, random, openpyxl, os
from pygame.locals import *
import pokeBallAssets as assets
import pytweening as tween



FPS = 30
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768

gridHeight = 192
gridWidth =  170

BLACK           =(  0,   0, 0)
WHITE           =(255, 255, 255)


pokeBallTween = tween.easeInOutSine
animationSpeed = 10
ballOffset = 140
flashOffset = 250

locationAngles = [0, 60, 120, 180, 240, 300]



locations = [
    assets.getTrigoFromCenter(0, ballOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(60, ballOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(120, ballOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(180, ballOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(240, ballOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(300, ballOffset, WINDOWWIDTH, WINDOWHEIGHT)
    ]

flashLocations = [
    assets.getTrigoFromCenter(0, flashOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(60, flashOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(120, flashOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(180, flashOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(240, flashOffset, WINDOWWIDTH, WINDOWHEIGHT),
    assets.getTrigoFromCenter(300, flashOffset, WINDOWWIDTH, WINDOWHEIGHT)
]






def main():
    global FPSCLOCK
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
    DISPLAYSURF.fill(BLACK)
    pygame.display.set_caption('The PokeBall Game')

    book = 'EB2'
    unit = 'U1'

    flashImages = getFlashcards(book, unit)

    questions = excelGetQuestionMessage(book, unit)    
    correctQAPair = random.choice(questions)
    questionSurf, questionRect = makeQuestionPanel(correctQAPair)
    
    messages = [question.answer for question in questions]    
    pokeBalls = generatePokeballs(messages)

    alakazam = assets.alakazam
    alakazam.state = 'normal'

    alakazamImg = assets.alakazam.surface
    alakazamRect = assets.alakazam.rect
    alakazamRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    rotations = random.randint(2, 4)
    spinAnimation(pokeBalls, locationAngles, animationSpeed, DISPLAYSURF, rotations)
    DISPLAYSURF.fill(BLACK)

    lastGuess = None
    winState = None
    tries = 0

    while True:

        
        mouseClick = False

        checkForQuit()

        if winState:
            pygame.time.wait(1000)
            return

    
        mouseX, mouseY = pygame.mouse.get_pos()       
        
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mouseClick = True
            

        for ball in pokeBalls:
            if ball.rect.collidepoint(mouseX, mouseY):
                if mouseClick:
                    
                    if ball.state == 'closed':
                        assets.ballOpenSound.play()
                        tries += 1
                        
                        lastGuess = ball.message
                        ball.state = 'open'
                    # elif ball.state == 'open':
                    #     ball.state = 'closed'
            if alakazamRect.collidepoint(mouseX, mouseY):
                if mouseClick:
                    return


        alakazam, winState = checkWin(lastGuess, correctQAPair, tries, alakazam)

        alakazamImg = assets.alakazam.surface
        alakazamRect = assets.alakazam.rect
        alakazamRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)   
        

        
        drawPokeBallDefaultLocations(pokeBalls, locationAngles, DISPLAYSURF)
        drawFlashcards(flashImages, flashLocations, DISPLAYSURF)
        DISPLAYSURF.blit(alakazamImg, alakazamRect)
        DISPLAYSURF.blit(questionSurf, questionRect)

        


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
        current.rect.center = assets.getTrigoFromCenter(locations[n], ballOffset, WINDOWWIDTH, WINDOWHEIGHT)
        targetSurf.blit(current.surface, current.rect)

def spinAnimation(pokeballs, locations, animationSpeed, targetSurf, rotateTimes=4):
    assets.ballSound.play()
    totalRotation = 360 * rotateTimes
    origSurf = targetSurf.copy()
    targetSurf.blit(origSurf, (0, 0))

    for rotationStep in range(0, totalRotation, animationSpeed):
        checkForQuit()        
        offset = pokeBallTween(rotationStep / totalRotation) * 360
        
        for n in range(len(pokeballs)):
            location = assets.getTrigoFromCenter((locations[n]+offset), ballOffset, WINDOWWIDTH, WINDOWHEIGHT)
            pokeballs[n].rect.center = location
            targetSurf.blit(pokeballs[n].surface, pokeballs[n].rect)
            pygame.display.flip()
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


def makeQuestionPanel(questionObj):

    questionFont = assets.pokeFont(30)
    text = questionFont.render(questionObj.question, 1, WHITE)
    textRect = text.get_rect()
    textRect.center = (WINDOWWIDTH/2, 50)

    return (text, textRect)

def getFlashcards(book, unit):
    basePath = r'C:\Come On Python Games\resources\pokeBallGame'
    sessionPath = os.path.join(basePath, book, unit)

    imagePaths = [os.path.join(sessionPath, image) for image in os.listdir(sessionPath) if os.path.splitext(image)[1] in ('.png', '.PNG')]
    random.shuffle(imagePaths)
    sessionImgs = random.sample(imagePaths, 6)

    pyImages = [pygame.image.load(imgFile) for imgFile in sessionImgs]

    
    return [pygame.transform.scale(image, (200, 125))for image in pyImages]


def drawFlashcards(flashList, flashLocationList, targetSurf):
    for n in range(len(flashList)):
            
            current = flashList[n]
            
            currentRect = current.get_rect()
            currentRect.center = flashLocationList[n]

            targetSurf.blit(current, currentRect)

def checkWin(lastGuess, questionPair, tries, alakazam):
    win = None
    if tries > 4:
        alakazam.state = 'laugh'
        win = 'Fail'
    if lastGuess == None:
        pass
    else:
        if lastGuess == questionPair.answer:
            alakazam.state = 'ouch'
            win = 'Win'
    return alakazam, win




def game():
    while True:
        main()


if __name__ == "__main__":
    game()