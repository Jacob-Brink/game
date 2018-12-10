from lib.modules.physics.vector import Vector
from lib.modules.physics.line import Line
from lib.modules.gui.rectangle import Rectangle
from lib.modules.physics.physics import Collision

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
    
    def reposition(self, player_list, rigid_body_list, immovable_rect_list, delta_time):
        '''Return new rectangle based on how two rectangles collided'''
        MARGIN_PIXEL = 1


        
        for player in player_list:
            player.reset_platform_status()
            
            for platform in immovable_rect_list:
            # if a collision occurs, figure out how what side the player collided
                if self._collision.rect_rect(player.return_rect(), platform):
                    past_rect = player.return_past_rect()
                    rect = player.return_rect()
                    body_velocity = player.return_velocity_vector()

                    
                    print('body_velocity.return_direction()',  body_velocity.return_direction())

                    direction = player.return_past_velocity().return_direction()


                    if  45 < direction <= 135:
                        # player is on top
                        print('player on top')
                        player.set_rect(Rectangle(rect.get_x(), platform.get_y()-rect.get_h()-MARGIN_PIXEL, rect.get_w(), rect.get_h()))
                        player.change_platform_status('top_platform', True)

                    elif 135 < direction <= 180 or -180 < direction <= -135:
                        # player is to left
                        print('player on left')
                        player.set_rect(Rectangle(platform.get_x()+platform.get_w()+MARGIN_PIXEL, rect.get_y(), rect.get_w(), rect.get_h()))
                        player.change_platform_status('right_platform', True)
                        
                    elif -135 < direction <= -45:
                        # player is on bottom
                        print('player on bottom')

                        player.set_rect(Rectangle(rect.get_x(), platform.get_y()+platform.get_h()+MARGIN_PIXEL, rect.get_w(), rect.get_h()))
                        player.change_platform_status('beneath_platform', True)
                        
                    elif -45 < direction <= 0 or 0 < direction <= 45:
                        # player is on right
                        print('player on right')

                        player.set_rect(Rectangle(platform.get_x()-rect.get_w()-MARGIN_PIXEL, rect.get_y(), rect.get_w(), rect.get_h()))
                        player.change_platform_status('left_platform', True)

                    
                        '''    
                    # on top
                    if past_rect.get_y()+past_rect.get_h() <= platform.get_y():
                        print('correcting top')
                        player.set_rect(Rectangle(rect.get_x(), platform.get_y()-rect.get_h()-MARGIN_PIXEL, rect.get_w(), rect.get_h()))
                        player.change_platform_status('on_platform', True)
                    # on bottom
                    if past_rect.get_y() >= platform.get_y() + platform.get_h():
                        print('correcting bottom')
                        player.set_rect(Rectangle(rect.get_x(), platform.get_y()+platform.get_h()+MARGIN_PIXEL, rect.get_w(), rect.get_h()))
                        player.change_platform_status('beneath_platform', True)
                    # on left
                    if past_rect.get_x() >= platform.get_x() + platform.get_w():
                        print('correcting to left')
                        player.set_rect(Rectangle(platform.get_x()+platform.get_w()+MARGIN_PIXEL, rect.get_y(), rect.get_w(), rect.get_h()))
                        player.change_platform_status('right_platform', True)
                    # on right
                    if past_rect.get_x()+past_rect.get_w() <= platform.get_x():
                        print('correcting to right')
                        player.set_rect(Rectangle(platform.get_x()-rect.get_w()-MARGIN_PIXEL, rect.get_y(), rect.get_w(), rect.get_h()))
                        player.change_platform_status('left_platform', True)


                    '''
                    # apply appropriate force
                    print('Collision Occurred')
                    player.set_velocity(body_velocity*(-1))
                    


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

    
