

class Collision:
    '''Class for organizing collision functions'''
    def __init__(self):
        pass

    def vector_rect(self, vector, rect):
        '''Return boolean value of any intersection between vector and rect'''
        return self._line_collides_rect(vector.return_slope(), vector.return_start_position(), rect, (vector.return_x_component(), vector.return_y_component()))

    def rect_rect(self, rect1, rect2):
        '''Return boolean value of any intersection between two given pygame rects'''
        return rect1.get_x() <= rect2.get_x()+rect2.get_w() and rect1.get_x()+rect1.get_w() >= rect2.get_x() and rect1.get_y() <= rect2.get_y()+rect2.get_w() and rect1.get_y()+rect1.get_h() >= rect2.get_y()
        
    def _line_collides_rect(self, slope, point_coordinate, rect, range_xy):
        '''Returns boolean value of whether or not a line collided with a rectangle'''
        '''This is used to make sure that players cannot fly through objects if the position from one tick to the next creates a line of motion intersecting the platform'''

        #FIX OR DELETE
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
