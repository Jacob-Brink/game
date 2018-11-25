import pygame
from pygame import Rect
import time

from menu import Menu
from player import Player
from camera import Camera

def test_callback():
    print('Callback called')


def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('BLASK')

    pygame.display.flip()
    
    rect = Rect(10, 10, 10, 10)
    camera = Camera(Rect(0,0,640,480))
    menu = Menu(screen, 'left')
    menu.add_button('HELLO', test_callback)
    menu.add_button('Hi', test_callback)

    men = Menu(screen, 'middle')
    men.add_button('Middle Button', test_callback)

    m = Menu(screen, 'right')
    m.add_button('Right', test_callback)
    # Event loop
    while 1:

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        men.update(pygame.mouse.get_pos(), True)
        menu.update(pygame.mouse.get_pos(), True)
        m.update(pygame.mouse.get_pos(), True)
    
        #updates screen
        pygame.display.flip()


if __name__ == '__main__': main()
