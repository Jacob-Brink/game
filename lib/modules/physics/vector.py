import math

class Vector:

    def __init__(self, direction, magnitude):
        self._direction = direction
        self._magnitude = magnitude

    def return_x_component(self):
        return math.cos(math.radians(self._direction))*self._magnitude

    def return_y_component(self):
        return math.sin(math.radians(self._direction))*self._magnitude

    def return_direction(self):
        return self._direction

    def return_magnitude(self):
        return self._magnitude

    #modify replaces value
    def modify_magnitude(self, new_magnitude):
        self._magnitude = new_magnitude

    def modify_direction(self, new_direction):
        self._direction = new_direction

    #alter functions change values by addition
    def alter_magnitude(self, new_magnitude):
        self._magnitude += new_magnitude

    def alter_direction(self, new_direction):
        self._direction += new_direction



    def __str__(self):

        return 'Direction: ' + str(self.return_direction()) + ', Magnitude: ' + str(self.return_magnitude())
        
    def __mul__(self, other):

        #scalar multiplication
        if isinstance(other, int) or isinstance(other, float):
        
            return Vector(self.return_direction(), other * self.return_magnitude())

            
    #add overload
    def __add__(self, other):

        x_component = self.return_x_component() + other.return_x_component()
        y_component = self.return_y_component() + other.return_y_component()

        return Vector( math.degrees(math.atan2(y_component, x_component)), math.sqrt((x_component)**2 + (y_component)**2) )


    
if __name__ == '__main__':
    #initialize vector v
    v = Vector(90, 100)

    #test component returning functions
    assert(round(v.return_x_component()) == 0)
    assert(round(v.return_y_component()) == 100)

    #test direction and magnitude returning functions
    assert(round(v.return_direction()) == 90)
    assert(round(v.return_magnitude()) == 100)

    #test modify_magnitude function
    v.modify_magnitude(1000)
    assert(round(v.return_magnitude()) == 1000)

    #test modify_direction function
    v.modify_direction(180)
    assert(round(v.return_direction()) == 180)

    #test alter function
    v.alter_magnitude(1000)
    assert(round(v.return_magnitude()) == 2000)

    v.alter_direction(-1)
    assert(round(v.return_direction()) == 179)

    #test overloading
    v1 = Vector(45, 100)
    v2 = Vector(180+45, 100)

    v3 = v1+v2
    
    assert(round(v3.return_magnitude()) == 0)

    #test scalar

    v1 = Vector(45, 100)
    v = v1 * 2

    assert(round(v.return_magnitude()) == 200)
    
    print('Vector Tests passed')
    
