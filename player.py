import pygame
from pygame import Rect
import math
import sys

from lib.modules.physics.rigid_body import RigidBody
from lib.modules.physics.vector import Vector

class Player:

    def __init__(self, rect, mass, image, screen):

        self._r_body = RigidBody(rect, mass)
        self._image_sprite = pygame.image.load(image)
        self._screen = screen

    def update(self):

        self._r_body.update()
        self._screen.blit(self._image_sprite, (self._r_body.return_rect().x, self._r_body.return_rect().y))

    def add_force(self, force_vector):
        self._r_body.apply_force(force_vector)

    def return_rect(self):
        return self._r_body.return_rect()

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Player Class Test')

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    surface.fill((250,250,250))

    screen.blit(surface, (0,0))

    image = 'lib/data/assets/test.png'


    r = Rect(0, 0, 10, 10)

    p = Player(r, 1000, image, screen)


    running = True
    decrease = 1
    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                pygame.display.quit()
                pygame.quit()
                running = False


        if running == False:
            break


        x_diff = pygame.mouse.get_pos()[0] - p.return_rect().x
        y_diff = pygame.mouse.get_pos()[1] - p.return_rect().y


        decrease += .01
        p.add_force(Vector(math.degrees(math.atan2(y_diff, x_diff)), math.sqrt(x_diff**2 + y_diff**2)/decrease))
        #p.add_force(Vector(-90, -10))
        screen.blit(surface, (0,0))
        p.update()
        pygame.display.flip()
