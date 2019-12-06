import pygame, sys, random, openpyxl, os
from pygame.locals import *
import pokeBallAssets as assets
import pytweening as tween



FPS = 30
# To change 
WINDOWWIDTH = assets.WINDOWWIDTH
WINDOWHEIGHT = assets.WINDOWHEIGHT

gridHeight = 192
gridWidth =  170

BLACK           =(  0,   0, 0)
WHITE           =(255, 255, 255)

BKGCOLOR = WHITE
MAINTEXTCOLOR = BLACK


pokeBallTween = tween.easeInOutSine
animationSpeed = 10
ballOffset = 130
flashOffset = 270

locationAngles = [0, 60, 120, 180, 240, 300]

quizPath = r'C:\Come On Python Games\resources\pokeBallGame\quiz'
possibleUnits = ['U1', 'U2', 'U3']
track = 'johtoTrainerBattle'
teamTurn = 0



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



def main(teams, initObjects, teamTurn, selectionList):
    global FPSCLOCK 
    pygame.init()

    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]

    book = selectionList[0]
    unit = selectionList[1]
    section = str(2)

    firstTeam = teams[0]
    secondTeam = teams[1]
    correctQAPair, sessionQAList, sessionFlashcards = excelGetGameScheme(book, unit, section)

    ballMessages = [pair.answer for pair in sessionQAList]

    questionSurf, questionRect = makeQuestionPanel(correctQAPair)
    
    pokeBalls = generatePokeballs(ballMessages)


    alakazam = assets.alakazam
    alakazam.state = 'normal'

    alakazamImg = assets.alakazam.surface
    alakazamRect = assets.alakazam.rect
    alakazamRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    rotations = random.randint(2, 4)

    spinAnimation(pokeBalls, locationAngles, animationSpeed, DISPLAYSURF, teams, rotations)
    
    lastGuess = None
    winState = None
    tries = 0
    
    
    
    

    while True:

        DISPLAYSURF.fill(BKGCOLOR)
        if teamTurn > 1:
            teamTurn = 0

        currentTeam = teams[teamTurn]
        currentTeam.drawTurnIndicator(DISPLAYSURF)
        
    
        

        mouseClick = False
        lastGuess = None


        checkForQuit()


        mouseX, mouseY = pygame.mouse.get_pos()

        musicRepeat(track)

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

        if lastGuess:
            if lastGuess == correctQAPair.answer:
                alakazam.state = 'ouch'
                winState = 'Win'
                
                
                if tries == 1:
                    currentTeam.addGreatPoint()
                else:
                    currentTeam.addPoint()
            teamTurn += 1

        if tries > 4:
            alakazam.state = 'laugh'
            winState = 'Fail'
            
        
        alakazamImg = assets.alakazam.surface
        alakazamRect = assets.alakazam.rect
        alakazamRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)   
        
        for team in teams:
            team.drawTeamLabel(DISPLAYSURF)
        

        DISPLAYSURF.blit(alakazamImg, alakazamRect)
        drawFlashcards(sessionFlashcards, flashLocations, DISPLAYSURF)
        drawPokeBallDefaultLocations(pokeBalls, locationAngles, DISPLAYSURF)
        
        
        DISPLAYSURF.blit(questionSurf, questionRect)

        
   

        pygame.display.update()

        FPSCLOCK.tick(FPS)           

        if winState:
            pygame.time.wait(1000)
            return teams, teamTurn


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

def spinAnimation(pokeballs, locations, animationSpeed, targetSurf, teams, rotateTimes=4):
    musicRepeat(track)
    assets.ballSound.play()
    totalRotation = 360 * rotateTimes
    
    

    for rotationStep in range(0, totalRotation, animationSpeed):
        checkForQuit()        
        offset = pokeBallTween(rotationStep / totalRotation) * 360
        targetSurf.fill(BKGCOLOR)
        copySurf = targetSurf.copy()
        
        for n in range(len(pokeballs)):
            location = assets.getTrigoFromCenter((locations[n]+offset), ballOffset, WINDOWWIDTH, WINDOWHEIGHT)
            pokeballs[n].rect.center = location
            copySurf.blit(pokeballs[n].surface, pokeballs[n].rect)


            
        targetSurf.blit(copySurf, (0, 0))
        for team in teams:
            team.drawTeamLabel(targetSurf)
        pygame.display.flip()
        FPSCLOCK.tick(FPS)
           
