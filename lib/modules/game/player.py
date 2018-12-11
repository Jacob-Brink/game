import math
import pygame

from lib.modules.physics.vector import Vector
from lib.modules.physics.rigid_body import RigidBody
from lib.modules.gui.image import Image
from lib.modules.gui.events import *
from lib.modules.gui.text import Text
from lib.modules.gui.rectangle import Rectangle
from lib.modules.game.bomb import Bomb

from lib.modules.physics.physics import PlatformStatus

import time

class Timer:

    def __init__(self):
        '''Construct timer'''
        self._running = False
    
    def start(self, time):
        '''Start timer with given time remaining'''
        self._time = time.monotonic()
        self._running = True
        
    def read(self):
        '''Return time remaining'''
        return time.monotonic()-self._time if self._running else -1

    def stop(self):
        '''Stop timer from running'''
        self._running = False
        self._time = time.monotonic()
        
    def reset(self):
        '''Reset timer'''
        self._time = time.monotonic()


image_path = 'lib/data/assets/'

KEYS_MAP = [{'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'up': pygame.K_w, 'fire': pygame.K_f}, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'up': pygame.K_UP, 'fire': pygame.K_RCTRL}]


class Player(RigidBody):
    '''Models a player'''

    def __init__(self, keyboard_layout, debug_mode):
        '''Constructs a new player with rigid body as Base Class'''

        self._surface = Image(image_path+'test.png').return_surface()
        super().__init__(Rectangle((0,0), self._surface.get_size()), 100)

        self._debug = debug_mode
        self._player_num = keyboard_layout
        self._keys = KEYS_MAP[keyboard_layout]

        self._timer = Timer()

        self._jump_limit = 2
        self._jumps = 0
        
        self._health = 10

        
    def jump(self, change):
        '''Adds upward velocity'''
        if super().get_platform_status(PlatformStatus.on_top) and self._timer.read() == -1:
            self._jumps = 0
            super().add_velocity(Vector(super().return_rect().get_center(), x_component=0, y_component=-change))

        elif self._jumps < self._jump_limit and self._timer.read() > 1:
            self._jumps += 1
            super().add_velocity(Vector(self.return_rect().get_center(), x_component=0, y_component=-change))
            
    def fire_bomb(self):
        '''Fires bomb'''
        
        

                
    def update(self, events):
        '''To be called on every game tick'''
        pressed = events.keyboard().down
        delta_x = 0
        delta_y = 0

        change = .1*events.delta_time()

        if pressed(self._keys['left']) and  not super().get_platform_status(PlatformStatus.on_right):
            delta_x -= change

        if pressed(self._keys['right']) and not super().get_platform_status(PlatformStatus.on_left):
            delta_x += change
            
        if pressed(self._keys['up']) and not super().get_platform_status(PlatformStatus.on_bottom):
            self.jump(change)

        if pressed(self._keys['down']):
            delta_y += change
            
        if pressed(self._keys['fire']):
            self.fire_bomb()

        user_velocity = Vector(self.return_rect().get_center(), x_component=delta_x, y_component=delta_y)

        super().add_velocity(user_velocity)
        super().update()
        
    def return_surface_and_pos(self):
        '''Returns array of surface and point of x and y position. (Used for easy blitting)'''

        if self._debug:
            return [Text('Player'+str(self._player_num) + 'Pos: ' + str(super().return_rect()), 64, (200,255,255), 'left', 10).get_surface(), super().return_rect().get_top_left()]
        else:
            return [self._surface, super().return_rect().get_top_left()]
