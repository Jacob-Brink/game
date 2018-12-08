from lib.modules.physics.vector import Vector
from lib.modules.physics.line import Line
import math


class Parallelogram:
    def __init__(self, vector1, vector2):
        '''From two rectangles, create a parallelogram with greatest area'''

        # check if vector positions are same
        if not vector1.return_start_position() == vector2.return_start_position():
            raise ValueError('Given vectors must represent adjacent sides of a parallelogram. They must have same starting position')
        
        # find opposite points
        self._opposite_points = vector1.return_start_position(), Vector(vector2.return_end_position(), direction=vector1.return_direction(),magnitude=vector1.return_magnitude()).return_end_position()

        # calculate 4 points
        self._points = [self._opposite_points[0], vector1.return_end_position(), vector2.return_end_position(), self._opposite_points[1]]

        # calculate base and height
        self._base = vector1.return_magnitude()
        self._height = math.sqrt(vector2.return_magnitude()**2+(vector2.project_on(vector1).return_magnitude())**2)
        
        # calculate center
        point1 = self._opposite_points[0]
        point2 = self._opposite_points[1]
        self._center = (point1[0]+point2[0])/2, (point1[1]+point2[1])/2

    def __str__(self):
        '''Returns string for pretty print'''
        string_ = ''
        for index in range(0, len(self._points)):
            string_ += 'Point ' + str(index) + str(self._points[index])
        return string_ + '\n'
    
    def return_center(self):
        '''Returns center of parallelogram'''
        return self._center
    
    def return_area(self):
        '''Returns area'''
        return self._base*self._height
        
    def return_points(self):
        '''Returns list of four points (tuple)'''
        return self._points

if __name__ == '__main__':
    '''Testing'''


    
    vector1 = Vector((0,0), direction=90, magnitude=10)
    vector2 = Vector((0,0), direction=0, magnitude=5)

    print(Parallelogram(vector1, vector2).return_points())
    print(Parallelogram(vector1, vector2).return_area())
