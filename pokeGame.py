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

throwTween = tween.easeInSine
dropTween = tween.easeInSine
wobbleTween = tween.easeInCirc
bounceTween = tween.easeOutBounce
pokeBallTween = tween.easeInOutSine
throwAnimationSpeed = 5
animationSpeed = 10
ballOffset = 140
flashOffset = 280

locationAngles = [0, 60, 120, 180, 240, 300]

quizPath = r'C:\Come On Python Games\resources\pokeBallGame\quiz'
possibleUnits = ['U1', 'U2', 'U3', 'U4']
subSets = ['1', '2']
tracks = ['johtoTrainerBattle', 'gymBattle', 'darkCave']
track = random.choice(tracks)
menuTrack = 'menu'
teamTurn = 0

bkgImg = assets.backgrounds['grass']

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
    enemyPoke = initObjects[2]

    book = selectionList[0]
    unit = selectionList[1]
    section = selectionList[2]

    firstTeam = teams[0]
    secondTeam = teams[1]
    correctQAPair, sessionQAList, sessionFlashcards = excelGetGameScheme(book, unit, section)

    ballMessages = [pair.answer for pair in sessionQAList]

    questionSurf, questionRect = makeQuestionPanel(correctQAPair)
    
    pokeBalls = generatePokeballs(ballMessages)


    alakazam = assets.alakazam
    alakazam.state = 'normal'

    # alakazamImg = assets.alakazam.surface
    # alakazamRect = assets.alakazam.rect
    # alakazamRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    enemyPoke.rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + 20)

    rotations = random.randint(2, 4)

    spinAnimation(pokeBalls, locationAngles, animationSpeed, enemyPoke, DISPLAYSURF, teams, rotations)
    
    lastGuess = None
    winState = None
    tries = 0
    

    #Test
   
    
    

    while True:

        DISPLAYSURF.fill(BKGCOLOR)
        DISPLAYSURF.blit(bkgImg, (0, 0))
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
            collideRect = ball.rect.copy()
            collideRect.inflate_ip(-120, -30)
            if collideRect.collidepoint(mouseX, mouseY):
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
                
                
                
                if tries < 3:
                    currentTeam.addGreatPoint()
                    assets.critHitSound.play()
                else:
                    currentTeam.addPoint()
                    assets.hitSound.play()
            teamTurn += 1
            

        if tries > 4 and winState != 'Win': # On the 5th try, if no-one won, alakazam laughs.
            alakazam.state = 'laugh'
            winState = 'Fail'
            assets.nopeSound.play()
            
        
        alakazamImg = assets.alakazam.surface
        alakazamRect = assets.alakazam.rect
        alakazamRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)   
        
        for team in teams:
            team.drawTeamLabel(DISPLAYSURF)
        

        DISPLAYSURF.blit(enemyPoke.surface, enemyPoke.rect)
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

def spinAnimation(pokeballs, locations, animationSpeed, enemyPokemon, targetSurf, teams, rotateTimes=4):
    
    assets.ballSound.play()
    totalRotation = 360 * rotateTimes

    enemyPokemon.rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + 20)
    
    

    for rotationStep in range(0, totalRotation, animationSpeed):
        checkForQuit()
        musicRepeat(track)        
        offset = pokeBallTween(rotationStep / totalRotation) * 360
        targetSurf.blit(bkgImg, (0, 0))
        
        for n in range(len(pokeballs)):
            location = assets.getTrigoFromCenter((locations[n]+offset), ballOffset, WINDOWWIDTH, WINDOWHEIGHT)
            pokeballs[n].rect.center = location
            targetSurf.blit(pokeballs[n].surface, pokeballs[n].rect)

        targetSurf.blit(enemyPokemon.surface, enemyPokemon.rect)    
  
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
    
        potentialQuestions = []
        for row in range(rowRangeStart, rowRangeStop):
            questionCell = sheet.cell(row=row, column=1).value
            answerCell = sheet.cell(row=row, column=2).value
            potentialQuestions.append(assets.question(questionCell, answerCell))

        correctQuestionAnswerPair = random.choice(potentialQuestions)
        sessionQuestions = [assets.question('', 'X') for _ in range(5)]
        sessionQuestions.append(correctQuestionAnswerPair)
        random.shuffle(sessionQuestions)

    elif questionType.lower() == 'closed':
        if subSet == '1':
            bedo = sheet.cell(row=10, column=1).value
        elif subSet == '2':
            bedo = sheet.cell(row=20, column=1).value

        correctQuestionAnswerPair, sessionQuestions = closedQuestionType(bedo.lower())

    
    if flashInstructions in ('all', 'All', 'ALL'):
        sessionFlashcards = getFlashcards(book, unit)
    else:
        if subSet == '1':
            setStart = int(sheet['B9'].value)
            setEnd = int(sheet['C9'].value)
        else:
            setStart = int(sheet['B19'].value)
            setEnd = int(sheet['C19'].value)
        
        
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
            pygame.mixer.music.set_volume(0.2)
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
        musicRepeat(menuTrack)
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
                elif event.key in (K_RETURN, K_KP_ENTER):
                    return menuList[selection]
        

        if selection < 0:
            selection = len(menuLabels)-1
        elif selection > len(menuLabels)-1:
            selection = 0
        
        selectionY = (menuTopBorder + menuSpacing * selection + 5)
        selectionRect.topleft = (selectionX, selectionY)
        DISPLAYSURF.blit(selectionIcon, selectionRect)

        pygame.display.update()

        FPSCLOCK.tick(FPS)


