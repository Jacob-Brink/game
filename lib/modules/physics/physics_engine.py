from lib.modules.physics.vector import Vector
from lib.modules.physics.line import Line
from lib.modules.gui.rectangle import Rectangle
from lib.modules.physics.physics import Collision
import copy

import math
import pygame

def list_points(_rect):
    '''Return points in clockwise order'''
    return [_rect.topleft, _rect.topright, _rect.bottomright, _rect.bottomleft]

class Physics:

    def __init__(self, debug_mode=False):
        '''Construct Physics object'''
        self._debug_mode = debug_mode
        self._collision = Collision()
        self._MARGIN_PIXEL = 1

    def return_new_rect_reposition(self, past_rect, platform):
        '''Checks rigid body against platform'''
        rect = copy.copy(past_rect)
        side = None
        
        
        if past_rect.get_y()+past_rect.get_h() <= platform.get_y():
            print('correcting top')
            rect = Rectangle(rect.get_x(), platform.get_y()-rect.get_h()-self._MARGIN_PIXEL, rect.get_w(), rect.get_h())
            side = 'on_platform'
        # on bottom
        if past_rect.get_y() >= platform.get_y() + platform.get_h():
            print('correcting bottom')
            rect = Rectangle(rect.get_x(), platform.get_y()+platform.get_h()+self._MARGIN_PIXEL, rect.get_w(), rect.get_h())
            side = 'beneath_platform'
        # on left
        if past_rect.get_x() >= platform.get_x() + platform.get_w():
            print('correcting to left')
            rect = Rectangle(platform.get_x()+platform.get_w()+self._MARGIN_PIXEL, rect.get_y(), rect.get_w(), rect.get_h())
            side = 'right_platform'
        # on right
        if past_rect.get_x()+past_rect.get_w() <= platform.get_x():
            print('correcting to right')
            rect = Rectangle(platform.get_x()-past_rect.get_w()-self._MARGIN_PIXEL, rect.get_y(), rect.get_w(), rect.get_h())
            side = 'left_platform'

        print(rect, platform)
        print(str(rect), ' collided with ', str(platform), ' at side', side)

        return rect, side

        
    def reposition(self, player_list, rigid_body_list, immovable_rect_list, delta_time):
        '''Return new rectangle based on how two rectangles collided'''


        
        for player in player_list:
            player.reset_platform_status()
            
            for platform in immovable_rect_list:
            # if a collision occurs, figure out how what side the player collided
                if self._collision.rect_rect(player.return_rect(), platform):
                    past_rect = player.return_past_rect()
                    repositioned = self.return_new_rect_reposition(past_rect, platform)
                    player.set_rect(repositioned[0])
                    player.change_platform_status(repositioned[1], True)
                    
                    # apply appropriate force
                    print('Collision Occurred')
                    player.set_velocity(Vector(player.return_rect().get_center(), magnitude=0, direction=0))
                    


    def update(self, events, player_list, rigid_body_list, platform_list):
        '''Calculate collisions, reposition from collisions, work with forces, etc'''        
        
        for player in player_list:
            player.update(events)

        
        self.reposition(player_list, rigid_body_list, platform_list, events.delta_time())

        
if __name__ == '__main__':
    '''Tests'''

    p = Physics()
    rectangle = pygame.Rect(0,0,10, 5)
    vertical = Vector((0,0), direction=0, magnitude=50)
    print(p.return_greatest_parallelogram(rectangle, vertical))

    
