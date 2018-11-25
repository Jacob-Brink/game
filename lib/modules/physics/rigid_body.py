from vector import Vector

from pygame import Rect
import math

class RigidBody:

    def __init__(self, rect, mass):

        self._rect = rect
        self._velocity = Vector(0, 0)
        self._mass = mass
        self._acceleration = Vector(0, 0)
        self._forces = []
        
        
    #must be applied before update is called in game loop
    def apply_force(self, force_vector):
        self._forces.append(force_vector)

    #to be called every tick
    def update(self):

        self._acceleration = Vector(0,0)
        
        for force in self._forces:

            self._acceleration += force * (1/self._mass)
            

        self._velocity += self._acceleration

        self._rect = self._rect.move(self._velocity.return_x_component(), self._velocity.return_y_component())
        
        self._forces = []
    
    def return_rect(self):
        
        return self._rect
        
    
    
if __name__ == '__main__':

    r = RigidBody(1,2,3,4, 1)

    #test apply_forces
    force_list = [[180, 100], [0, 100], [90,100]]
    [r.apply_force(Vector(force[0], force[1])) for force in force_list]
    r.update()
    assert(round(r._velocity.return_x_component()) == 0)
    assert(round(r._velocity.return_y_component()) == 100)
