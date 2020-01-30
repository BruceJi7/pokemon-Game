import pygame, os, math, random


WINDOWWIDTH = 1024
WINDOWHEIGHT = 786


# Colours
WHITE           =(255, 255, 255)
BLACK           =(  0,   0,   0)
GREEN           =(  0, 200,   0)
RED             =(255,   0,   0)
CLEAR           =(  0,   0,   0,  0)


BKGCOLOR = WHITE
MAINTEXTCOLOR = BLACK

POINTBALLPOSX = 36
POINTBALLPOSY = 0


pygame.init()

def pokeFont(size=20):
    return pygame.font.SysFont('minecraft', size)

pokeBallFont = pokeFont(20)


alakaPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\alakazam'
alakazamImg = {
    'normal': pygame.image.load(os.path.join(alakaPath, 'alakazamNormal.png')),
    'blink': pygame.image.load(os.path.join(alakaPath, 'alakazamBlink.png')),
    'ouch': pygame.image.load(os.path.join(alakaPath, 'alakazamOuch.png')),
    'laugh': pygame.image.load(os.path.join(alakaPath, 'alakazamLaugh.png')),
}


pokeBallPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\pokeball'

pokeballImgs = {
    'open' : pygame.image.load(os.path.join(pokeBallPath, 'pokeballOpen.png')),
    'closed' : pygame.image.load(os.path.join(pokeBallPath, 'pokeballClosed.png')),
}

bkgPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\backgrounds'

backgrounds = {
    'grass' : pygame.image.load(os.path.join(bkgPath, 'grass.png')),
}



teamImagesPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\team'
teamImgs = {
    'bar': {
        'A': pygame.image.load(os.path.join(teamImagesPath, 'teamBarA.png')),
        'B': pygame.image.load(os.path.join(teamImagesPath, 'teamBarB.png')),
    },
    'turnIndicator':
    {
        'A': pygame.image.load(os.path.join(teamImagesPath, 'turnIndicatorA.png')),
        'B': pygame.image.load(os.path.join(teamImagesPath, 'turnIndicatorB.png')),
    },
    'pokeScore': pygame.image.load(os.path.join(teamImagesPath, 'scorePokeBall.png')),
    'greatScore': pygame.image.load(os.path.join(teamImagesPath, 'scoreGreatBall.png')),
}


menuPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\menu'
menuBKG = pygame.image.load(os.path.join(menuPath, 'menuTable.png'))

soundPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\sounds'

ballSound = pygame.mixer.Sound(os.path.join(soundPath, 'ballSwirl.ogg'))
ballOpenSound = pygame.mixer.Sound(os.path.join(soundPath, 'ballOpen.ogg'))
selectSound = pygame.mixer.Sound(os.path.join(soundPath, 'wink.ogg'))
ballBounceSound = pygame.mixer.Sound(os.path.join(soundPath, 'ballBounceSound.ogg'))
ballShakeSound = pygame.mixer.Sound(os.path.join(soundPath, 'ballShakeSound.ogg'))
catchFailSound = pygame.mixer.Sound(os.path.join(soundPath, 'catchFailSound.ogg'))
throwSound = pygame.mixer.Sound(os.path.join(soundPath, 'throwSound.ogg'))
critHitSound = pygame.mixer.Sound(os.path.join(soundPath, 'critHit.ogg'))
runAwaySound = pygame.mixer.Sound(os.path.join(soundPath, 'runAway.ogg'))
nopeSound = pygame.mixer.Sound(os.path.join(soundPath, 'nope.ogg'))
hitSound = pygame.mixer.Sound(os.path.join(soundPath, 'hit.ogg'))



musicPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\music'

music = {
    'johtoTrainerBattle' :
    {
        'intro' : os.path.join(musicPath, 'TrainerBattleIntro.ogg'),
        'main' : os.path.join(musicPath, 'TrainerBattleMain.ogg'),
    },
    'gymBattle' :
    {
        'intro' : os.path.join(musicPath, 'gymIntro.ogg'),
        'main' : os.path.join(musicPath, 'gymMain.ogg'),
    },
    'darkCave' :
    {
        'intro' : os.path.join(musicPath, 'darkIntro.ogg'),
        'main' : os.path.join(musicPath, 'darkMain.ogg'),
    },
    'route' :
    {
        'intro' : os.path.join(musicPath, 'routeIntro.ogg'),
        'main' : os.path.join(musicPath, 'routeMain.ogg'),
    },
    'menu' : {
        'intro' : os.path.join(musicPath, 'menuIntro.ogg'),
        'main' : os.path.join(musicPath, 'menuMain.ogg'),
    },
    'victory' : {
        'intro' : os.path.join(musicPath, 'mainVictoryIntro.ogg'),
        'main' : os.path.join(musicPath, 'mainVictoryMain.ogg'),
    },
    'bonus' : {
        'intro' : os.path.join(musicPath, 'bonusVictoryIntro.ogg'),
        'main' : os.path.join(musicPath, 'bonusVictoryMain.ogg'),
    }
}

bonusPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\bonus\pokes'
bonusPokemonImages = {
    'bulbasaur' : [os.path.join(bonusPath, 'bulbasaur.png'), 20],
    'squirtle' : [os.path.join(bonusPath, 'squirtle.png'), 20],
    'charmander' : [os.path.join(bonusPath, 'charmander.png'), 20],
    'charizard' : [os.path.join(bonusPath, 'charizard.png'), 10],
    'pikachu' : [os.path.join(bonusPath, 'pikachu.png'), 18],
    'raichu' : [os.path.join(bonusPath, 'raichu.png'), 12],
    'ekans' : [os.path.join(bonusPath, 'ekans.png'), 16],
    'eevee' : [os.path.join(bonusPath, 'eevee.png'), 18],
    'zapdos' : [os.path.join(bonusPath, 'zapdos.png'), 6],
    'mewtwo' : [os.path.join(bonusPath, 'mewtwo.png'), 3],
    'suicune' : [os.path.join(bonusPath, 'suicune.png'), 2],
}

bonusBallPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\bonus\ball'
bonusBallImages = {
    'P': {
        'closed': pygame.image.load(os.path.join(bonusBallPath, 'bonusPokeClosed.png')),
        'open': pygame.image.load(os.path.join(bonusBallPath, 'bonusPokeOpen.png')),
    },
    'G': {
        'closed': pygame.image.load(os.path.join(bonusBallPath, 'bonusGreatClosed.png')),
        'open': pygame.image.load(os.path.join(bonusBallPath, 'bonusGreatOpen.png')),
    },
}
bonusCatchPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\bonus\catchAnim'
bonusBallCatch = [pygame.image.load(os.path.join(bonusCatchPath, imageFile)) for imageFile in os.listdir(bonusCatchPath) if os.path.splitext(imageFile)[1] in ('.png', '.PNG')]

class bonusBall():
    def __init__(self):
        self.__Type = None
        self.dict = bonusBallImages
        self.__state = 'closed'
    
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, setState):
        self.__state = setState

    @property
    def ballType(self):
        return self.__type

    @ballType.setter
    def ballType(self, setType):
        self.__type = setType
    
    @property
    def surface(self):
        image = self.dict[self.ballType][self.state]
        newSurf = pygame.Surface((40, 60), pygame.SRCALPHA)
        newSurf.fill(BKGCOLOR)
        newSurf.blit(image, (0, 0))
        return newSurf


    @property
    def rect(self):
        return self.surface.get_rect()        

bonusPokeBall = bonusBall()



def getRandomPoke(imageDict=bonusPokemonImages):
    pokemonChanceList = []
    for value in imageDict.values():
        for _ in range(value[1]):
            pokemonChanceList.append(value[0])
    return random.choice(pokemonChanceList)


class bonusPokemon():
    def __init__(self, pokeImagePath):
        self.path = pokeImagePath
        self.rect = self.makeRect()

    @property
    def surface(self):
        return pygame.image.load(self.path)

    def makeRect(self):
        return self.surface.get_rect()      


class pokeball():
    def __init__(self, pathDict, message=None, state=None):
        self.path = pathDict
        self.__state = state
        self.__message = message
        self.__surface = None
        self.rect = self.makeRect()

        


    # State Setter/Getter
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, setState):
        self.__state = setState

    # Message Setter/Getter
    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, setMessage):
        self.__message = setMessage

    @property
    def surface(self):
        surfaceWidth = 180
        surfaceHeight = 90
        self.__surface = pygame.Surface((surfaceWidth, surfaceHeight), pygame.SRCALPHA)
        # self.__surface.convert_alpha
        self.__surface.fill(CLEAR)

        if self.state == 'closed':
            closedBall = self.path['closed']

            closedBallRect = closedBall.get_rect()
            closedBallRect.center = (surfaceWidth/2, surfaceHeight/2)
            self.__surface.blit(closedBall, closedBallRect)

            return self.__surface

        else:
            text = pokeBallFont.render(self.message, 1, MAINTEXTCOLOR)
            messageRect = text.get_rect()
            messageRect.center = (surfaceWidth/2, 50)

            openBall = self.path['open'].copy()
            openBallRect = openBall.get_rect()
            openBallRect.center = (surfaceWidth/2, surfaceHeight/2)

            self.__surface.blit(openBall, openBallRect)
            self.__surface.blit(text, messageRect)

            return self.__surface


    def makeRect(self):
        return self.surface.get_rect()

class alakazamChar():
    def __init__(self, path, state='normal', surface=None):
        self.path = path
        self.__state = state
        self.__surface = surface
        self.rect = self.makeRect()

    @property
    def state(self):
        return self.__state


    @state.setter
    def state(self, setState):
        self.__state = setState

    
    @property
    def surface(self):
        self.__surface = pygame.Surface((160, 160), pygame.SRCALPHA)
        # self.__surface.fill(BKGCOLOR)
        image = self.path[self.state]
        imgRect = image.get_rect()
        imgRect.center = (80, 80)
        self.__surface.blit(image, imgRect )
        return self.__surface
    
    def makeRect(self):
        return self.surface.get_rect()

