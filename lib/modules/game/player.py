import math
import pygame

from lib.modules.physics.vector import Vector
from lib.modules.physics.rigid_body import RigidBody
from lib.modules.gui.image import Image
from lib.modules.gui.events import *
from lib.modules.gui.text import Text
from lib.modules.gui.rectangle import Rectangle

image_path = 'lib/data/assets/'

KEYS_MAP = [{'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'up': pygame.K_w, 'fire': pygame.K_f}, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'up': pygame.K_UP, 'fire': pygame.K_RCTRL}]


class Player(RigidBody):
    '''Models a player'''

    def __init__(self, keyboard_layout, debug_mode):
        '''Constructs a new player with rigid body as Base Class'''

        super().__init__(Rectangle((0,0), (400, 400)), 100)
        print('Player Rect', super().return_rect().get_x())
        print(keyboard_layout, debug_mode)
        self._debug = debug_mode
        self._player_num = keyboard_layout
        self._keys = KEYS_MAP[keyboard_layout]
        
        self._health = 10
        self._surface = Image(image_path+'test.png').return_surface()
        
    def update(self, events):
        '''To be called on every game tick'''
        pressed = events.keyboard().down
        delta_x = 0
        delta_y = 0

        change = 1*events.delta_time()

        if pressed(self._keys['left']) and  not super().get_platform_status('right_platform'):
                delta_x -= change

        if pressed(self._keys['right']) and not super().get_platform_status('left_platform'):
                delta_x += change
            
        if pressed(self._keys['up']) and not super().get_platform_status('beneath_platform'):
                delta_y -= change

        if pressed(self._keys['down']) and not super().get_platform_status('on_platform'):
                delta_y += change
            
        if pressed(self._keys['fire']):
            pass
            #ADD CODE!!!!!!!!!!!!

        user_force = Vector(self.return_rect().get_center(), x_component=delta_x, y_component=delta_y)
        print(user_force.return_direction())
        super().apply_force(user_force)
        super().update()
        
    def return_surface_and_pos(self):
        '''Returns array of surface and point of x and y position. (Used for easy blitting)'''

        if self._debug:
            return [Text('Player'+str(self._player_num) + 'Pos: ' + str(super().return_rect()), 64, (200,255,255), 'left', 10).get_surface(), super().return_rect().get_top_left()]
        else:
            return [self._surface, super().return_rect().get_top_left()]