# Mega meta function to set out the whole game questions and flashcards
def excelGetGameScheme(book, unit, subSet):
    path = r'C:\Come On Python Games\resources\pokeBallGame\quiz'
    bookPath = f'{book}.xlsx'
    excelPath = os.path.join(path, bookPath)

    

    wb = openpyxl.load_workbook(excelPath)
    sheet = wb[unit]

    sessionQuestions = []

    questionType = None
    flashInstructions = None

    if subSet == '1':
        questionType = sheet['A9'].value
        flashInstructions = sheet['B9'].value

    elif subSet == '2':
        questionType = sheet['A19'].value
        flashInstructions = sheet['B19'].value

    if questionType.lower() == 'open':
        if subSet == '1':
            rowRangeStart = 10
            rowRangeStop = 16

        elif subSet == '2':
            rowRangeStart = 20
            rowRangeStop = 26
        
        for row in range(rowRangeStart, rowRangeStop):
            questionCell = sheet.cell(row=row, column=1).value
            answerCell = sheet.cell(row=row, column=2).value
            sessionQuestions.append(assets.question(questionCell, answerCell))

        correctQuestionAnswerPair = random.choice(sessionQuestions)

    elif questionType.lower() == 'closed':
        if subSet == '1':
            bedo = sheet.cell(row=10, column=1).value
        elif subSet == '2':
            bedo = sheet.cell(row=20, column=1).value

        correctQuestionAnswerPair, sessionQuestions = closedQuestionType(bedo.lower())

    
    if flashInstructions in ('all', 'All', 'ALL'):
        sessionFlashcards = getFlashcards(book, unit)
    else:
        if subSet == 1:
            setStart = sheet['B9'].value
            setEnd = sheet['C9'].value
        else:
            setStart = sheet['B19'].value
            setEnd = sheet['C19'].value
        
        sessionFlashcards = getFlashcards(book, unit, [setStart, setEnd])

    
    return correctQuestionAnswerPair, sessionQuestions, sessionFlashcards 
 

def closedQuestionType(bedo):
    if bedo == 'be':
        questions = [
                ("Is he...?", "Yes, he is",  "No, he isn't"),
                ("Is she...?", "Yes, she is",  "No, she isn't"),
                ("Is Tom...?", "Yes, he is",  "No, he isn't"),
                ("Is Alice...?", "Yes, she is",  "No, she isn't"),
                ("Are they...?", "Yes, they are",  "No, they're not"),
                ("Are you...?", "Yes, I am",  "No, I'm not")
            ]
    else:
        questions = [
                ("Does he...?", "Yes, he does",  "No, he doesn't"),
                ("Does she...?", "Yes, she does",  "No, she doesn't"),
                ("Does Tom...?", "Yes, he does",  "No, he doesn't"),
                ("Does Alice...?", "Yes, she does",  "No, she doesn't"),
                ("Do they...?", "Yes, they do",  "No, they don't"),
                ("Do you...?", "Yes, I do",  "No, I don't")
            ]

    randomlyPickedQuestion = random.choice(questions)
    question = randomlyPickedQuestion[0]
    correctAnswer = randomlyPickedQuestion[1]
    wrongAnswer = randomlyPickedQuestion[2]

    rightQAPair = assets.question(question, correctAnswer)

    AnswerList = [assets.question(None, wrongAnswer) for _ in range(5)]
    AnswerList.append(rightQAPair)
    random.shuffle(AnswerList)

    return rightQAPair, AnswerList


def makeQuestionPanel(questionObj):

    questionFont = assets.pokeFont(30)
    text = questionFont.render(questionObj.question, 1, MAINTEXTCOLOR)
    textRect = text.get_rect()
    textRect.center = (WINDOWWIDTH/2, 30)

    return (text, textRect)

def getFlashcards(book, unit, flashRange=None):
    basePath = r'C:\Come On Python Games\resources\pokeBallGame'
    sessionPath = os.path.join(basePath, book, unit)

    imagePaths = [os.path.join(sessionPath, image) for image in os.listdir(sessionPath) if os.path.splitext(image)[1] in ('.png', '.PNG')]
    
    if flashRange: # Flashrange is for when the parts of the unit don't work well together.
        start = flashRange[0]
        stop = flashRange[1]
        imagePaths = imagePaths[start:stop]



    
    if len(imagePaths) > 6:
        sessionImgs = random.sample(imagePaths, 6)
    else:
        sessionImgs = imagePaths
        random.shuffle(sessionImgs)

    pyImages = [pygame.image.load(imgFile) for imgFile in sessionImgs]

    
    return [pygame.transform.scale(image, (200, 125))for image in pyImages]