alakazam = alakazamChar(alakazamImg)

class question():
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer




class Menubutton():
    def __init__(self, path, series, gameType, state='up', surface=None):
        self.path = path
        self.__state = state
        self.series = series
        self.gameType = gameType
        self.__surface = surface
        self.rect = self.makeRect()
        
        # self.surface = self.path[self.state]
        # self.rect = self.surface.get_rect()




    @property
    def state(self):
        return self.__state


    @state.setter
    def state(self, setState):
        self.__state = setState

    @property
    def surface(self):
        return self.path[self.state]

    def makeRect(self):
        return self.surface.get_rect()




class Team():
    def __init__(self, name):
        self.name = name
        self.scoreList = [] # Contains a letter for each type of point
        
        self.images = teamImgs
        self.isTurn = False

        self.barImg = self.images['bar'][self.name]

        self.turnIndicator = self.images['turnIndicator'][self.name]
        self.turnIndicatorX = 20 + 100
        self.turnIndicatorY = WINDOWHEIGHT - 80

        self.teamSurf = pygame.Surface((154, 70), pygame.SRCALPHA)
        self.teamRect = self.teamSurf.get_rect()
        self.teamRectY = WINDOWHEIGHT - 120
        self.teamRectX = 20
        

        self.pointSurf = pygame.Surface((108,18), pygame.SRCALPHA)
        self.pointRect = self.pointSurf.get_rect()
        self.pointSpacing = 0

        self.labelText = f'Team {self.name}'



    # State Setter/Getter
    @property
    def score(self):
        return len(self.scoreList)
    
        
    @property
    def hasWon(self):
        if self.score >= 4:
            return True
        else:
            return False

    def addPoint(self):
        self.scoreList.append('P')

    def addGreatPoint(self):
        self.scoreList.append('G')

    @property
    def popPoint(self):
        scoreList = self.scoreList
        lastPoint = scoreList.pop()
        self.scoreList = scoreList
        return lastPoint

    

    def drawTeamLabel(self, targetSurf):
        ballX = 0
        ballY = 0
        self.teamSurf.blit(self.barImg, (0, 0))
        # self.pointSurf.fill(BKGCOLOR)
        for ball in self.scoreList:
            if ball == "P":
                ballImage = self.images['pokeScore']
            elif ball == "G":
                ballImage = self.images['greatScore']
                 # Calculate how many balls to show
            self.pointSurf.blit(ballImage, (ballX, ballY))
            ballX += 18

        self.pointRect.topleft = (self.pointSpacing, 0)
        self.teamSurf.blit(self.pointSurf, self.pointRect) # Add balls to main surface

        teamLabel = pokeFont().render(self.labelText, 1, MAINTEXTCOLOR)
        teamLabelRect = teamLabel.get_rect()
        teamLabelRect.topleft = ((20, 40))
        self.teamSurf.blit(teamLabel, teamLabelRect)

        self.teamRect.topleft = (self.teamRectX, self.teamRectY)
        targetSurf.blit(self.teamSurf, self.teamRect)

    def drawTurnIndicator(self, targetSurf):
        turnIndicatorRect = self.turnIndicator.get_rect()
        turnIndicatorRect.topleft = (self.turnIndicatorX, self.turnIndicatorY)
        targetSurf.blit(self.turnIndicator, turnIndicatorRect)         
    

    
class TeamA(Team):
    def __init__(self):
        super().__init__(name='A')

        self.barImg = self.images['bar']['A']
        self.teamRectX = 20
        self.pointSpacing = 20
        


class TeamB(Team):
    def __init__(self):
        super().__init__(name='B')

        self.barImg = self.images['bar']['B']
        self.teamRectX = (WINDOWWIDTH - 154 - 20)
        self.turnIndicatorX = (WINDOWWIDTH - 154 - 20) 
        self.pointSpacing = 8
        














# Trig Functions
def degToRadian(deg):
    return deg * math.pi / 180

def getXcoord(deg, hypo):
    # The sin of the degree is equal to ANS divided by HYPO
    # Get sin of degree.
    # Multiply this number by the HYPO
    # This will be the length co-ord
    radA = degToRadian(deg)
    sinA = math.sin(radA)
    xLength = sinA * hypo

    return xLength

def getYcoord(deg, hypo):
    # The same but wit COSINE I think.
    radA = degToRadian(deg)
    cosA = math.cos(radA)
    yLength = cosA * hypo
    return yLength

def getTrigoXY(deg, hypo):
    x = getXcoord(deg, hypo)
    y = getYcoord(deg, hypo)
    intx = int(x)
    inty = int(y)
    return (intx, inty)

def getTrigoFromCenter(deg, hypo, WINDOWWIDTH, WINDOWHEIGHT):
    trigX, trigY = getTrigoXY(deg, hypo)

    return (trigX + WINDOWWIDTH/2, trigY+WINDOWHEIGHT/2)

def getTrigoForArc(deg, hypo, centreX, centreY):
    trigX, trigY = getTrigoXY(deg, hypo)

    return (trigX + centreX, trigY+centreY)


