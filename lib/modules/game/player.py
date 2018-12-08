import math
import pygame

from lib.modules.physics.vector import Vector
from lib.modules.physics.rigid_body import RigidBody
from lib.modules.gui.image import Image
from lib.modules.gui.events import *
from lib.modules.gui.text import Text

image_path = 'lib/data/assets/'

KEYS_MAP = [{'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'up': pygame.K_w, 'fire': pygame.K_f}, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'up': pygame.K_UP, 'fire': pygame.K_RCTRL}]


class Player(RigidBody):
    '''Models a player'''

    def __init__(self, keyboard_layout):
        '''Constructs a new player with rigid body as Base Class'''

        self._keys = KEYS_MAP[keyboard_layout]
        
        self._health = 10
        super().__init__(pygame.Rect(0, 0, 192, 192), 100)
        self._surface = Image(image_path+'test.png').return_surface()
        
    def update(self, events):
        '''To be called on every game tick'''
        pressed = events.keyboard().down
        delta_x = 0
        delta_y = 0

        change = 2*events.delta_time()

        if pressed(self._keys['left']):
            delta_x -= change

        if pressed(self._keys['right']):
            delta_x += change
            
        if pressed(self._keys['up']):
            delta_y -= change

        if pressed(self._keys['down']):
            delta_y += change
            
        if pressed(self._keys['fire']):
            pass
            #ADD CODE!!!!!!!!!!!!

        
        user_force = Vector((self.return_rect().centerx, self.return_rect().centery), x_component=delta_x, y_component=delta_y)
        super().apply_force(user_force)
        super().update()

    def return_true_rect(self):
        '''Return absolute rectangle coordinates in pygame rect'''
        return super().return_rect()
        
    def return_surface_and_pos(self):
        '''Returns array of surface and tuple of x and y position. (Used for easy blitting)'''
        return [self._surface, (self.return_rect()[0], self.return_rect()[1])]
