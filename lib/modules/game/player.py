import math
import pygame

from lib.modules.physics.vector import Vector
from lib.modules.physics.rigid_body import RigidBody
from lib.modules.gui.image import Image
from lib.modules.gui.events import *
from lib.modules.gui.text import Text
from lib.modules.gui.rectangle import Rectangle, Point
from lib.modules.game.bomb import Bomb
from lib.modules.physics.physics import PlatformStatus
from lib.modules.game.timer import Timer

# Map of keys
KEYS_MAP = [{'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'up': pygame.K_w, 'fire explosion': pygame.K_f, 'fire implosion': pygame.K_r}, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'up': pygame.K_UP, 'fire explosion': pygame.K_RCTRL, 'fire implosion': pygame.K_RSHIFT}]

# player color
PLAYER_COLOR = [(255, 0, 0), (0, 0, 255)]

# size and offsets
HEALTH_BAR_SIZE = Point(100, 20)
OFFSET = HEALTH_BAR_SIZE.y()*5


class HealthBar(Rectangle):
    '''Models a health bar'''
    def __init__(self, rectangle):
        '''Constructs a health bar'''
        super().__init__(rectangle.get_top_left(), rectangle.get_size())
        self._green = 255
        self._red = 0
        self._initial_width = super().get_w()
        
    def get_color(self):
        '''Sets color based on red and green values'''
        return (self._red, self._green, 0)
    
    def change_percentage(self, percentage):
        '''Given percentage, will change the width of the rectangle filling the outside rectangle'''
        if percentage > 1 or percentage < 0:
            raise ValueError('HealthBar->change_percentage: percentage must be a value between 0 and 1')
        self._green = 255*percentage
        self._red = 255*(1-percentage)

        # change rectangle width without moving left position
        original_position = super().get_top_left()
        super().change_width(self._initial_width*percentage)
        super().change_top_left(original_position)



class Player(RigidBody):
    '''Models a player'''

    def __init__(self, start_position_point, keyboard_layout, debug_mode, throw_bomb_callback):
        '''Constructs a new player with rigid body as Base Class'''

        super().__init__(Rectangle(start_position_point, Point(100,150)), 200)

        self._color = PLAYER_COLOR[keyboard_layout]
        
        self._debug = debug_mode
        self._player_num = keyboard_layout
        self._keys = KEYS_MAP[keyboard_layout]

        self._x_velocity_max = 10
        self._change = 13
    
        self._alive = True
        self._health_total = 10
        self._health = 10
        self._health_bar = HealthBar(Rectangle(Point(0,0), HEALTH_BAR_SIZE))

        
        self._jump_timer = Timer()
        self._jump_timer.restart()
        self._jump_limit = 2
        self._jumps = 0
        
        self._throw_bomb_callback = throw_bomb_callback
        self._bomb_reload_timer = Timer()
        self._bomb_reload_timer.restart()
        self._bomb_reload_time = .1
        self._bomb_speed = 200

        # 1 indicates facing right, while -1 indicates facing left
        self._facing = 1

        
    def fire_bomb(self, bomb_type):
        '''Fires bomb'''
        p_vector = super().return_velocity_vector()
        
        # if reload time has ended throw next bomb
        if self._bomb_reload_timer.read() > self._bomb_reload_time:
            self._throw_bomb_callback(p_vector+Vector(self.return_rect().get_center(), x_component=self._facing*self._bomb_speed, y_component=-self._bomb_speed), bomb_type)
            self._bomb_reload_timer.restart()
        
            
    def update(self, events):
        '''To be called on every game tick'''
        is_pressed = events.keyboard().is_pressed
        delta_x = 0
        delta_y = 0

        x_component_velocity = super().return_velocity_vector().return_x_component()
        p_status = super().get_platform_status
        
        
        # fire explosive bomb
        if is_pressed(self._keys['fire explosion']) == Switch.pushed_up:
            self.fire_bomb('explosion')

        # fire implosive bomb
        if is_pressed(self._keys['fire implosion']) == Switch.pushed_up:
            self.fire_bomb('implosion')

        
            
        if not p_status(PlatformStatus.on_top) and not p_status(PlatformStatus.on_left) and not p_status(PlatformStatus.on_right) and not p_status(PlatformStatus.on_bottom):

            if is_pressed(self._keys['left']) == Switch.down:
                delta_x -= .1*self._change
                self._facing = -1
                
            if is_pressed(self._keys['right']) == Switch.down:
                delta_x += .1*self._change
                self._facing = 1
                
        else:

            # go left when left key is pressed
            if is_pressed(self._keys['left']) == Switch.down and not p_status(PlatformStatus.on_right) and x_component_velocity > -self._x_velocity_max:
                delta_x -= self._change
                self._facing = -1

            # go right when right key is pressed
            if is_pressed(self._keys['right']) == Switch.down and not p_status(PlatformStatus.on_left) and x_component_velocity < self._x_velocity_max:
                delta_x += self._change
                self._facing = 1

                          
            # apply friction
            if (is_pressed(self._keys['right']) == Switch.up and is_pressed(self._keys['left']) == Switch.up):
                
                if x_component_velocity > 0:
                    delta_x -= .4*x_component_velocity
                elif x_component_velocity < 0:
                    delta_x -= .4*x_component_velocity

            # jump
            if is_pressed(self._keys['up']) == Switch.pushed_down and (not p_status(PlatformStatus.on_bottom)) and p_status(PlatformStatus.on_top):

                    delta_y -= self._change*5



                          
        # compile velocity from key presses    
        user_velocity = Vector(self.return_rect().get_center(), x_component=delta_x, y_component=delta_y)
        super().add_velocity(user_velocity)

        delta_time = events.delta_time()
        super().update(delta_time)

        # set health bar rectangle to be above player
        self._health_bar.change_bottom_left(super().return_rect().get_top_left()+Point(0,-OFFSET/4))
        
    def is_alive(self):
        '''Returns true if player is still alive'''
        return self._alive

    
    def change_health(self, health_delta):
        '''Changes health'''
        self._health -= health_delta
        
        if self._health <= 0:
            self._alive = False
            self._health = 0
            self._health_bar.change_percentage(self._health/self._health_total)
        else:
            self._health_bar.change_percentage(self._health/self._health_total)
            
            
    def return_healthbar_and_color(self):
        '''Return rectangle and color'''
        return self._health_bar, self._health_bar.get_color()

    def return_surface_and_pos(self):
        '''Returns debug mode surface'''
        return [Text('Player '+str(self._player_num), 64, (200,255,255), 'left', 10).get_surface(), super().return_rect().get_top_left()+Point(0,-OFFSET)]
    
    def return_rectangle_and_color(self):
        '''Returns array of surface and point of x and y position. (Used for easy blitting)'''
        return [super().return_rect().copy(), self._color]
