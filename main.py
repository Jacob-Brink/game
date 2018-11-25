import pygame
#FIX MODULE DIRECTORY PROBLEM SO MENU AND MAIN CAN BE RUN
from lib.modules.gui.menu import Menu
#from game import Game


def init():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('The Game')
    pygame.display.flip()
    
    return screen

def test_callback():
    print('callback')

def main():

    running = True
    
    screen = init()

    menu = Menu(screen, 'middle')
    menu.add_button('Play Game', test_callback)
    menu.add_button('Debug Mode', test_callback)
    menu.add_button('Quit', test_callback)

    while running:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        menu.update(pygame.mouse.get_pos(), True)
        pygame.display.flip()

if __name__ == '__main__':


    main()
    
