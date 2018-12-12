from lib.modules.physics.vector import Vector
from lib.modules.physics.line import Line
from lib.modules.gui.rectangle import Rectangle, Point
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
        self._gravity_magnitude = 2
        
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

    def apply_gravity(self, rigid_body):
        '''Applies gravity vector to rigid body'''
        rigid_body.apply_force(Vector(rigid_body.return_rect().get_center(), direction=90, magnitude=self._gravity_magnitude*self._delta_time))

    def reposition(self, rigid_body, platform_list):
        
            for platform in platform_list:

                # if a collision occurs, figure out how what side the rigid_body collided
                if rigid_body.return_rect().collides_with(platform):

                    # reposition rigid_body
                    rigid_body.set_rect(self.return_new_rect_reposition(rigid_body.return_past_rect(), platform))             

                rigid_body.change_platform_status(self.return_side_platform(rigid_body.return_rect(), platform), True)

                # set velocity to 0
                if rigid_body.get_platform_status(PlatformStatus.on_top) or rigid_body.get_platform_status(PlatformStatus.on_bottom):

                    rigid_body.set_velocity(Vector(Point(0,0), x_component=rigid_body.return_velocity_vector().return_x_component(), y_component=0))

                elif rigid_body.get_platform_status(PlatformStatus.on_left) or rigid_body.get_platform_status(PlatformStatus.on_right):

                    rigid_body.set_velocity(Vector(Point(0,0), x_component=0, y_component=rigid_body.return_velocity_vector().return_y_component()))
        

    def update(self, events, player_list, bomb_list, platform_list):
        '''Calculate collisions, reposition from collisions, work with forces, etc'''        

        self._delta_time = events.delta_time()
        
        # updates bomb rigid body
        for bomb in bomb_list:

            bomb.update(self._delta_time)
            self.apply_gravity(bomb)
            
            if bomb.exploded():

                coefficient = 1

                # if the bomb implodes ( or sucks in rigid bodies instead of propelling them ) make the coefficient negative half
                if bomb.get_type() == 'implosion':
                    coefficient = -.5
                
                b_center = bomb.return_rect().get_center()
                b_radius = bomb.get_radius()
                
                for player in player_list:

                    #if self._collision.circle_rect(b_center, b_radius, player.return_rect()):
                    p_center = player.return_rect().get_center()
                    dist_centers = math.sqrt((p_center.x()-b_center.x())**2+(b_center.y()-p_center.y())**2)
                    player.apply_force(Vector(p_center, direction=math.degrees(math.atan2(p_center.y()-b_center.y(),p_center.x()-b_center.x())), magnitude=coefficient*(50*b_radius/(.1+dist_centers))))
                    
                    player.change_health(b_radius/(.1+dist_centers*dist_centers))

                for bomby in bomb_list:
                    
                    #if self._collision.circle_rect(b_center, b_radius, bomby.return_rect()) and bomby is not bomb:
                    if bomby is not bomb:
                        p_center = bomby.return_rect().get_center()
                        dist_centers = math.sqrt((p_center.x()-b_center.x())**2+(b_center.y()-p_center.y())**2)
                        bomby.apply_force(Vector(p_center, direction=math.degrees(math.atan2(p_center.y()-b_center.y(),p_center.x()-b_center.x())), magnitude=coefficient*(60*b_radius/(.1+dist_centers))))

                        
                if bomb.finished_exploding():

                    bomb_list.remove(bomb)

            self.reposition(bomb, platform_list)

            
        for player in player_list:
            
            player.update(events)
            player.reset_platform_status()
            
            self.reposition(player, platform_list)
            
            if not player.get_platform_status(PlatformStatus.on_top):
                self.apply_gravity(player)
            
    
            


        


            

        
if __name__ == '__main__':
    '''Tests'''

    p = Physics()
    rectangle = pygame.Rect(0,0,10, 5)
    vertical = Vector((0,0), direction=0, magnitude=50)
    print(p.return_greatest_parallelogram(rectangle, vertical))

    
