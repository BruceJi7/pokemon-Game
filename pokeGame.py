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






def main(teams):
    global FPSCLOCK
    pygame.init()

    FPSCLOCK = pygame.time.Clock()

    
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
    DISPLAYSURF.fill(BKGCOLOR)
    pygame.display.set_caption('The PokeBall Game')

    book = 'EB4'
    unit = 'U1'

    flashImages = getFlashcards(book, unit)

    firstTeam = teams[0]
    secondTeam = teams[1]





    # Load questions from EXCEL
    # questions = excelGetQuestionMessage(book, unit)    
    # correctQAPair = random.choice(questions)
    # messages = [question.answer for question in questions]


    # Use Closed Questions:
    closedType = 'do'
    correctQAPair, messages = closedQuestionType(closedType)

    messages.append(correctQAPair.answer)
    random.shuffle(messages) 


    questionSurf, questionRect = makeQuestionPanel(correctQAPair)
    
    
    pokeBalls = generatePokeballs(messages)

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
    teamTurn = 0
    
    

    while True:

        currentTeam = teams[teamTurn]
    

        DISPLAYSURF.fill(BKGCOLOR)

        
        mouseClick = False

        checkForQuit()


        if winState:
            pygame.time.wait(1000)
            return teams
   
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
            # if alakazamRect.collidepoint(mouseX, mouseY):
            #     if mouseClick:
            #         return teams


        if tries > 4:
            alakazam.state = 'laugh'
            winState = 'Fail'
            teamTurn += 1

        if lastGuess:
            if lastGuess == correctQAPair.answer:
                alakazam.state = 'ouch'
                winState = 'Win'
                lastGuess = None
                if tries == 1:
                    currentTeam.addGreatPoint()
                else:
                    currentTeam.addPoint()

            else:
                teamTurn += 1
                lastGuess = None
        if teamTurn > 1:
            teamTurn = 0
        

            
        # alakazam, winState, currentTeam, teamTurn = checkWin(lastGuess, correctQAPair, tries, alakazam, currentTeam, teamTurn)

        alakazamImg = assets.alakazam.surface
        alakazamRect = assets.alakazam.rect
        alakazamRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)   
        
        for team in teams:
            team.drawTeamLabel(DISPLAYSURF)
        currentTeam.drawTurnIndicator(DISPLAYSURF)



        DISPLAYSURF.blit(alakazamImg, alakazamRect)
        drawFlashcards(flashImages, flashLocations, DISPLAYSURF)
        drawPokeBallDefaultLocations(pokeBalls, locationAngles, DISPLAYSURF)
        
        
        DISPLAYSURF.blit(questionSurf, questionRect)

        
        

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
           

def excelGetGameScheme(book, unit, subSet):
    path = r'C:\Come On Python Games\resources\pokeBallGame\quiz'
    bookPath = f'{book}.xlsx'
    excelPath = os.path.join(path, bookPath)
    questions = []

    wb = openpyxl.load_workbook(excelPath)
    sheet = wb[unit]

    if subSet == '1':
        questionType = sheet['B9']
        flashInstructions = sheet['A9']

    elif subSet == '2':
        questionType = sheet['B20']
        flashInstructions = sheet['A20']

    if questionType.lower() == 'open':
        if subSet == '1':
            rowRangeStart = 11
            rowRangeStop = 17

        elif subSet == '2':
            rowRangeStart = 21
            rowRangeStop = 27
        
        for row in range(rowRangeStart, rowRangeStop):
            questionCell = sheet.cell(row=row, column=1).value
            answerCell = sheet.cell(row=row, column=2).value
            questions.append(assets.question(questionCell, answerCell))

        correctQuestionAnswerPair = random.choice(questions)

    elif questionType.lower() == closed:
        pass

         

    
    return questions

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

    wrongAnswerList = [wrongAnswer for _ in range(5)]

    return rightQAPair, wrongAnswerList


def makeQuestionPanel(questionObj):

    questionFont = assets.pokeFont(30)
    text = questionFont.render(questionObj.question, 1, MAINTEXTCOLOR)
    textRect = text.get_rect()
    textRect.center = (WINDOWWIDTH/2, 30)

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




def game():
    sessionTeams = [assets.TeamA(), assets.TeamB()]
    random.shuffle(sessionTeams)
    for team in sessionTeams:
        scoreList = []
    
    while True:
        
        random.shuffle(sessionTeams)
        sessionTeams = main(sessionTeams)


if __name__ == "__main__":
    game()