def catchWildPokemon(animationSpeed, targetSurf, teams, currentTeam, bonusPokemon, lastScoredPoint, shakeHowManyTimes, caught):
    
    pokeBall = assets.bonusPokeBall

    pokeBall.ballType = lastScoredPoint
    pokeBall.state = 'closed'

    pokeBallImg = pokeBall.surface
    pokeBallRect = pokeBall.rect

    
    

    totalRotation = 100
    dropDistance = 200
    bounceHeight = 100

    if currentTeam.name == 'A':
        startingLocation = -100
        arcCentreX = 550
        arcCentreY = 600
        reverseMode = -1
    else:
        startingLocation = 100
        arcCentreX = WINDOWWIDTH - 550
        arcCentreY = 600
        reverseMode = 1

    # bonusPokemon.rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/3)
    

    # Throw Arc Animation part
    assets.throwSound.play()
    for rotationStep in range(0, totalRotation, animationSpeed):
        checkForQuit()        
        offset = (throwTween(rotationStep / totalRotation) * 80)
        offset *= reverseMode
        targetSurf.blit(bkgImg, (0,0))
        distFromRotationalCentre = 300

        location = assets.getTrigoForArc(startingLocation + offset, distFromRotationalCentre, arcCentreX, arcCentreY)
        pokeBallRect.center = location
        targetSurf.blit(bonusPokemon.surface, bonusPokemon.rect)
        targetSurf.blit(pokeBallImg, pokeBallRect)

        currentTeam.drawTeamLabel(targetSurf)

        pygame.display.flip()
        FPSCLOCK.tick(FPS)
    
    startingCentery = pokeBallRect.centery

    # Pokemon Goes Into Ball section will go here:

    assets.ballOpenSound.play()

    pokeBall.state = 'open'
    pokeBallImg = pokeBall.surface

    for animFrame in assets.bonusBallCatch:
        for time in range (0, 10):
            checkForQuit()
            if time == 1:
                animFrameSurf = animFrame
                animFrameRect = animFrame.get_rect()
                animFrameRect.centerx = pokeBallRect.centerx
                animFrameRect.centery = pokeBallRect.centery

                targetSurf.blit(bkgImg, (0,0))
                
                targetSurf.blit(bonusPokemon.surface, bonusPokemon.rect)
                targetSurf.blit(pokeBallImg, pokeBallRect)
                targetSurf.blit(animFrameSurf, animFrameRect)

                currentTeam.drawTeamLabel(targetSurf)

                pygame.display.flip()
                FPSCLOCK.tick(FPS)





    
    
    # Drop and bounce animation
    pokeBall.state = 'closed'
    pokeBallImg = pokeBall.surface

    soundPlayed = False
    for dropStep in range(1, 100, animationSpeed):
        checkForQuit()
        offset =  dropDistance * (bounceTween(dropStep/100))

        targetSurf.blit(bkgImg, (0,0))
        
        pokeBallRect.centery = startingCentery + offset
        targetSurf.blit(pokeBallImg, pokeBallRect)

        currentTeam.drawTeamLabel(targetSurf)
        if dropStep > 50 and soundPlayed == False:
            assets.ballBounceSound.play()
            soundPlayed = True
            
        pygame.display.flip()
        FPSCLOCK.tick(FPS)
    
    # Waiting animation
    waitTime = random.randint(20, 30)
    for waitStep in range(1, waitTime):
        checkForQuit()
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

    # Wobble Animation
    jumpStartY = pokeBallRect.centery
    jumpHeight = 40
    
    for _ in range(shakeHowManyTimes):
        assets.ballShakeSound.play()
        for jumpStep in range(1, 100, animationSpeed*6):

            checkForQuit()
            
            offset =  (jumpHeight * (wobbleTween(jumpStep/100)))
            targetSurf.blit(bkgImg, (0,0))
            
            pokeBallRect.centery = jumpStartY - offset
            targetSurf.blit(pokeBallImg, pokeBallRect)
            currentTeam.drawTeamLabel(targetSurf)
            pygame.display.flip()
            FPSCLOCK.tick(FPS)
        
        for fallStep in range(1, 100, animationSpeed):

            checkForQuit()

            offset =  (jumpHeight * (bounceTween(fallStep/100))) - jumpHeight
            targetSurf.blit(bkgImg, (0,0))
            pokeBallRect.centery = jumpStartY + offset
            targetSurf.blit(pokeBallImg, pokeBallRect)

            currentTeam.drawTeamLabel(targetSurf)
            pygame.display.flip()
            FPSCLOCK.tick(FPS)
        
        waitTime = random.randint(6, 20)
        for waitStep in range(1, waitTime):
            checkForQuit()
            pygame.display.flip()
            FPSCLOCK.tick(FPS)
        

    if not caught:

        assets.catchFailSound.play()

        for animFrame in assets.bonusBallCatch:
            for time in range (0, 10):
                checkForQuit()
                if time == 1:
                    animFrameSurf = animFrame
                    animFrameRect = animFrame.get_rect()
                    animFrameRect.centerx = pokeBallRect.centerx
                    animFrameRect.centery = pokeBallRect.centery

                    targetSurf.blit(bkgImg, (0,0))
                    targetSurf.blit(bonusPokemon.surface, bonusPokemon.rect)
                    targetSurf.blit(animFrameSurf, animFrameRect)

                    currentTeam.drawTeamLabel(targetSurf)

                    pygame.display.flip()
                    FPSCLOCK.tick(FPS)

            pygame.display.flip()
            FPSCLOCK.tick(FPS)    


        for waitStep in range(1, 20):
            checkForQuit()
            targetSurf.blit(bkgImg, (0,0))
            currentTeam.drawTeamLabel(targetSurf)
            targetSurf.blit(bonusPokemon.surface, bonusPokemon.rect)    
            pygame.display.flip()
            FPSCLOCK.tick(FPS)
        
        WAITING = True
        while WAITING:
            checkForQuit()
            for event in pygame.event.get():
                if event.type == KEYUP:
                    if event.key in (K_RETURN, K_KP_ENTER):
                        WAITING = False
                    else:
                        continue
            pygame.display.flip()
            FPSCLOCK.tick(FPS)