def drawFlashcards(flashList, flashLocationList, targetSurf):
    for n in range(len(flashList)):
            
            current = flashList[n]
            
            currentRect = current.get_rect()
            currentRect.center = flashLocationList[n]

            targetSurf.blit(current, currentRect)

def checkWin(lastGuess, questionPair, tries, alakazam, currentTeam, teamTurn):
    win = None

    if tries > 4:
        alakazam.state = 'laugh'
        win = 'Fail'
        teamTurn += 1
    if lastGuess == None:
        pass
    else:
        if lastGuess == questionPair.answer:
            alakazam.state = 'ouch'
            win = 'Win'
            if tries == 1:
                currentTeam.addGreatPoint()
            else:
                currentTeam.addPoint()
        else:
            teamTurn += 1
    if teamTurn > 1:
        teamTurn = 0
    return alakazam, win, currentTeam, teamTurn


def musicRepeat(track):
    for event in pygame.event.get(pygame.USEREVENT):
            pygame.mixer.music.load(assets.music[track]['main'])
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()       
        

def selectionMenu(initObjects, menuList):
    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]

    menuSurf = assets.menuBKG
    menuRect = menuSurf.get_rect()
    menuRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

       
    menuLabels = [assets.pokeFont(30).render(label, 1, assets.MAINTEXTCOLOR) for label in menuList]
    menuRects = [label.get_rect() for label in menuLabels]

    menuLeftBorder = WINDOWWIDTH/2 - 200
    menuTopBorder = WINDOWHEIGHT/2 - 100
    menuSpacing = 35

    selectionIcon = assets.teamImgs['turnIndicator']['B']
    selectionRect = selectionIcon.get_rect()
    selectionX = menuLeftBorder - 20
    selection = 0
    

    for n in range(len(menuLabels)):
        menuRects[n].topleft = (menuLeftBorder, (menuTopBorder + menuSpacing * n))
        


    while True:
        checkForQuit()
        musicRepeat(track)
        DISPLAYSURF.fill(BKGCOLOR)
        DISPLAYSURF.blit(menuSurf,menuRect)

        
        for n in range(len(menuLabels)):
            DISPLAYSURF.blit(menuLabels[n], menuRects[n])

        for event in pygame.event.get():
            if event.type == KEYUP:
                assets.selectSound.play()
                if event.key == K_UP:
                    selection -= 1
                elif event.key == K_DOWN:
                    selection += 1
                elif event.key == K_RETURN:
                    return menuList[selection]
        

        if selection < 0:
            selection = 0
        elif selection > len(menuLabels)-1:
            selection = len(menuLabels)-1
        
        selectionY = (menuTopBorder + menuSpacing * selection + 5)
        selectionRect.topleft = (selectionX, selectionY)
        DISPLAYSURF.blit(selectionIcon, selectionRect)

        pygame.display.update()

        FPSCLOCK.tick(FPS)



def bonusGame(teams, initObjects):
    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]

def beginMusic(track):
    pygame.mixer.music.load(assets.music[track]['intro'])
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(pygame.USEREVENT)


def game():
    
    FPSCLOCK = pygame.time.Clock()    
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
    DISPLAYSURF.fill(BKGCOLOR)
    pygame.display.set_caption('The PokeBall Game')

    initObjects = [FPSCLOCK, DISPLAYSURF] # Makes sending this into main, other screens flippin EASY tho.

    sessionTeams = [assets.TeamA(), assets.TeamB()]
    random.shuffle(sessionTeams)


    for team in sessionTeams:
        scoreList = []

    teamTurn = 0

    books = [os.path.splitext(title)[0] for title in os.listdir(quizPath) if os.path.splitext(title)[1] in ('.xlsx', '.XLSX')]
    
    bookSelection = selectionMenu(initObjects, books)
    unitSelection = selectionMenu(initObjects, possibleUnits)
    selectionList = [bookSelection, unitSelection]
    print(selectionList)
    beginMusic(track)
        
    while True:
        
        sessionTeams, teamTurn = main(sessionTeams, initObjects, teamTurn, selectionList)


if __name__ == "__main__":
    game()