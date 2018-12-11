from enum import Enum
from lib.modules.gui.rectangle import Point

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

    def circle_rect(self, center_point, radius, rect):
        '''Given radius and rectangle, determine collision'''
        return self.one_dimensional_collision((center_point.x()-radius, center_point.x()+radius), (rect.get_x(), rect.get_x()+rect.get_w())) and self.one_dimensional_collision((center_point.y()-radius, center_point.y()+radius), (rect.get_y(), rect.get_y()+rect.get_y()))
    
    def rect_rect(self, rect1, rect2):
        '''Return boolean value of any intersection between two given pygame rects'''
        return rect1.get_x() <= rect2.get_x()+rect2.get_w() and rect1.get_x()+rect1.get_w() >= rect2.get_x() and rect1.get_y() <= rect2.get_y()+rect2.get_h() and rect1.get_y()+rect1.get_h() >= rect2.get_y()
