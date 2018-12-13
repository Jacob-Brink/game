from lib.modules.gui.rectangle import Rectangle

RECTANGLE_COLOR = (0,0,0)
HIGHLIGHT_COLOR = (0, 0, 255)
UNFINISHED_COLOR = (0,255,0)
WRONG_COLOR = (100, 100, 100)

class Platform(Rectangle):
  
    def __init__(self, rectangle):
        '''Constructs platform given rectangle and color'''
        self._placeable = True
        self._finished = True
        self._highlighted = False
        self._set_color()
        
        
        if isinstance(rectangle, Rectangle):
            super().__init__((rectangle.get_top_left().return_tuple()), rectangle.get_size().return_tuple())

            
        else:
            raise TypeError('Platform->Constructor: rectangle must be of type Rectangle. Not pygame rectangle')

    def _set_color(self):
        '''Set color based from attributes'''
        if not self._placeable:
            self._color = WRONG_COLOR
            
        elif not self._finished:
            self._color = UNFINISHED_COLOR

        elif self._highlighted:
            self._color = HIGHLIGHT_COLOR

        else:
            self._color = RECTANGLE_COLOR
        
    def copy(self):
        '''Returns a copy'''
        return Platform(super().copy())
            
    def change_placeability(self, can_place_bool):
        '''Sets placeability to can place bool'''
        self._placeable = can_place_bool
        self._set_color()
        
    def change_highlight(self, highlighted):
        '''Sets highlight bool'''
        self._highlighted = highlighted
        self._set_color()
        
    def change_finished(self, finished):
        '''Sets finished bool'''
        self._finished = finished
        self._set_color()
        
    def get_placeability(self):
        '''Return placeability'''
        return self._placeable
        
    def get_color(self):
        '''Returns color'''
        return self._color
    
