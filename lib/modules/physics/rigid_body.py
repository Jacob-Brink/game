from lib.modules.physics.vector import Vector
from lib.modules.physics.physics import Collision, PlatformStatus
from lib.modules.gui.rectangle import *

import pygame
import math


class RigidBody():
    def __init__(self, rect, mass):
        '''Constructs a new RigidBody object with given pygame.Rect rectangle and integer mass'''
        
        # if given pygame.Rect type convert to floatable homemade rectangle object
        if isinstance(rect, pygame.Rect):
            raise ValueError('RigidBody->Constructor: rectangle must be of type Rectangle not pygame.Rect')
        self._rect = rect
        self._past_rect = self._rect.copy()
        
        self._platform_status = {PlatformStatus.on_top: False, PlatformStatus.on_left: False, PlatformStatus.on_right: False, PlatformStatus.on_bottom: False, PlatformStatus.alone:True}
        
        self._velocity = Vector(self._rect.get_center(), direction=0, magnitude=0)
        self._past_velocity = self._velocity
        self._mass = mass
        self._acceleration = Vector(self._rect.get_center(), direction=0, magnitude=0)
        self._forces = []
        self._collided = False

        self._max_velocity_magnitude = 10
        
        
    def set_collided(self, collided):
        '''Sets value to collided'''
        self._collided = collided

    def get_collided(self):
        '''Returns collided bool'''
        return self._collided
        
    def change_platform_status(self, keyword, boolean):
        '''For knowing whether on a platform or not, other places can call this to set platform status'''
        self._platform_status[keyword] = boolean

    def reset_platform_status(self):
        '''Resets values to False'''
        for key in self._platform_status:
            self._platform_status[key] = False
            
    def get_platform_status(self, key):
        '''Given key, will return boolean value'''
        return self._platform_status[key]
        
    def apply_force(self, force_vector):
        '''Applies an instantaneous force to the RigidBody object. Multiple forces can be applied over a game loop cycle, but forces will disappear after the cycle.'''
        if isinstance(force_vector, Vector):
            self._forces.append(force_vector)
        else:
            raise ValueError('RigidBody->ApplyForce: Requires argument to be vector type')

    def return_net_force(self):
        '''Returns net force'''
        net_force = Vector(self._rect.get_center(), direction=0, magnitude=0)
        for force in self._forces:
            net_force = net_force + force
        return net_force
        
    def return_past_velocity(self):
        '''Return velocity vector of last tick'''
        return self._past_velocity
    
    def return_velocity_vector(self):
        '''Return the velocity vector'''
        return self._velocity
    
    def set_rect(self, rect):
        '''Sets rectangle to given rect'''
        if isinstance(rect, pygame.Rect):
            raise ValueError('rectangle must be of type Rectangle, not pygame.Rectangle')
        self._rect = rect

    def limit_velocity(self):
        '''Limits velocity based on max velocity magnitude'''
        # restrict upper bound
        if self._velocity.return_magnitude() > self._max_velocity_magnitude:
            self._velocity = Vector(self._velocity.return_start_position(), direction=self._velocity.return_direction(), magnitude=self._max_velocity_magnitude)
        # restrict lower bound
        elif self._velocity.return_magnitude() < -self._max_velocity_magnitude:
            self._velocity = Vector(self._velocity.return_start_position(), direction=self._velocity.return_direction(), magnitude=-self._max_velocity_magnitude)
            
    def set_velocity(self, new_velocity):
        '''Sets the velocity to new velocity'''
        self._velocity = new_velocity
        
    def add_velocity(self, velocity):
        '''Set velocity to given velocity'''
        self._velocity += velocity

    def remove_unecessary_velocity(self):
        '''Given platform status and velocity, remove any components that cause collision'''

        # ensure no movement occurs into blocks
        p_status = self.get_platform_status
        v = self._velocity
        v_y = self._velocity.return_y_component()
        v_x = self._velocity.return_x_component()

        
        # if on top side and velocity goes down
        if p_status(PlatformStatus.on_top) and v_y > 0:
            v.change_y_component(0)

        # if on right side and velocity goes left
        if p_status(PlatformStatus.on_right) and v_x < 0:
            v.change_x_component(0)

        # if on left side and velocity goes right
        if p_status(PlatformStatus.on_left) and v_x > 0:
            v.change_x_component(0)

        # if on bottom side and velocity goes up
        if p_status(PlatformStatus.on_bottom) and v_y < 0:
            v.change_y_component(0)

            
    def update(self, delta_time):
        '''Updates RigidBody object to translate force into acceleration and acceleration into new velocity. To be called after physics repositioning'''

        self._acceleration = Vector(self._rect.get_center(), direction=self._velocity.return_direction(), magnitude=0)*delta_time

        for force in self._forces:
            self._acceleration += force * (1/self._mass)
    
        # velocity and past velocity are set
        self._past_velocity = self._velocity
        print(delta_time, 'delta time')
        self._velocity = (self._acceleration + self._velocity)
        
        self._past_rect = self._rect.copy()
        
        self.remove_unecessary_velocity()
        
        # changes rectangle from last velocity
        delta_point = Point(self._velocity.return_x_component(), self._velocity.return_y_component())

        self._rect.move(delta_point)


        self._forces = []

        self.limit_velocity()

    def return_past_rect(self):
        '''Returns rect that is distinguishably different than current rect'''
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
