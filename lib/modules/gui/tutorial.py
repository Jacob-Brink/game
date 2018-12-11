from lib.modules.gui.editor import Editor
from lib.modules.game.game import Game

from lib.modules.gui.

TUTORIAL_STAGE = [

    {'Game': 'To move around, use wasd for player 1, arrow keys for player 2'},
    {'Game': 'To fire a bomb, press f for player 1, right control key for player 2'},
    {'Editor': 'To start drawing a platform, press 1 to select the platform brush'},
    {'Editor': 'To draw a platform, simply left click and drag to make the platform'},
    {'Editor': 'To erase a platform, press 2 to select eraser'}
    
]

class Tutorial(View):

    def __init__(self, go_back, screen):
        '''Constructs Tutorial'''
        super().__init__(screen)
        self._go_back_callback = go_back
        self._step = 0
        self._game
        
    def update(events):
        '''Update tutorial'''
        if 
