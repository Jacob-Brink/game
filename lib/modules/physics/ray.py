from lib.modules.physics.physics import Collision

class Ray(Collision):
    '''Represents a physical object as a ray. E.g: Hooks or bullets'''
    def __init__(self, vector, mass):
        '''From given force vector for ray, construct Ray object'''
        self._force_vector = vector
        if mass <= 0:
            raise ValueError('Ray->Constructor: mass must be a positive nonzero integer or float')
        self._mass = mass
        self._velocity_vector = self._force_vector*(1/self._mass)
        
        # construct Base class thingy
        super().__init__()

    def _return_acceleration_vector(self, force_vector):
        '''Given force vector, return acceleration vector'''
        return force_vector*(1/self._mass)
        
    def collides_with(self, other):
        '''Returns boolean value of colliding with other object or not'''
        return super().vector_rect(self._velocity_vector, other)
        
    def update(self, force_vector_list):
        '''With given list of force vectors, adjust current velocity and force vectors'''
        for force_vector in force_vector_list:
            self._velocity_vector += self._return_acceleration_vector(force_vector)

    def return_velocity(self):
        '''Returns velocity vector'''
        return self._velocity_vector
