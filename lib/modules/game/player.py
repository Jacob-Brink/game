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
from lib.modules.game.timer import Timer

class HealthBar(Rectangle):

    def __init__(self, rectangle):
        '''Constructs a health bar'''
        super().__init__(rectangle.get_top_left(), rectangle.get_size())
        self._green = 255
        self._red = 0
        self._initial_width = super().get_w()

    def get_color(self):
        '''Sets color based on red and green values'''
        print('Color: (', self._red, ',', self._green, ',', 0)
        return (self._red, self._green, 0)
    
    def change_percentage(self, percentage):
        '''Given percentage, will change the width of the rectangle filling the outside rectangle'''
        if percentage > 1 or percentage < 0:
            raise ValueError('HealthBar->change_percentage: percentage must be a value between 0 and 1')
        self._green = 255*percentage
        self._red = 255*(1-percentage)

        
        original_position = super().get_top_left()
        super().change_width(self._initial_width*percentage)
        super().change_top_left(original_position)

        
image_path = 'lib/data/assets/'

KEYS_MAP = [{'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'up': pygame.K_w, 'fire': pygame.K_f}, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'up': pygame.K_UP, 'fire': pygame.K_RCTRL}]


class Player(RigidBody):
    '''Models a player'''

    def __init__(self, keyboard_layout, debug_mode, throw_bomb_callback):
        '''Constructs a new player with rigid body as Base Class'''

        self._surface = Image(image_path+'test.png').return_surface()
        super().__init__(Rectangle((0,0), self._surface.get_size()), 100)

        self._debug = debug_mode
        self._player_num = keyboard_layout
        self._keys = KEYS_MAP[keyboard_layout]

        self._jump_timer = Timer()
        self._jump_limit = 2
        self._jumps = 0

        self._alive = True
        self._health_total = 10
        self._health = 10
        self._health_bar = HealthBar(Rectangle((0,0), (100, 20)))
        
        self._throw_bomb_callback = throw_bomb_callback
        self._bomb_timer = Timer()

        
    def jump(self, change):
        '''Adds upward velocity'''
        if super().get_platform_status(PlatformStatus.on_top) and self._jump_timer.read() == -1:
            self._jumps = 0
            super().add_velocity(Vector(super().return_rect().get_center(), x_component=0, y_component=-change))
            self._jump_timer.restart()
            
        elif self._jumps < self._jump_limit and self._jump_timer.read() > 1:
            self._jumps += 1
            super().add_velocity(Vector(self.return_rect().get_center(), x_component=0, y_component=-change))
            self._jump_timer.stop()

            
    def fire_bomb(self):
        '''Fires bomb'''
        # when timer is stopped, call callback
        if self._bomb_timer.read() == -1:
            self._throw_bomb_callback(super().return_velocity_vector())
            self._bomb_timer.restart()

        # reset timer after 2 seconds
        elif self._bomb_timer.read() > .5:
            self._bomb_timer.stop()

            
    def update(self, events):
        '''To be called on every game tick'''
        pressed = events.keyboard().down
        delta_time = events.delta_time()
        delta_x = 0
        delta_y = 0

        change = 5

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

        self._health_bar.change_bottom_left(super().return_rect().get_top_left())
        super().add_velocity(user_velocity)
        super().update(delta_time)

        
    def is_alive(self):
        '''Returns true if player is still alive'''
        return self._alive

    
    def change_health(self, health_delta):
        '''Changes health'''
        self._health -= health_delta
        
        if self._health < 0:
            self._alive = False
        else:
            self._health_bar.change_percentage(self._health/self._health_total)
            
            
    def return_healthbar_and_color(self):
        '''Return rectangle and color'''
        return self._health_bar, self._health_bar.get_color()

    
    def return_surface_and_pos(self):
        '''Returns array of surface and point of x and y position. (Used for easy blitting)'''

        if self._debug:
            return [Text('Player'+str(self._player_num) + 'Pos: ' + str(super().return_rect()), 64, (200,255,255), 'left', 10).get_surface(), super().return_rect().get_top_left()]
        else:
            return [self._surface, super().return_rect().get_top_left()]
