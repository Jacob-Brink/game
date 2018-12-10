import math
from lib.modules.gui.rectangle import Point

class Vector:
    '''Vector class used for velocity, force, and acceleration in physics stuff'''

    def __init__(self, position_point, **keywords):
        '''Constructs a new vector given direction (degrees :0 for facing right) and magnitude (any num type)'''

        if not isinstance(position_point, Point):
            raise ValueError('Vector->Constructor requires position to be of type Point')
        self._position_point = position_point
        
        # constructed with direction and magnitude
        if 'direction' in keywords and 'magnitude' in keywords:
            self._direction = math.radians(keywords['direction'])
            self._magnitude = keywords['magnitude']

            self._x_component = math.cos(self._direction)*self._magnitude
            self._y_component = math.sin(self._direction)*self._magnitude
            
        # constructed with components
        elif 'x_component' in keywords and 'y_component' in keywords:
            self._x_component = keywords['x_component']
            self._y_component = keywords['y_component']
            self._direction = math.atan2(self._y_component, self._x_component)
            self._magnitude = math.sqrt((self._x_component)**2+(self._y_component)**2)
        else:
            raise TypeError('Parameters must include position point as first arg, then either direction and magnitude or x_component and y_component')

    def return_slope(self):
        '''Returns slope of vector'''
        if self.return_x_component() == 0:
            return 'infinite'
        return self.return_y_component() / self.return_x_component()

    def return_end_position(self):
        '''Returns end position'''
        return Point(self._position_point.x()+self._x_component, self._position_point.y()+self._y_component)
                
    def return_start_position(self):
        '''Returns start position'''
        return self._position_point
    
    def return_x_component(self):
        '''Returns the x component of the vector via Trig'''
        return self._x_component

    def return_y_component(self):
        '''Returns the y component of the vector via Trig'''
        return self._y_component

    def return_direction(self):
        '''Returns the direction (degrees)'''
        return math.degrees(self._direction)

    def return_magnitude(self):
        '''Returns the magnitude'''
        return self._magnitude

    def return_unit_vector(self):
        '''Returns unit vector'''
        return Vector(self._position_point, self._x_component / self._magnitude, self._y_component / self._magnitude)

    def project_on(self, axis_vector):
        '''Return vector projected on given vector'''
        return Vector(axis_vector.return_start_position(), direction=axis_vector.return_direction(), magnitude=(self._x_component*axis_vector.return_x_component()+ self._y_component*axis_vector.return_y_component())/axis_vector.return_magnitude())
    
    def dot_product(self, axis_vector):
        '''Returns vector projected on axis_vector'''
        return Vector(axis_vector.return_start_position(), direction=axis_vector.return_direction(), magnitude=(self._x_component*axis_vector.return_x_component()+ self._y_component*axis_vector.return_y_component()))
    
    def __str__(self, rounding=True):
        '''Pretty print enabled for class'''
        return 'Direction: ' + str(round(self.return_direction())) + ', Magnitude: ' + str(round(self.return_magnitude())) + '<' + str(round(self.return_x_component())) + ',' + str(round(self.return_y_component()))+'>'

    def __mul__(self, other):
        '''Allows for scalar and vector multiplication'''
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self._position_point, direction=self.return_direction(), magnitude=other * self.return_magnitude())
    
    def __add__(self, other):
        '''Addition overloading of vectors when both terms are vectors'''

        x = self.return_x_component() + other.return_x_component()
        y = self.return_y_component() + other.return_y_component()

        return Vector( self._position_point, x_component=x, y_component=y)

    def __sub__(self, other):
        '''Subtraction overloading of vectors when both terms are vectors'''
        x = self.return_x_component() - other.return_x_component()
        y = self.return_y_component() - other.return_y_component()

        return Vector( self._position_point, x_component=x, y_component=y)


if __name__ == '__main__':
    '''Test each part of the vector class'''
    import random

    
    vector = Vector((0,0), direction=123, magnitude=123)
    test_string = 'asdfasdf'
    random_magnitude = random.randint(-100, 100)
    random_direction = random.randint(-180, 180)
    random_x = random.randint(-100, 100)
    random_y = random.randint(-100, 100)

    random_value = random.randint(-100, 100)

    # the reason the arguments are in string format is that there is no other way to store parameters with key value input(e.g. direction=number) without errors
    incorrect_parameters = [((12,2), {'direction':random_direction, 'x_component':random_x}),({'direction':random_direction, 'magnitude':random_magnitude}),((12,3)), ((test_string, test_string), {'direction':12, 'magnitude':14}), ((12,12), 12,3,4), (), (), ()]

    
    # ensure bad values and parameters raise exceptions
    for parameters in incorrect_parameters:
        try:
            invalid_vector = Vector(*exec(parameters, locals(), globals()))
            assert False
        except:
            pass

    # test correct parameters and basic functions
    correct_parameters = [{'return_x_component': 3, 'return_y_component': 4, 'return_magnitude': 5, 'return_direction': math.degrees(math.atan2(4,3)), 'parameters': ((random_x, random_y), {'x_component':3, 'y_component':4})}, {'return_x_component': 6, 'return_y_component': 8, 'return_magnitude': 10, 'return_direction': math.degrees(math.atan2(8,6)), 'parameters': ((random_x, random_y), {'x_component':6, 'y_component':8})}, {'return_x_component': 4, 'return_y_component': 3, 'return_magnitude': 5, 'return_direction': 37, 'parameters': ((random_x, random_y), {'direction':37, 'magnitude':5})}]

        
    for parameters in correct_parameters:
        valid_vector = Vector(parameters['parameters'][0], **parameters['parameters'][1])
        
        assert round(parameters['return_x_component']) == round(valid_vector.return_x_component())
        assert round(parameters['return_y_component'])== round(valid_vector.return_y_component())

        assert round(parameters['return_magnitude']) == round(valid_vector.return_magnitude())
        assert round(parameters['return_direction']) == round(valid_vector.return_direction())

    # test dot product

    axis_vector = Vector((0,0), direction=0, magnitude=16)
    vector = Vector((0,0), direction=45, magnitude=25)

    projected_vector = vector.dot_product(axis_vector)
    assert projected_vector.return_x_component() == 16*(math.cos(math.radians(45))*25) + 0*(math.sin(math.radians(45))*25)


    print('Vector Tests passed')
