import pygame, os, math



# Colours
WHITE           =(255, 255, 255)
BLACK           =(  0,   0,   0)
GREEN           =(  0, 200,   0)
RED             =(255,   0,   0)
CLEAR           =(  0,   0,   0,   0)


backGroundColour = BLACK

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

alakaPath = r'C:\Users\Administrator\Google 드라이브\ASPython\Pokemon Game\pokemonGame\assets\alakazam'
alakazamImg = {
    'normal': pygame.image.load(os.path.join(alakaPath, 'alakazamNormal.png')),
    'blink': pygame.image.load(os.path.join(alakaPath, 'alakazamBlink.png')),
    'ouch': pygame.image.load(os.path.join(alakaPath, 'alakazamOuch.png')),
    'laugh': pygame.image.load(os.path.join(alakaPath, 'alakazamLaugh.png')),
}


pokeBallPath = r'C:\Users\Administrator\Google 드라이브\ASPython\Pokemon Game\pokemonGame\assets\pokeball'

pokeballImgs = {
    'open' : pygame.image.load(os.path.join(pokeBallPath, 'pokeballOpen.png')),
    'closed' : pygame.image.load(os.path.join(pokeBallPath, 'pokeballClosed.png')),
}

# quickBall = pokeBallImgs['closed']

def pokeFont(size=20):
    return pygame.font.SysFont('minecraft', size)

pokeBallFont = pokeFont(25)

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
        self.__surface = pygame.Surface((180, 200))
        self.__surface.convert_alpha
        self.__surface.fill(CLEAR)

        if self.state == 'closed':
            closedBall = self.path['closed']
            closedBallRect = closedBall.get_rect()
            closedBallRect.center = (90, 100)
            self.__surface.blit(closedBall, closedBallRect)

            return self.__surface

        else:
            text = pokeBallFont.render(self.message, 1, WHITE)
            messageRect = text.get_rect()
            messageRect.center = (90, 100)

            openBall = self.path['open'].copy()
            openBallRect = openBall.get_rect()
            openBallRect.center = (90, 100)

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
        return self.path[self.state]
    
    def makeRect(self):
        return self.surface.get_rect()

alakazam = alakazamChar(alakazamImg)

class question():
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer


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




