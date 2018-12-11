from enum import Enum

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

    def vector_rect(self, vector, rect):
        '''Return boolean value of any intersection between vector and rect'''
        return self._line_collides_rect(vector.return_slope(), vector.return_start_position(), rect, (vector.return_x_component(), vector.return_y_component()))

    def one_dimensional_collision(self, length_point1, length_point2):
        '''Return true if lengths overlap'''
        return length_point1[0] <= length_point2[0] + length_point2[1] and length_point1[0]+length_point1[1] >= length_point2[0]
    
    def rect_rect(self, rect1, rect2):
        '''Return boolean value of any intersection between two given pygame rects'''
        return rect1.get_x() <= rect2.get_x()+rect2.get_w() and rect1.get_x()+rect1.get_w() >= rect2.get_x() and rect1.get_y() <= rect2.get_y()+rect2.get_h() and rect1.get_y()+rect1.get_h() >= rect2.get_y()
