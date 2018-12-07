import pygame
import math
from enum import Enum



class Switch(Enum):
    '''Models a button or key and different states'''
    down = 1
    up = 2
    pushed_down = 3
    pushed_up = 4

class Mouse:
    '''This class represents a mouse with two buttons: left clicker and right clicker'''

    def __init__(self):
        self._left_button = Switch.up
        self._right_button = Switch.down
        self._cursor_position = (0,0)

    def set_position(self, position_tuple):
        self._cursor_position = position_tuple

    def get_position(self):
        return self._cursor_position

    def left_button(self):
        return self._left_button

    def right_button(self):
        return self._right_button

    def set_left_state(self, new_state):
        self._left_button = new_state

    def set_right_state(self, new_state):
        self._right_button = new_state


class Keyboard:
    '''This keyboard class represents a keyboard with the keys necessary for this game.'''

    def __init__(self):
        '''This constructor constructs a small list of keys that are off by default'''
        # keys is a file containing a list of all possible key values
        # This makes it alot easier to have all keys supported without manually typing them out :)
        self._keys = {}
        with open('keys') as keys_file:
            for line in keys_file:
                exec('p = pygame.'+line.strip(), locals(), globals())
                global p
                self._keys[p] = Switch.up
        # create keys dictionary

    def is_pressed(self, key_key):
        '''Returns boolean state of given key'''
        return self._keys[key_key]

    def set_key(self, key_key, key_value):
        '''Sets key to given Switch value'''
        self._keys[key_key] = key_value



class Event:
    '''This class is a wrapper for events and allows events to be handled more simply'''

    def __init__(self, screen):
        '''Constructs new event object'''
        self._mouse = Mouse()
        self._keyboard = Keyboard()
        self._delta_time = 1
        self._fps = 0
        self._window_exit = False
        self._screen = screen

    def update(self, delta_time):
        '''Takes events and organizes them'''

        # set keys to up or down first, then later check if event is up or down
        keys_pressed = pygame.key.get_pressed()
        for element in range(0, len(keys_pressed)):
            if keys_pressed[element] == 1:
                self._keyboard.set_key(element, Switch.down)
            elif keys_pressed[element] == 0:
                self._keyboard.set_key(element, Switch.up)
        
        
        # loop through events in given pygame.event.get()
        for event in pygame.event.get():

            # handle window events, including Exit and Resize
            if event.type == pygame.QUIT:
                self._window_exit = True

            elif event.type == pygame.VIDEORESIZE:
                self._screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # handle keyboard and wrap in keyboard object
            # handle keyboard down events
            if event.type == pygame.KEYDOWN:
                self._keyboard.set_key(event.key, Switch.pushed_down)

            # handle keyboard up events
            if event.type == pygame.KEYUP:
                self._keyboard.set_key(event.key, Switch.pushed_up)


            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:
                self._mouse.set_left_state(Switch.down)
            else:
                self._mouse.set_left_state(Switch.up)

            if mouse_pressed[1]:
                self._mouse.set_right_state(Switch.down)
            else:
                self._mouse.set_right_state(Switch.up)
            
                
            # handle mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._mouse.set_left_state(Switch.pushed_down)
                elif event.button == 3:
                    self._mouse.set_right_state(Switch.pushed_down)
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self._mouse.set_left_state(Switch.pushed_up)
                elif event.button == 3:
                    self._mouse.set_right_state(Switch.pushed_up)
                
                
            if event.type == pygame.MOUSEMOTION:
                self._mouse.set_position(event.pos)
            #print(pygame.mouse.get_pos())




        # store delta time and fps value
        self._delta_time = delta_time
        if self._delta_time == 0:
            self._fps = '99999'
        else:
            self._fps = int(1/self._delta_time*1000)
    def screen(self):
        return self._screen

    def quit(self):
        return self._window_exit

    def fps(self):
        return self._fps

    def delta_time(self):
        return self._delta_time

    def mouse(self):
        return self._mouse

    def keyboard(self):
        return self._keyboard
