
class Line:
    def __init__(self, slope, point, x_range, y_range):

        # check invariants for slope being a number or infinite
        if slope == 'infinite' or type(slope) == int or type(slope) == float:
            self._slope = slope
        else:
            raise ValueError('Slope must be any real number or string infinite')

        # check invariants for points being type tuple and only numbers
        if isinstance(point, tuple) and len(point) == 2:
            if self.isnumber(point[0]) and self.isnumber(point[1]):
                self._x = point[0]
                self._y = point[1]
            else:
                raise ValueError('Line->Constructor: point should have integer or float values')
        else:
            raise ValueError('Line->Constructor: point should be tuple with only two elements which should be numbers')

        # checks invariants for range
        if self.isnumber(x_range) and self.isnumber(y_range):
            self.range_x = x_range
            self.range_y = y_range
        else:
            raise ValueError('Line->Constructor: ranges should be integer or float values')

    
        
    def isnumber(self, value):
        '''Returns boolean state of value being integer or float'''
        return type(value) == int or type(value) == float

    def is_in_x_range(self, x):
        '''Returns boolean state of value being in range of x'''
        return self.is_in_range(x, self.range_x+self._x, self._x)

    def is_in_y_range(self, y):
        '''Returns boolean state of value being in range of y'''
        return self.is_in_range(y, self.range_y+self._y, self._y)
    
    def is_in_range(self, value, beginning_range, end_range):
        '''Returns boolean value of whether or not point is in range or not'''
        if value == None:
            return False
        if value == 'infinite':
            return True

        if beginning_range > end_range:
            return end_range <= value <= beginning_range
        else:
            return beginning_range <= value <= end_range

        
    def y_value(self, x):
        '''Return y value'''
        # if the slope is infinite and the x is the initial x, y values are infinite
        if self._slope == 'infinite' and x == self._x:
            return 'infinite'
        
        # if the slope is infinite but the x is not equal to the initial x, None is returned
        elif self._slope == 'infinite' and (not x == self._x):
            return None

        # if the slope is 0, then the y value is the initial y value
        elif self._slope == 0:
            return self._y

        # if the slope is a real number other than 0, the value if returned using point slope formula
        elif not self._slope == 0:
            return self._slope*(x-self._x)+self._y
        
    def x_value(self, y):
        '''Return x value'''
        # if the slope is 0 and the y value is equal to the y value of the initial point, then the x value does exist
        if self._slope == 0 and y == self._y:
            return 'infinite'

        # if the slope is 0(a horizontal line) and the given y is not equal to the horizontal line, None is returned
        elif self._slope == 0 and not y == self.y_value(self._x):
            return None

        # if the slope is not 0 and not infinite, the point slope formula rearranged is used to return x value
        elif not self._slope == 0 and not self._slope == 'infinite':
            return (y-self._y)/self._slope+self._x

        # if the slope is infinite, return the only x for all y value
        elif self._slope == 'infinite':
            return self._x


        
if __name__ == '__main__':
    '''Tests'''

    # Test exception handling
    incorrect_parameters = [('bla', (12,0), 200, 300), ('infinite', (12)), (123, (12,0,3), 23, 23), ('infinite', ('asdf', 2), -123, 12)]
    
    for parameter in incorrect_parameters:
        try:
            invalid_line = Line(*parameter)
            assert False
        except:
            pass

        
    # test output
    correct_parameters = [{'y_value': 4, 'parameters': (2, (3,4))}, {'y_value': 'infinite', 'parameters': ('infinite', (3,2))}, {'x_value': 'infinite', 'parameters': (0, (2,5))}]
    
    for parameter in correct_parameters:
        try:
            arguments = parameter['parameters']
            line = Line(*arguments)
            if 'y_value' in parameter:
                assert line.y_value(arguments[1][0]) == parameter['y_value']
            if 'x_value' in parameter:
                assert line.x_value(arguments[1][1]) == parameter['x_value']
        except:
            assert False
