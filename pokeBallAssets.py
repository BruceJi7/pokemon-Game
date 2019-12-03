import pygame, os, math


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

pygame.init()


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

def pokeFont(size=20):
    return pygame.font.SysFont('minecraft', size)

pokeBallFont = pokeFont(20)

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
        self.__surface = pygame.Surface((160, 160))
        self.__surface.fill(BKGCOLOR)
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



teamImagesPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\team'
teamImgs = {
    'bar': {
        'A': pygame.image.load(os.path.join(teamImagesPath, 'teamBarA.png')),
        'B': pygame.image.load(os.path.join(teamImagesPath, 'teamBarB.png')),
    },
    'pokeScore': pygame.image.load(os.path.join(teamImagesPath, 'scorePokeBall.png')),
    'greatScore': pygame.image.load(os.path.join(teamImagesPath, 'scoreGreatBall.png')),
}


POINTBALLPOSX = 36
POINTBALLPOSY = 0

class Team():
    def __init__(self, name):
        self.name = name
        self.scoreList = [] # contains pygame images for each 
        self.images = teamImgs

        self.barImg = self.images['bar'][self.name]

        self.teamSurf = pygame.Surface((154, 26), pygame.SRCALPHA)
        self.teamRect = self.teamSurf.get_rect()
        self.teamRectY = WINDOWHEIGHT - 100
        self.teamRectX = 20
        

        self.pointSurf = pygame.Surface((108,18), pygame.SRCALPHA)
        self.pointRect = self.pointSurf.get_rect()
        self.pointSpacing = 0



    # State Setter/Getter
    @property
    def score(self):
        return len(self.scoreList)
    

    def addPoint(self):
        self.scoreList.append(self.images['pokeScore'])

    def addGreatPoint(self):
        self.scoreList.append(self.images['greatScore'])

    def drawTeamLabel(self, targetSurf):
        ballX = 0
        ballY = 0
        self.teamSurf.blit(self.barImg, (0, 0))
        for ball in self.scoreList:
            self.pointSurf.blit(ball, (ballX, ballY))
            ballX += 18
        self.pointRect.topleft = (self.pointSpacing, 0)
        self.teamSurf.blit(self.pointSurf, self.pointRect)
        self.teamRect.topleft = (self.teamRectX, self.teamRectY)
        targetSurf.blit(self.teamSurf, self.teamRect)
             
    

    
class TeamA(Team):
    def __init__(self):
        super().__init__(name='A')

        self.barImg = self.images['bar']['A']
        self.teamRectX = 0
        self.pointSpacing = 20
        


class TeamB(Team):
    def __init__(self):
        super().__init__(name='B')

        self.barImg = self.images['bar']['B']
        self.teamRectX = (WINDOWWIDTH - 154 - 20)
        self.pointSpacing = 8
        














soundPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\sounds'

ballSound = pygame.mixer.Sound(os.path.join(soundPath, 'ballSwirl.ogg'))
ballOpenSound = pygame.mixer.Sound(os.path.join(soundPath, 'ballOpen.ogg'))



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




