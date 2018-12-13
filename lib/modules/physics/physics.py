from enum import Enum
from lib.modules.gui.rectangle import *
from lib.modules.physics.line import Line

class PlatformStatus(Enum):
    on_top = 1
    on_left = 2
    on_right = 3
    on_bottom = 4
    alone = 5

class Collision:
    '''Class for organizing collision functions'''
    def __init__(self):
        pass
    
    def return_collision_line_x(self, x_value, rect, platform, platform_value):
        '''If value is infinite or value is none return appropriate boolean value'''
        if x_value == 'infinite':
            return True
        
        elif x_value == None:
            return False
        
        else:
            rect.set_center(Point(x_value, platform_value))
            if self.rect_rect(rect, platform):
                return True

    def return_collision_line_y(self, y_value, rect, platform, platform_value):
        '''If value is infinite or value is none return appropriate boolean value'''
        if y_value == 'infinite':
            return True
        
        elif y_value == None:
            return False
        
        else:
            rect.set_center(Point(platform_value, y_value))
            if self.rect_rect(rect, platform):
                return True

    
    def vector_rect(self, vector, rect):
        '''Return boolean value of any intersection between vector and rect'''
        return self._line_collides_rect(vector.return_slope(), vector.return_start_position(), rect, (vector.return_x_component(), vector.return_y_component()))

    def one_dimensional_collision(self, length_point1, length_point2):
        '''Return true if lengths overlap'''
        return length_point1[0] <= length_point2[0] + length_point2[1] and length_point1[0]+length_point1[1] >= length_point2[0]

    def circle_rect(self, center_point, radius, rect):
        '''Given radius and rectangle, determine collision'''
        return self.one_dimensional_collision((center_point.x()-radius, center_point.x()+radius), (rect.get_x(), rect.get_x()+rect.get_w())) and self.one_dimensional_collision((center_point.y()-radius, center_point.y()+radius), (rect.get_y(), rect.get_y()+rect.get_y()))

    def rect_rect(self, rect1, rect2):
        '''Returns boolean value of whether or not two rectangles collide'''
        return rect1.collides_with(rect2)

    def rigid_body_and_platform(self, rigid_body, platform):
        '''Return boolean value of any intersection between two given pygame rects'''

        # if a simple overlap occurs, exit and return True
        if self.rect_rect(rigid_body.return_rect(), platform):
            return True
        
        # make a big box containing the initial and final position of rigid body and motion between tick
        general_collision_area = rigid_body.return_past_rect()+rigid_body.return_rect()

        # only if the platform is in the general collision box does specific collision get detected
        if self.rect_rect(general_collision_area, platform):
            
            
            # if no simple overlap occurs and yet the platform is in the general collision box, do something complicated that I don't understand lol
            # my main idea was to have a line of motion drawn through past and present rectangle and see if any collisions occurred around the platforms
            r_velocity = rigid_body.return_past_velocity()
            r_rect = rigid_body.return_past_rect()
            r_center = r_rect.get_center()
            
            # find the line of motion created by the velocity vector through the centers of the past and future rigid body rectangle
            motion_path_line_thru_center = Line(r_velocity.return_slope(), r_center, r_velocity.return_x_component(), r_velocity.return_y_component())
            
            # check for collision along line
            platform_top = platform.get_top()
            platform_bottom = platform.get_bottom()
            platform_left = platform.get_left()
            platform_right = platform.get_right()
            
            # create base rectangle with same size as rigid body and arbitrary position
            r = Rectangle(Point(0,0), Point(r_rect.get_w(), r_rect.get_h()))
            
            if motion_path_line_thru_center.is_in_y_range(platform_top):
                r_x = motion_path_line_thru_center.x_value(platform_top)         

                # check collision where center is on platform top
                if self.return_collision_line_x(r_x, r_rect, platform, platform_top):
                    return True
                         
            if motion_path_line_thru_center.is_in_y_range(platform_bottom):
                r_x = motion_path_line_thru_center.x_value(platform_bottom)

                # check collision where center in on platform bottom y
                if self.return_collision_line_x(r_x, r_rect, platform, platform_bottom):
                    return True
                
            if motion_path_line_thru_center.is_in_x_range(platform_left):
                r_y = motion_path_line_thru_center.y_value(platform_left)

                # check collision where center is on platform left x
                if self.return_collision_line_y(r_y, r_rect, platform, platform_left):
                    return True
                
            if motion_path_line_thru_center.is_in_x_range(platform_right):
                r_y = motion_path_line_thru_center.y_value(platform_right)

                # check collision where center is on platform right x
                if self.return_collision_line_y(r_y, r_rect, platform, platform_right):
                    return True
                
        return False

        
        

