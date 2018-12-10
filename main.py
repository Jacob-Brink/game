#!/usr/bin/env python3
import pygame

from lib.modules.gui.menu import Menu
from handler import Handler
from lib.modules.gui.events import Event

FPS_CAP = 60

running = True

def init():
    '''Initializes pygame stuff and returns the screen'''
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    pygame.display.set_caption('The Game')
    pygame.display.flip()

    return screen


def main():
    '''Runs main loop for game'''

    running = True

    screen = init()

    e = Event(screen)
    handler = Handler(screen)
    time_start = pygame.time.get_ticks()

    while handler.is_running() and running:
        # measure change in time for each frame
        delta_time = pygame.time.Clock().tick(120)

        if delta_time <= 0:
            print(delta_time)
            delta_time =.0000001


        # calls update which gets all events from pygame.events.get() and updates all values
        e.update(delta_time)

        # when quit is called, exit program
        if e.quit():
            running = False

        # because of resizing, screen must be updated every tick
        screen = e.screen()

        # update handler for all views
        handler.update(e)

        # flip display and clear it
        pygame.display.flip()
        screen.fill((0, 0, 0))


if __name__ == '__main__':
    main()
