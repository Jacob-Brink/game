import pygame

from lib.modules.gui.menu import Menu
from handler import Handler
from events import Event


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

    e = Event()
    handler = Handler(screen)
    
    while running:

        # clear screen with black
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        e.update(pygame.key.get_pressed(), pygame.mouse.get_pressed(), pygame.mouse.get_pos())
        handler.update(e)
        
        pygame.display.flip()

if __name__ == '__main__':


    main()
    
