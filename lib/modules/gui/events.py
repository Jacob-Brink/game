import pygame
from enum import Enum
'''
This class is a wrapper for events and allows events to be handled more simply
'''


class Mouse:
    '''
    This class represents a mouse with two buttons: left clicker and right clicker
    '''

    
    def __init__(self):
        self._left_button = False
        self._right_button = False
        self._cursor_position = (0,0)

    def set_position(self, position_tuple):
        self._cursor_position = position_tuple

    def get_position(self):
        return self._cursor_position
        
    def left_button(self):
        return self._left_button

    def right_button(self):
        return self._right_button

    def update_left_state(self, new_state):
        self._left_button = new_state
        
    def update_right_state(self, new_state):
        self._right_button = new_state


class Keyboard:
    '''
    This keyboard class represents a keyboard with the keys necessary for this game.
    '''

    
    def __init__(self):
        '''
        This constructor constructs a small list of keys that are off by default
        '''

        self._keys = {
            'space': False,
            'a': False,
            'd': False,
            'w': False,
            's': False,
            'ctrl': False,
            'z': False
            }
    def _check_bool(self, var):
        '''
        Checks for invariants
        '''

        if not isinstance(var, bool):
            raise ValueError('Key Value must be of type bool (i.e: True or False)')

    def reset(self):
        '''
        Resets all values to False
        '''
        for key in self._keys:
            self._keys[key] = False
        
    def is_pressed(self, key_key):
        '''
        Returns boolean state of given key
        '''
        
        return self._keys[key_key]

    def set_key(self, key_key, key_value):
        '''
        Sets key to given boolean
        '''

        self._check_bool(key_value)
        self._keys[key_key] = key_value

    
    
class Event:
    '''
    This class handles events cleanly for events the game needs to check.
    '''

    
    def __init__(self):
        self._mouse = Mouse()
        self._keyboard = Keyboard()

    def update(self,pressed_keys, pressed_mouse_button, mouse_pos):
        '''
        Takes events and organizes them
        '''

        self._keyboard.reset()
        
        keys = pressed_keys
        buttons = pressed_mouse_button

        
        if keys[pygame.K_SPACE]: self._keyboard.set_key('space', True)
        if keys[pygame.K_w]: self._keyboard.set_key('w', True)
        if keys[pygame.K_a]: self._keyboard.set_key('a', True)
        if keys[pygame.K_d]: self._keyboard.set_key('d', True)
        if keys[pygame.K_s]: self._keyboard.set_key('s', True)

        


        # update mouse position
        self._mouse.set_position(mouse_pos)

        
        # update mouse button states
        self._mouse.update_left_state(buttons[0])

        self._mouse.update_right_state(buttons[2])

    

        
    def mouse(self):
        return self._mouse

    def keyboard(self):
        return self._keyboard
