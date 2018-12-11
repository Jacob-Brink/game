from lib.modules.gui.rectangle import Rectangle

class Platform(Rectangle):
  
    def __init__(self, rectangle, color):
        '''Constructs platform given rectangle and color'''

        if isinstance(rectangle, Rectangle):
            super().__init__((rectangle.get_top_left().return_tuple()), rectangle.get_size().return_tuple())
            self._color = color
        else:
            raise TypeError('Platform->Constructor: rectangle must be of type Rectangle. Not pygame rectangle')

    def get_color(self):
        '''Returns color'''
        return self._color
        
    def change_color(self, new_color):
        '''Sets color to new color'''
        self._color = new_color
