from lib.modules.gui.rectangle import Rectangle

RECTANGLE_COLOR = (0,0,0)


class Platform(Rectangle):
  
    def __init__(self, rectangle, color):
        '''Constructs platform given rectangle and color'''

        if isinstance(rectangle, Rectangle):
            super().__init__((rectangle.get_top_left().return_tuple()), rectangle.get_size().return_tuple())
            self._color = color
        else:
            raise TypeError('Platform->Constructor: rectangle must be of type Rectangle. Not pygame rectangle')

    def change_placeability(self, can_place_bool):
        '''Sets placeability to can place bool'''
        self._placeable = can_place_bool

    def get_placeability(self):
        '''Return placeability'''
        return self._placeable
        
    def get_color(self):
        '''Returns color'''
        return self._color
        
    def change_color(self, new_color):
        '''Sets color to new color'''
        self._color = new_color
