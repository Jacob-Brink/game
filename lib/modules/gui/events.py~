import pygame
from enum import Enum
'''
This class is a wrapper for events and allows events to be handled more simply
'''


class Mouse():
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

        
class Event:
    '''
    This class handles events cleanly for events the game needs to check.
    '''

    
    def __init__(self):
        self._mouse = Mouse()
        

    def update(self,pressed_keys, pressed_mouse_button, mouse_pos):
        '''
        Takes events and organizes them
        '''

        keys = pressed_keys
        buttons = pressed_mouse_button

        
        if keys[pygame.K_SPACE]: print('space')
        if keys[pygame.K_w]: print('w')
        if keys[pygame.K_a]: print('a')
        if keys[pygame.K_d]: print('d')
        if keys[pygame.K_s]: print('s')



        # update mouse position
        self._mouse.set_position(mouse_pos)

        
        # update mouse button states
        self._mouse.update_left_state(buttons[0])

        self._mouse.update_right_state(buttons[2])



        
    def mouse(self):
        return self._mouse
