#Handle different import methods for testing and gaming
if __name__ == '__main__':

    from vector import Vector

else:

    from lib.modules.physics.vector import Vector


import pygame
import math

class RigidBody:

    def __init__(self, rect, mass):
        '''Constructs a new RigidBody object with given pygame.Rect rectangle and integer mass'''
        self._rect = rect
        self._past_rect = self._rect
        
        self._velocity = Vector(0.0, 0.0)
        self._past_velocity = self._velocity
        self._mass = mass
        self._acceleration = Vector(0.0, 0.0)
        self._forces = []

    def apply_force(self, force_vector):
        '''Applies an instantaneous force to the RigidBody object. Multiple forces can be applied over a game loop cycle, but forces will disappear after the cycle.'''
        self._forces.append(force_vector)

    def return_past_velocity(self):
        '''Return velocity vector of last tick'''
        return self._past_velocity
        
    def return_velocity_vector(self):
        '''Return the velocity vector'''
        return self._velocity
    
    def set_rect(self, rect):
        '''Sets rectangle to given rect'''
        self._rect = rect

    def set_velocity(self, velocity):
        self._velocity = velocity
        
    def update(self):
        '''Updates RigidBody object to translate force into acceleration and acceleration into new velocity.
        To be called after physics repositioning'''
        self._acceleration = Vector(0,0)

        for force in self._forces:
            self._acceleration = self._acceleration + force * (1/self._mass)

        # velocity and past velocity are set
        self._past_velocity = self._velocity    
        self._velocity += self._acceleration

        # set past and present rectangle values
        self._past_rect = self._rect
        self._rect = self._rect.move(self._velocity.return_x_component(), self._velocity.return_y_component())

        self._forces = []

    def return_past_rect(self):
        '''Returns rect from last tick'''
        return self._past_rect
        
    def return_rect(self):
        '''Returns rectangle of type pygame.Rect'''
        return self._rect

    def return_mass(self):
        '''Returns mass'''
        return self._mass

if __name__ == '__main__':
    '''
    Test RigidBody class with force list and mass of 1 for simplicity
    '''

    r = RigidBody(pygame.Rect(1,2,3,4), 1)

    #test apply_forces
    force_list = [[180, 100], [0, 100], [90,100]]
    [r.apply_force(Vector(force[0], force[1])) for force in force_list]
    r.update()
    assert(round(r._velocity.return_x_component()) == 0)
    assert(round(r._velocity.return_y_component()) == 100)

    print('\nAll Tests Have Passed')
