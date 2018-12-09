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
        super().__init__(screen)
        self._menu = Menu(screen, 'right', 'THE BEST GAME EVER!!!', [('Quit', go_back)])
        self._player1 = Player(0)
        self._player2 = Player(1)
        self._debug = debug_mode
        self._go_back = go_back

        self._physics = Physics(debug_mode)
        self._level = level
        self._platforms = []
        self._load_level()
        
        # Add way for more players and rigid body stuff
        self._player_list = [self._player1, self._player2]
        
        self._rigid_body_list = []
        self._surface_pos_list = [self._player1.return_surface_and_pos(), self._player2.return_surface_and_pos()]

        self._num = 0
        
    def _load_level(self):
        '''Loads level platforms into game'''
        with open(self._level, 'r') as level_file:
            [self._platforms.append(pygame.Rect([int(string_integer) for string_integer in line.strip().split()])) for line in level_file]

    def update(self, events):
        '''Updates all game objects'''

        screen = events.screen()

        if events.was_resized():
            super().update_screen_size(screen.get_size())
        
        if events.keyboard().is_pressed(pygame.K_RETURN) == Switch.down:
            super().zoom(.5)
        #super().track(self._player1.return_true_rect(), self._player2.return_true_rect(), events.delta_time())
            
        # update menu
        self._menu.update(events)

        super().track(self._player1.return_true_rect(), self._player2.return_true_rect(), events.delta_time())
        
        # physics sim
        self._physics.update(events, self._player_list, self._rigid_body_list, self._platforms)
        
        # render appropriate rigid_bodies
        for rigid_body in self._rigid_body_list:
            # if surface is visible, render it
            if super().is_visible(rigid_body.return_true_rect()):
                super().render(screen, rigid_body.return_surface_and_pos())

        # render appropriate players
        for player in self._player_list:
            super().render(screen, player.return_surface_and_pos())
            if self._debug:
                super().render_line(player.return_velocity_vector()*100)
                
        # render platforms
        for platform in self._platforms:
            # if rectangle is visible, render it
            if super().is_visible(platform):
                super().render_rectangle(platform)
        

        super().render_rectangle(pygame.Rect(super().return_camera_position(), (20,20)))
                
        # Quit Game if escape is pressed
        if events.keyboard().is_pressed(pygame.K_ESCAPE) == Switch.pushed_down:
            self._go_back()

