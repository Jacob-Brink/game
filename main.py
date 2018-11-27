import pygame
#FIX MODULE DIRECTORY PROBLEM SO MENU AND MAIN CAN BE RUN
from lib.modules.gui.menu import Menu
#from handler import Handler
#from game import Game

running = True

def init():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('The Game')
    pygame.display.flip()
    
    return screen

def test_callback():
    print('callback')

def quit_loop():
    print('Quitting Game')
    global running
    running = False
    print('running:', running)

    
def main():


    global running
    
    screen = init()

    m = Menu(screen, 'left', 'bla')
    m.add_button('hey', test_callback)
    
    while running:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #handler.update(pygame.event.get())
        m.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
        pygame.display.flip()

if __name__ == '__main__':


    main()
    
