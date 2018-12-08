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
    start = 2
    coin = 3
    eraser = 4

# dictionary of width and height for cursor items
ITEM_DIMENSIONS = {
    Cursor.start: (40, 40),
    Cursor.coin: (20, 20)
}
        
    
class Editor(View):

    def __init__(self, screen, level, quit_callback):
        '''Constructs an editor object derived from base class View. The editor object allows for easy creation of new levels.'''

        # construct view object that will handle all rendering and blitting stuff
        super().__init__(screen, pygame.Rect((0,0), screen.get_size()))
        self._menu = Menu(screen, 'right', 'Editor', [('Save', self.save_level_callback()), ('Platform', self.change_cursor(Cursor.platform)), ('Starting Block', self.change_cursor(Cursor.start)), ('Coin', self.change_cursor(Cursor.coin)),('Exit', quit_callback)])

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
        def callback(*args):
            self._cursor = new_cursor
        return callback
        
    def write_level(self):
        '''Write to level all platforms and items'''
        with open(self._level, 'w') as level_file:
            for platform in self._platforms:
                level_file.write(str(platform.x)+ ' ' + str(platform.y) + ' ' + str(platform.w) + ' ' + str(platform.h) + '\n')

    def read_level(self):
        '''Load level platforms into level editor'''
        with open(self._level) as level_file:
            [self._platforms.append(pygame.Rect([int(string_integer) for string_integer in line.strip().split()])) for line in level_file]

    def move_camera(self, events):
        '''With given events, controls camera movement.'''

        keys_pressed = events.keyboard()
        delta_x = 0
        delta_y = 0

        change = 5

        if keys_pressed.is_pressed(pygame.K_a) == Switch.down:
            delta_x -= change

        if keys_pressed.is_pressed(pygame.K_d) == Switch.down:
            delta_x += change

        if keys_pressed.is_pressed(pygame.K_w) == Switch.down:
            delta_y -= change

        if keys_pressed.is_pressed(pygame.K_s) == Switch.down:
            delta_y += change

        super().move(change_x=delta_x, change_y=delta_y)

    def _return_rect(self, first_pos, second_pos):
        '''Transforms two mouse position points into rectangle.'''

        width = second_pos[0] - first_pos[0]
        height = second_pos[1] - first_pos[1]
        return pygame.Rect(first_pos[0], first_pos[1], width, height)

    def draw_platform(self, current_click, mouse_position):
        '''Draws platform with mouse clicks'''
        # Start drawing rectangle
        if current_click == Switch.pushed_down and not self._first_click:

            self._first_click = True
            # get true first position
            self.first_pos = super().return_true_position(mouse_position)

        # Continue drawing rectangle
        if current_click == Switch.down and self._first_click:

            # get true second position
            self.second_pos = super().return_true_position(mouse_position)

            self._unfinished_rect = pygame.Rect(self._return_rect(self.first_pos, self.second_pos))
            

        # End drawing of rectangle on second click event
        if self._first_click == True and current_click == Switch.pushed_up:

            # reset first click so new rectangle can be created
            self._first_click = False

            # get true second position
            self.second_pos = super().return_true_position(mouse_position)

            # return rectangles with from two true positions
            self._platforms.append(self._return_rect(self.first_pos, self.second_pos))

            # remove temp rectangle
            self._unfinished_rect = None


    def save_level_callback(self):
        '''Saves level, given to button'''
        def callback(*args):
            self.write_level()
        return callback
        
    def _collides_platform(self, rect):
        '''Checks for collisions, returns boolean value'''
        for rectangle in self._platforms:
            if rectangle.colliderect(rect):
                return True
        return False
            
    def place_item(self, current_click, mouse_pos):
        '''Places an item only if the user places it where it does not overlap with another rectangle'''
        item_rect = pygame.Rect(super().return_true_position(mouse_pos), ITEM_DIMENSIONS[self._cursor])

        if not self._collides_platform(item_rect):
            if current_click == Switch.pushed_up:
                if self._cursor == Cursor.coin:
                    self._coins.append((item_rect.x, item_rect.y))
                if self._cursor == Cursor.start:
                    self._start = item_rect
        print(self._coins)
                
    
    def update(self, events):
        '''Use mouse to drag and make rectangle platforms'''

        screen = events.screen()

        
        current_click = events.mouse().left_button()
        mouse_pos = events.mouse().get_position()
        
        if self._cursor == Cursor.platform:
            self.draw_platform(current_click, mouse_pos)
        elif self._cursor == Cursor.coin or self._cursor == Cursor.start:
            self.place_item(current_click, mouse_pos)
        elif self._cursor == Cursor.eraser:
            self.erase(current_click, mouse_pos)
        
        for rectangle in self._platforms:
            super().render_rectangle(rectangle, color=(200,0,100))

        if not self._unfinished_rect == None:
            super().render_rectangle(self._unfinished_rect, color=(100, 100, 100))

        self.move_camera(events)
        self._menu.update(events)
    

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
