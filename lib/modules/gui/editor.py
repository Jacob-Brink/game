if __name__ == '__main__':
    from text import Text
    from events import Event
    from view import View
    from camera import Camera
else:    
    from lib.modules.gui.text import Text
    from event import Event

    
import pygame
    
def init():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('The Game')
    pygame.display.flip()
    
    return screen



class Editor(View):

    def __init__(self, level, screen):
        '''
        Constructs an editor object derived from base class View. The editor object allows for easy cration of new levels.
        '''
        
        self._platforms = []
        
        self._screen = screen
        self._level = level
        self._first_click = False
        self.first_pos = None
        self.second_pos = None
        
        self._camera = Camera(pygame.Rect((0,0), screen.get_size()))

    def write_level(self):

        with open(self._level) as level_file:
            for platform in self._platforms:
                level_file.write(str(platform.x)+ ' ' + str(platform.y) + ' ' + str(platform.w) + ' ' + str(platform.h) + '\n')

    def read_level(self):

        with open(self._level) as level_file:
            
    
    def move_camera(self, events):
        '''
        With given events, controls camera movement.
        '''
        
        keys_pressed = events.keyboard()
        delta_x = 0
        delta_y = 0

        change = .01
        
        if keys_pressed.is_pressed('a'):
            delta_x -= change

        if keys_pressed.is_pressed('d'):
            delta_x += change

        if keys_pressed.is_pressed('w'):
            delta_y -= change

        if keys_pressed.is_pressed('s'):
            delta_y += change

        self._camera.move(delta_x, delta_y)
        
    def _return_rect(self, first_pos, second_pos):
        '''
        Transforms two mouse position points into rectangle.
        '''

        width = second_pos[0] - first_pos[0]
        height = second_pos[1] - first_pos[1]
        return pygame.Rect(first_pos[0], first_pos[1], width, height)
            
    def update(self, events):
        '''
        Use mouse to drag and make rectangle platforms
        '''
        
        current_click = events.mouse().left_button()

        # first click event
        if current_click and not self._first_click:
            
            self._first_click = True

            # get true first position
            self.first_pos = self._camera.return_true_position(events.mouse().get_position())

            
        # dragging event
        if current_click and self._first_click:

            self.second_pos = self._camera.return_true_position(events.mouse().get_position())

            pygame.draw.rect(self._screen, (0, 255,0), self._camera.return_disp_rect(self._return_rect( self.first_pos, self.second_pos )))

            
        # second click event    
        if self._first_click == True and current_click == False:

            # reset first click so new rectangle can be created
            self._first_click = False

            # get true second position
            self.second_pos = self._camera.return_true_position(events.mouse().get_position())

            # return rectangles with from two true positions
            self._platforms.append(self._return_rect(self.first_pos, self.second_pos))

            
        for rectangle in self._platforms:
            pygame.draw.rect(self._screen, (0, 100, 0), (self._camera.return_display_position((rectangle.x, rectangle.y)), (rectangle.width, rectangle.height)))

        self.move_camera(events)

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
        
                
        editor.update(event_handler)
        pygame.display.flip()
