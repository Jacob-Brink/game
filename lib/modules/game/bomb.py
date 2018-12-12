from lib.modules.gui.rectangle import Rectangle, Point
from lib.modules.physics.rigid_body import RigidBody
from lib.modules.gui.image import Image
from lib.modules.game.timer import Timer

class Bomb(RigidBody):

    def __init__(self, initial_velocity, bomb_type):
        '''Models an exploding bomb'''
        # set rigid body
        self._width = 20
        self._mass = 90
        super().__init__(Rectangle(initial_velocity.return_start_position(), Point(self._width, self._width)), self._mass)
        super().set_velocity(initial_velocity)

        # exploded
        self._exploded = False
        self._explosion_radius = 2000
        self._bomb_type = bomb_type
        
        # color flash stuff
        self._color = (0, 0, 0)
        self._color_increase = True
        self._color_step = 30
        
        # bomb fuse
        self._fuse_timer = Timer()
        self._fuse_timer.restart()
        self._fuse_limit = 3

        # explosion duration timer
        self._explosion_timer = Timer()
        self._explosion_duration = 2

    def get_type(self):
        '''Returns type of bomb'''
        return self._bomb_type
        
    def color_transition(self, color_value):
        '''Returns next color in color transition'''
        if self._color_increase:
            if color_value <= 255-self._color_step:
                color_value += self._color_step
            elif color_value > 255-self._color_step:
                self._color_increase = False
        else:
            if color_value >= self._color_step:
                color_value -= self._color_step
            elif color_value < self._color_step:
                self._color_increase = True

        return color_value
        
    def update(self, delta_time):
        '''Change color for flashing effect'''

        if not self._exploded:

            # make fuse flash blink faster and faster as time progresses
            self._color_step = self._fuse_timer.read()*20
            
            # change color
            self._color = (self.color_transition(self._color[0]), 255 - self._color[0], self._color[2])
            
            # explode after fuse goes out
            if self._fuse_timer.read() > self._fuse_limit:
                self.explode()
            
        elif self._bomb_type == 'implosion':
            self._color = (0,10,200)
            
        elif self._bomb_type == 'explosion':
            self._color = (195,0,198)

        # update rigid body
        super().update(delta_time)

        
    def explode(self):
        '''Explodes!'''
        self._explosion_timer.restart()
        self._exploded = True
        
    def finished_exploding(self):
        '''Returns whether or not bomb's explosion is done'''
        return self._explosion_timer.read() >= self._explosion_duration
        
    def exploded(self):
        '''Returns whether or not it exploded'''
        return self._exploded

    def get_radius(self):
        '''Returns radius of explosion'''
        return self._explosion_radius

    def get_color(self):
        '''Return flashing color'''
        return self._color
