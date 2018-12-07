import unittest
import pygame


def test_callback():
    pass

def return_screen():
     pygame.init()
     screen = pygame.display.set_mode((640,480))
     pygame.display.set_caption('Test Mode')
     pygame.display.flip()
     return screen   

class TestGame(unittest.TestCase):

    def __init__(self):

           
    
    def test_button(self):
        from lib.modules.gui.button import Button
        
        b = Button('Button Text', test_callback, (0, 255, 0), screen, 32, coordinate_tuple)
        
