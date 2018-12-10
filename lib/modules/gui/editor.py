if __name__ == '__main__':
    from text import Text
    from events import Event
    from view import View
    from camera import Camera
else:
    from lib.modules.gui.text import Text
    from lib.modules.gui.events import *
    from lib.modules.gui.view import View
    from lib.modules.gui.camera import Camera
    from lib.modules.gui.menu import Menu
    from lib.modules.gui.rectangle import *

from enum import Enum
import pygame

def init():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('The Game')
    pygame.display.flip()

    return screen

# Cursor enum
class Cursor(Enum):
    platform = 1
    eraser = 2
        
    
class Editor(View):

    def __init__(self, screen, level, quit_callback):
        '''Constructs an editor object derived from base class View. The editor object allows for easy creation of new levels.'''

        self._quit_callback = quit_callback
        
        # construct view object that will handle all rendering and blitting stuff
        super().__init__(screen)

        # construct title surface
        self._title = Text('Editor Shortcuts: (w,a,s,d for panning), (1 for rectangle paint brush), (2 for eraser), (left click for painting), (ESC to save and exit)', 32, (255,255,255), 'left', 30)

        self._cursor = Cursor.platform
        self._platforms = []
        self._level = level

        # coin
        self._coins = []

        # start
        self._start = None
        
        # platforms
        self._first_click = False
        self.first_pos = None
        self.second_pos = None
        self._unfinished_rect = None
        
        self.read_level()

    
    def change_cursor(self, new_cursor):
        '''Changes cursor and is given to buttons in the menu'''
        self._cursor = new_cursor
        
    def write_level(self):
        '''Write to level all platforms and items'''
        with open(self._level, 'w') as level_file:
            for platform in self._platforms:
                level_file.write(str(platform)+'\n')

    def read_level(self):
        '''Load level platforms into level editor'''
        with open(self._level) as level_file:
            [self._platforms.append(Rectangle(*[float(string_integer) for string_integer in line.strip().split()])) for line in level_file]

    def erase(self, mouse_pos, current_click):
        '''Given mouse position and a click, erases a rectangle'''

        mouse_display_point = Point(*mouse_pos)
        
        # If eraser collides with rectangle, highlight it
        for platform in self._platforms:
            if platform.collide_point(super().return_display_position(mouse_display_point)):
                #Highlight rectangle
                if current_click == Switch.pushed_down:
                    self._platforms.remove(platform)
        # If clicked, pop it
        
        
    def _return_rect(self, first_pos, second_pos):
        '''Transforms two mouse position points into rectangle.'''

        width = second_pos.x() - first_pos.x()
        height = second_pos.y() - first_pos.y()
        true_rect = Rectangle(first_pos.x(), first_pos.y(), width, height)
        return true_rect

    def draw_platform(self, current_click, mouse_position):
        '''Draws platform with mouse clicks'''
        # Start drawing rectangle
        if current_click == Switch.pushed_down and not self._first_click:

            self._first_click = True
            # get true first position
            self.first_pos = super().return_true_position(Point(*mouse_position))

        # Continue drawing rectangle
        if current_click == Switch.down and self._first_click:

            # get true second position
            self.second_pos = super().return_true_position(Point(*mouse_position))

            self._unfinished_rect = self._return_rect(self.first_pos, self.second_pos)
            

        # End drawing of rectangle on second click event
        if self._first_click == True and current_click == Switch.pushed_up:

            # reset first click so new rectangle can be created
            self._first_click = False

            # get true second position
            self.second_pos = super().return_true_position(Point(*mouse_position))

            # return rectangles with from two true positions
            self._platforms.append(self._return_rect(self.first_pos, self.second_pos))

            # remove temp rectangle
            self._unfinished_rect = None

        
    def _collides_platform(self, rect):
        '''Checks for collisions, returns boolean value'''
        for rectangle in self._platforms:
            if rectangle.colliderect(rect):
                return True
        return False
    
    def handle_keyboard(self, events):
        '''Handle Keyboard events'''

        delta_x = 0
        delta_y = 0
        
        change = 5
        
        pressed = events.keyboard().is_pressed

        if pressed(pygame.K_w) == Switch.down:
            delta_y = -change
        if pressed(pygame.K_s) == Switch.down:
            delta_y = change
        if pressed(pygame.K_a) == Switch.down:
            delta_x = -change
        if pressed(pygame.K_d) == Switch.down:
            delta_x = change

        super().move(delta_x, delta_y)
        
        if pressed(pygame.K_1) == Switch.pushed_down:
            self.change_cursor(Cursor.platform)

        if pressed(pygame.K_2) == Switch.pushed_down:
            self.change_cursor(Cursor.eraser)

        if pressed(pygame.K_z) == Switch.pushed_down:
            del self._platforms[-1]

        # save and exit if esc is pressed

        if pressed(pygame.K_ESCAPE) == Switch.pushed_down:
            self.write_level()
            self._quit_callback()
        
    
    def update(self, events):
        '''Use mouse to drag and make rectangle platforms'''

        screen = events.screen()

        current_click = events.mouse().left_button()
        mouse_pos = events.mouse().get_position()

        
        if self._cursor == Cursor.platform:
            self.draw_platform(current_click, mouse_pos)

        elif self._cursor == Cursor.eraser:
            self.erase(mouse_pos, current_click)
        
        for rectangle in self._platforms:
            super().render_rectangle(rectangle, color=(200,0,100))

        if not self._unfinished_rect == None:
            super().render_rectangle(self._unfinished_rect, color=(100, 100, 100))

        super().render(screen, (self._title.get_surface(), Point(10,10)), relative_screen=True)
        self.handle_keyboard(events)
    

if __name__ == '__main__':

    screen = init()
    editor = Editor('level', screen)
    event_handler = Event()

    running = True

    while running:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        event_handler.update(pygame.key.get_pressed(), pygame.mouse.get_pressed(), pygame.mouse.get_pos())
        pygame.time.Clock().tick(60)
        editor.update(event_handler)
        pygame.display.flip()
