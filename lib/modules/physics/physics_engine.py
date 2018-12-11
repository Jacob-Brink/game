from lib.modules.physics.vector import Vector
from lib.modules.physics.line import Line
from lib.modules.gui.rectangle import Rectangle
from lib.modules.physics.physics import Collision, PlatformStatus


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
        self._gravity_force_magnitude = 10
        
    def next_to(self, value, side_value):
        return side_value - 4 <= value <= side_value + 4
        
    def return_side_platform(self, rect, platform):
        '''Returns which side the rectangle is adjacent to'''

        # rectangle overlaps platform's x coordinates
        if self._collision.one_dimensional_collision((rect.get_x(), rect.get_w()),(platform.get_x(), platform.get_w())):
            # on top
            if self.next_to(rect.get_y()+rect.get_h(), platform.get_y()):
                return PlatformStatus.on_top
            # on bottom
            if self.next_to(rect.get_y(), platform.get_y()+platform.get_h()):
                return PlatformStatus.on_bottom

        # rectangle overlaps platform's y coordinates
        elif self._collision.one_dimensional_collision((rect.get_y(), rect.get_h()),(platform.get_y(), platform.get_h())):
            # on left
            if self.next_to(rect.get_x()+rect.get_w(), platform.get_x()):
                return PlatformStatus.on_left
            # on right
            if self.next_to(rect.get_x(), platform.get_x()+platform.get_w()):
                return PlatformStatus.on_right
        
        return PlatformStatus.alone
        
    def return_new_rect_reposition(self, past_rect, platform):
        '''Checks rigid body against platform, Returns repositioned rectangle'''
        rect = past_rect.copy()

        # on top
        if past_rect.get_y()+past_rect.get_h() <= platform.get_y():
            rect = Rectangle(rect.get_x(), platform.get_y()-rect.get_h()-self._MARGIN_PIXEL, rect.get_w(), rect.get_h())

        # on bottom
        if past_rect.get_y() >= platform.get_y() + platform.get_h():
            rect = Rectangle(rect.get_x(), platform.get_y()+platform.get_h()+self._MARGIN_PIXEL, rect.get_w(), rect.get_h())

        # on left
        if past_rect.get_x() >= platform.get_x() + platform.get_w():
            rect = Rectangle(platform.get_x()+platform.get_w()+self._MARGIN_PIXEL, rect.get_y(), rect.get_w(), rect.get_h())

        # on right
        if past_rect.get_x()+past_rect.get_w() <= platform.get_x():
            rect = Rectangle(platform.get_x()-past_rect.get_w()-self._MARGIN_PIXEL, rect.get_y(), rect.get_w(), rect.get_h())

        return rect

                       

    def update(self, events, player_list, bomb_list, platform_list):
        '''Calculate collisions, reposition from collisions, work with forces, etc'''        

        delta_time = events.delta_time()
        
        # updates bomb rigid body
        for bomb in bomb_list:

            bomb.update(delta_time)

            if bomb.exploded():

                for player in player_list:
                    
                    p_center = player.return_rect().get_center()
                    b_center = bomb.return_rect().get_center()
                    dist_centers = math.sqrt((p_center.x()-b_center.x())**2+(b_center.y()-p_center.y())**2)
                    player.apply_force(Vector(p_center, direction=math.degrees(math.atan2(p_center.x()-b_center.x(),p_center.y()-b_center.y())), magnitude=(bomb.get_radius()/(.1+dist_centers))*300))

                    player.change_health(-.1)
                        
                
                bomb_list.remove(bomb)
    
        # updates, checks collision, and if collision occurs corrects and sets appropriate PlatformStatus value for player
        for player in player_list:

            player.update(events)

            # reset player platform status to all be False
            player.reset_platform_status()

            
            for platform in platform_list:

                # if a collision occurs, figure out how what side the player collided
                if player.return_rect().collides_with(platform):

                    # reposition player
                    player.set_rect(self.return_new_rect_reposition(player.return_past_rect(), platform))                  

                    # set velocity to 0
                    player.set_velocity(Vector(player.return_rect().get_center(), x_component=0, y_component=0))


                player.change_platform_status(self.return_side_platform(player.return_rect(), platform), True)

            if not player.get_platform_status(PlatformStatus.on_top):
                player.apply_force(Vector(player.return_rect().get_center(), x_component=0, y_component=self._gravity_force_magnitude))

        


            

        
if __name__ == '__main__':
    '''Tests'''

    p = Physics()
    rectangle = pygame.Rect(0,0,10, 5)
    vertical = Vector((0,0), direction=0, magnitude=50)
    print(p.return_greatest_parallelogram(rectangle, vertical))

    
