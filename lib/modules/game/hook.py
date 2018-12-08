from lib.modules.physics.ray import Ray



class Hook(Ray):

    def __init__(self, initial_force_vector, mass):
        '''Constructs hook weapon given initial force vector'''
        super().__init__(initial_force_vector, mass)
        
        
    def collides_with(self, rect):
        '''Returns boolean value of whether or not the hook collided with a rect'''
        return super().collides_with(rect)

    def retract(self, retract_force):
        '''Called when hook hooks onto any object hookable'''
        
        
    def update(self, force_vector_list):
        '''Update Hook's Ray'''
        super().update(force_vector_list)
        
