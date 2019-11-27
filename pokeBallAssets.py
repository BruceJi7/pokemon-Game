import pygame, os



# Colours
WHITE           =(255, 255, 255)
BLACK           =(  0,   0,   0)
GREEN           =(  0, 200,   0)
RED             =(255,   0,   0)

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


def pokeFont(size=20):
    return pygame.font.SysFont('minecraft', size)

pokeBallFont = pokeFont(40)

class pokeball():
    def __init__(self, pathDict, message=None, state=None, surface=None):
        self.path = pathDict
        self.__state = state
        self.__message = message
        # self.__surface = surface
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
        if self.state == 'closed':
            return self.path['closed']
        else:
            text = pokeBallFont.render(self.message, 1, WHITE)
            messageRect = text.get_rect()
            messageRect.center = (80, 140)
            selfSurf = self.path['open'].copy()
            selfSurf.blit(text, messageRect)
            return selfSurf


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