def rollToCatch(ballType):
    firstChance = random.randint(0, 100)
    if ballType == 'P':
        return firstChance
    else:
        secondChance = random.randint(0, 95)
        return max([firstChance, secondChance])




def catchMechanic(ballType):
    catchChance = rollToCatch(ballType)

    # print(f'Ball type {ballType}, catch chance {catchChance}.')
    
    if catchChance > 85:
        return True, 3
    
    return False, random.randint(1, 3)


def bonusGame(teams, playingTeam, initObjects, bonusPokemon):
    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]

    
    RUNNING = True
    caught = 'wait'

    while RUNNING:

        DISPLAYSURF.fill(BKGCOLOR)


        
        if playingTeam.score != 0:
            
            lastScoredPoint = playingTeam.popPoint
            caught, shakeTimes = catchMechanic(lastScoredPoint)
            catchWildPokemon(throwAnimationSpeed, DISPLAYSURF, teams, playingTeam, bonusPokemon, lastScoredPoint, shakeTimes, caught)
            if caught:
                caught = 'yes'

        
        if playingTeam.score == 0:
            print('You ran out of pokeballs!')
            caught = 'no'

        return caught, playingTeam

    
def beginMusic(track):
    pygame.mixer.music.load(assets.music[track]['intro'])
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(pygame.USEREVENT)

def gameOver(whoWon, initObjects):
    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]
    beginMusic('victory')

    victoryMessageA = f'Congratulations, Team {whoWon.name}.'
    victoryMessageB = 'You win!'
    victorySurfA = assets.pokeFont(30).render(victoryMessageA, 1, MAINTEXTCOLOR)
    victoryRectA = victorySurfA.get_rect()
    victoryRectA.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    victorySurfB = assets.pokeFont(50).render(victoryMessageB, 0, MAINTEXTCOLOR)
    victoryRectB = victorySurfB.get_rect()
    victoryRectB.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2+50)
    
    menuSurf = assets.menuBKG
    menuRect = menuSurf.get_rect()
    menuRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    while True:
        musicRepeat('victory')
        checkForQuit()
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(menuSurf, menuRect)
        DISPLAYSURF.blit(victorySurfA, victoryRectA)
        DISPLAYSURF.blit(victorySurfB, victoryRectB)

        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key in (K_RETURN, K_KP_ENTER):
                    return
        

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        



