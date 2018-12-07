import pygame

from lib.modules.gui.view import View
from lib.modules.gui.menu import Menu
from lib.modules.game.player import Player
from lib.modules.gui.text import Text
from lib.modules.physics.physics_engine import Physics
from lib.modules.gui.events import Switch

class Game(View):

    def __init__(self, screen, level, go_back, debug_mode):
        '''View that holds game entities, deals with collision, and handles the entire game!!!'''
        super().__init__(screen, pygame.Rect((0,0), (screen.get_size())))
        self._menu = Menu(screen, 'right', 'THE BEST GAME EVER!!!', ('Quit', go_back))
        self._player = Player()
        self._debug = debug_mode

        self._paused = False

        self._physics = Physics()
        self._level = level
        self._platforms = []
        self._load_level()

    def _load_level(self):
        '''Loads level platforms into game'''
        with open(self._level, 'r') as level_file:
            [self._platforms.append(pygame.Rect([int(string_integer) for string_integer in line.strip().split()])) for line in level_file]

    def update(self, events, screen):
        '''Updates all game objects boi'''

        # physics engine repositions player according to placement and other factors
        self._physics.reposition(self._player, self._platforms, events.delta_time())
        
        # Pause Game if escape is pressed
        if events.keyboard().is_pressed(pygame.K_ESCAPE) == Switch.pushed_down:
            self._paused = not self._paused


        # Handle Game Events
        if not self._paused:
            self._player.update(events)
        else:
            self._menu.update(events, screen)
            
        # if debug mode is on, then show velocity vectors, force vectors, and coordinate position
        if self._debug:
            x = self._player.return_rect().centerx
            y = self._player.return_rect().centery
            pygame.draw.aaline(screen, (255,0,0), (x, y), (self._player.return_velocity_vector().return_x_component()*1000 + x, self._player.return_velocity_vector().return_y_component()*1000 + y))
            coordinate_text = Text('X: ' + str(x) + ' Y: ' + str(y), 64, (200, 0, 200), (x-100, y+100))
            fps_text = Text('FPS: ' + str(events.fps()), 32, (0, 100, 200), (10, 40))
            velocity_text = Text('Velocity: ' + str(round(self._player.return_velocity_vector().return_magnitude()))+' Direction:' + str(round(self._player.return_velocity_vector().return_direction())), 32, (255,255,255), (200,40))
            super().render(screen, self._player.return_surface_and_pos(), fps_text.get_surface_and_pos(), coordinate_text.get_surface_and_pos(), velocity_text.get_surface_and_pos())
        else:
            # Do physics stuff
            super().render(screen, self._player.return_surface_and_pos())


        for platform in self._platforms:
            pygame.draw.rect(screen, (0, 255,0), super().camera().return_disp_rect(platform))
