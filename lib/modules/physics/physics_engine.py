from lib.modules.physics.vector import Vector
from lib.modules.physics.line import Line

import math
import pygame

class Physics:

    def __init__(self):
        pass
    def _check_collision(self, rect1, rect2):
        '''Return True if collision occurs between two objects'''
        return rect1.colliderect(rect2)

    def _one_dimensional_collision(self, point, line, line_begin, line_end):
        '''Return collision of point and one dimensional line'''
        # if only one point(no infinite slope), there is only one intersection possible
        return line.is_in_range(point, line_begin, line_end)

    def _check_rect_collision(self, rigid_body, platform):
        '''Checks collision between rigid_body and platform with velocity and position'''
        # rigid body
        past_rect = rigid_body.return_past_rect()
        new_rect = rigid_body.return_rect()
        # determine range parameters for intersection searches
        x_range = new_rect.x-past_rect.x
        y_range = new_rect.y-past_rect.y
        
        # platform
        past_velocity_slope = rigid_body.return_past_velocity().return_slope()

        # create function reducing parameters to only changing
        def check_line_collision(point):
            return self._line_collides_rect(past_velocity_slope, point, platform, (x_range, y_range))
        
        # Check if lines drawn by either point from moving rectangle ever intersect the platform
        return check_line_collision(past_rect.topleft) or check_line_collision(past_rect.topright) or check_line_collision(past_rect.bottomleft) or check_line_collision(past_rect.bottomright)
            

    
    def _line_collides_rect(self, slope, point_coordinate, rect, range_xy):
        '''Returns boolean value of whether or not a line collided with a rectangle'''
        '''This is used to make sure that players cannot fly through objects if the position from one tick to the next creates a line of motion intersecting the platform'''

        
        # range for intersection search
        x_range = range_xy[0]
        y_range = range_xy[1]

        # create line object with slope, x,y coordinate and ranges
        line = Line(slope, point_coordinate, x_range, y_range)
               

        y_values = line.y_value(rect.left), line.y_value(rect.right)
        x_values = line.x_value(rect.top), line.x_value(rect.bottom)

        # check for collision between left and right side of rectangle
        # uses one dimensional collision for checking if y coordinate of line at rectangle side's x position collides
        # Also ensures that the point is in range
        for y_value in y_values:
            if (self._one_dimensional_collision(y_value, line, rect.bottom, rect.top) and line.is_in_y_range(y_value)):
                return True
        
        # check for collision between top and bottom side of rectangle
        for x_value in x_values:
            if (self._one_dimensional_collision(x_value, line, rect.left, rect.right) and line.is_in_x_range(x_value)):
                return True

        return False

    
    def _return_x_collision(self, vector, y_line, rect):
        '''Returns x position of where vector and y_line intersect'''
        line = Line(vector.return_slope(), (rect.topleft))
        return line.x_value(y_line)
        
    def _return_y_collision(self, vector, x_line, rect):
        '''Returns y posiiton of where vector and x_line intersect'''
        line = Line(vector.return_slope(), (rect.topleft))
        return line.y_value(x_line)

        
    def reposition(self, rigid_body, immovable_rect_list, delta_time):
        '''Return new rectangle based on how two rectangles collided'''
        MARGIN_PIXEL = 20
        for platform in immovable_rect_list:

            # if a collision occurs, figure out how what side the rigid_body collided
            if self._check_rect_collision(rigid_body, platform) or rigid_body.return_rect().colliderect(platform):
                past_rect = rigid_body.return_past_rect()
                rect = rigid_body.return_rect()
                body_velocity = rigid_body.return_velocity_vector()
                body_direction = body_velocity.return_direction()

                
                # on top
                if past_rect.y+past_rect.h <= platform.y:
                    print('correcting top')
                    rigid_body.set_rect(pygame.Rect(rect.x, platform.y-rect.h-MARGIN_PIXEL, rect.w, rect.h))

                # on bottom
                if past_rect.y >= platform.y + platform.h:
                    print('correcting bottom')
                    rigid_body.set_rect(pygame.Rect(rect.x, platform.y+platform.h+MARGIN_PIXEL, rect.w, rect.h))

                # on left
                if past_rect.x >= platform.x + platform.w:
                    print('correcting to left')
                    rigid_body.set_rect(pygame.Rect(platform.x+platform.w+MARGIN_PIXEL, rect.y, rect.w, rect.h))
    
                # on right
                if past_rect.x+past_rect.w <= platform.x:
                    print('correcting to right')
                    rigid_body.set_rect(pygame.Rect(platform.x-rect.w-MARGIN_PIXEL, rect.y, rect.w, rect.h))

                    # give normal force to object
                    
                rigid_body.set_velocity(body_velocity*0)
            
        #return new_rect