def bonusSuccess(whoWon, initObjects, bonusPokemon):
    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]
    

    victoryMessageA = f'Congratulations, Team {whoWon.name}.'
    victoryMessageB = 'You caught the pokemon!'
    victorySurfA = assets.pokeFont(30).render(victoryMessageA, 1, MAINTEXTCOLOR)
    victoryRectA = victorySurfA.get_rect()
    victoryRectA.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    victorySurfB = assets.pokeFont(30).render(victoryMessageB, 0, MAINTEXTCOLOR)
    victoryRectB = victorySurfB.get_rect()
    victoryRectB.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2+50)
    
    menuSurf = assets.menuBKG
    menuRect = menuSurf.get_rect()
    menuRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)


    bonusPokemon.rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/4)
    beginMusic('bonus')

    while True:
        musicRepeat('bonus')
        checkForQuit()
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(menuSurf, menuRect)
        DISPLAYSURF.blit(bonusPokemon.surface, bonusPokemon.rect)
        DISPLAYSURF.blit(victorySurfA, victoryRectA)
        DISPLAYSURF.blit(victorySurfB, victoryRectB)

        pygame.display.update()
        FPSCLOCK.tick(FPS) 

 


def bonusFail(initObjects):
    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]
    pygame.mixer.music.stop()

    victoryMessageA = f'Oh no!'
    victoryMessageB = 'The pokemon got away!'
    victorySurfA = assets.pokeFont(30).render(victoryMessageA, 1, MAINTEXTCOLOR)
    victoryRectA = victorySurfA.get_rect()
    victoryRectA.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    victorySurfB = assets.pokeFont(30).render(victoryMessageB, 0, MAINTEXTCOLOR)
    victoryRectB = victorySurfB.get_rect()
    victoryRectB.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2+50)
    
    menuSurf = assets.menuBKG
    menuRect = menuSurf.get_rect()
    menuRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    while True:
        
        checkForQuit()
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(menuSurf, menuRect)
        DISPLAYSURF.blit(victorySurfA, victoryRectA)
        DISPLAYSURF.blit(victorySurfB, victoryRectB)

        pygame.display.update()
        FPSCLOCK.tick(FPS) 

 

def game():
    
    FPSCLOCK = pygame.time.Clock()    
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
    DISPLAYSURF.fill(BKGCOLOR)
    pygame.display.set_caption('The PokeBall Game')

    roundPokemon = assets.bonusPokemon(assets.getRandomPoke())


    initObjects = [FPSCLOCK, DISPLAYSURF, roundPokemon] # Makes sending this into main, other screens flippin EASY tho.

    sessionTeams = [assets.TeamA(), assets.TeamB()]
    random.shuffle(sessionTeams)       


    teamTurn = 0
    sessionTeams[0].addGreatPoint()
    sessionTeams[0].addGreatPoint()
    sessionTeams[0].addGreatPoint()

    books = [os.path.splitext(title)[0] for title in os.listdir(quizPath) if os.path.splitext(title)[1] in ('.xlsx', '.XLSX') and '~$' not in os.path.splitext(title)[0]]
    beginMusic(menuTrack)
    bookSelection = selectionMenu(initObjects, books)
    unitSelection = selectionMenu(initObjects, possibleUnits)
    subSetSelection = selectionMenu(initObjects, subSets)
    selectionList = [bookSelection, unitSelection, subSetSelection]
    beginMusic(track)

    winner = None
      
    while True: # This loop locks the game into repeating rounds
        
        sessionTeams, teamTurn = main(sessionTeams, initObjects, teamTurn, selectionList)
        for team in sessionTeams: # Check to see if someone has won 6 rounds
            if team.hasWon:
                winner = team
        if winner:
            break

    gameOver(winner, initObjects) # Show the main Game Over Screen

    bonusRound = False
    for team in sessionTeams:
        if 'G' or 'U' in team.scoreList:
            bonusRound = True
    if bonusRound:
        bonusPokemon = roundPokemon
        while True:
            caught, bonusPlayer = bonusGame(sessionTeams, winner, initObjects, bonusPokemon)
            if caught == 'yes' and bonusPlayer:
                bonusSuccess(bonusPlayer, initObjects, bonusPokemon)
            elif caught == 'no':
                assets.runAwaySound.play()
                bonusFail(initObjects)
            winner = bonusPlayer
              

       


if __name__ == "__main__":
    game()