from lib.modules.gui.rectangle import Rectangle
from lib.modules.physics.rigid_body import RigidBody

class Bomb(RigidBody):

    def __init__(self, initial_velocity, mass, explosion_radius):
        '''Models an exploding bomb'''
        self._width = 20
        self._mass = 10

        self._exploded = False
        self._explosion_radius = explosion_radius

        super().__init__(Rectangle(initial_velocity.get_start_position().return_tuple(), Point(self._width, self._width)), self._mass)

        super().set_velocity(initial_velocity)

    def explode(self):
        '''Explodes!'''
        self._exploded = True

    def update(self):
        '''Updates rigid_body'''
        super().update()

        if super().get_collided():

            self.explode()
            
