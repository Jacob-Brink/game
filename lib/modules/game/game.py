import pygame

from lib.modules.gui.view import View
from lib.modules.gui.menu import Menu
from lib.modules.gui.text import Text
from lib.modules.gui.events import Switch

from lib.modules.game.player import Player

from lib.modules.physics.physics_engine import Physics

from lib.modules.gui.rectangle import Rectangle

from lib.modules.game.bomb import Bomb
from lib.modules.game.timer import Timer


class Game(View):

    def __init__(self, screen, level, go_back, debug_mode):
        '''View that holds game entities, deals with collision, and handles the entire game!!!'''
        self._screen = screen
        
        super().__init__(self._screen)
        self._menu = Menu(self._screen, 'right', 'Press Escape to Quit', [('Quit', go_back)])

        self._go_back = go_back

        self.start_game(debug_mode)
        
        self._physics = Physics(debug_mode)
        
        # player, platform, and bomb list
        self._platforms = []
        self._bomb_list = []

        # load level
        self._level = level
        self._load_level()

        self._done = False
        self._restart_timer = Timer()
        self._restart_delay = 10
        
    def _game_over(self, message_string):
        '''Ends game'''
        self._done = True
        self._restart_timer.restart()
        self._message_string = message_string

    def start_game(self, debug_mode):
        '''Restarts game'''
                
        self._player1 = Player(0, debug_mode, self.throw_bomb_wrapper())
        self._player2 = Player(1, debug_mode, self.throw_bomb_wrapper())
        self._player_list = [self._player1, self._player2]
        self._debug = debug_mode

        
    def _load_level(self):
        '''Loads level platforms into game'''
        with open(self._level, 'r') as level_file:
            [self._platforms.append(Rectangle(*[float(string_integer) for string_integer in line.strip().split()])) for line in level_file]

    def throw_bomb_wrapper(self):
        '''Returns throw bomb callback'''
        def throw_bomb_callback(velocity):

            self._bomb_list.append(Bomb(velocity))
            
        return throw_bomb_callback

    
    def update(self, events):
        '''Updates all game objects'''

        # Quit Game if escape is pressed
        if events.keyboard().is_pressed(pygame.K_ESCAPE) == Switch.pushed_down:
            self._go_back()

        self._screen = events.screen()
        
        if events.was_resized():
            super().update(self._screen)
                
        # update menu
        self._menu.update(events)

        # set camera to track two players
        super().track(self._player1, self._player2)        
        
        # physics sim
        self._physics.update(events, self._player_list, self._bomb_list, self._platforms)

        # render platforms
        for platform in self._platforms:
            # if rectangle is visible, render it
            if super().is_visible(platform):
                super().render_rectangle(platform, color=(0,0,0))
        
        
        # render appropriate bomb
        for bomb in self._bomb_list:
            # if surface is visible, render it
            if super().is_visible(bomb.return_rect()):
                super().render_rectangle(bomb.return_rect(), color=bomb.get_color())

        # render appropriate players
        for player in self._player_list:
            super().render(player.return_surface_and_pos())
            super().render_rectangle(player.return_healthbar_and_color()[0], color=player.return_healthbar_and_color()[1])
            if self._debug:
                super().render_line(player.return_velocity_vector()*100)

        
        

        super().render(Text(str(events.fps()), 20, (100,40, 100), 'left', 10).get_surface_and_pos(self._screen.get_width()), relative_screen=True)
        # handle end game
        if not self._done:
            

            if not self._player1.is_alive() and not self._player2.is_alive():
                self._game_over('Tie')
                
            elif not self._player1.is_alive():
                self._game_over('Player 1 is the winner!')
            
            elif not self._player2.is_alive():
                self._game_over('Player 0 is the winner!')

        elif self._done:
            
            super().render(Text(self._message_string, 100, (100, 200, 100), 'middle', self._screen.get_height()/2).get_surface_and_pos(self._screen.get_width()), relative_screen=True)
            super().render(Text('Restarting in:'+str(round(self._restart_delay-self._restart_timer.read())), 100, (100, 200, 100), 'middle', self._screen.get_height()/2+110).get_surface_and_pos(self._screen.get_width()), relative_screen=True)


        # when restart timer finishes, game restarts
        if self._restart_timer.read() > self._restart_delay:
            self._restart_timer.stop()
            self.start_game(self._debug)
            self._done = False
            

