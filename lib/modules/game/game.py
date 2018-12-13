import pygame

from lib.modules.gui.view import View
from lib.modules.gui.menu import Menu
from lib.modules.gui.text import Text
from lib.modules.gui.events import Switch

from lib.modules.game.player import Player

from lib.modules.physics.physics_engine import Physics

from lib.modules.gui.rectangle import Rectangle

from lib.modules.game.level import Level
from lib.modules.game.bomb import Bomb
from lib.modules.game.timer import Timer


class Game(View):

    def __init__(self, screen, level, go_back, debug_mode):
        '''View that holds game entities, deals with collision, and handles the entire game!!!'''

        self._debug = debug_mode
        self._screen = screen
        
        super().__init__(self._screen)
        self._menu = Menu(self._screen, 'right', 'Press Escape to Quit', [('Quit', go_back)])
        self._go_back = go_back

        self._physics = Physics(debug_mode)
        
        # player, platform, and bomb list
        self._level = Level(level)
        self._platforms = self._level.get_platforms()
        self._bomb_list = []

        # find kill height by lowest platform bottom y
        lowest_y = self._platforms[0].get_bottom()
        for platform in self._platforms:
            if platform.get_bottom() > lowest_y:
                lowest_y = platform.get_bottom()
        self._lowest_y = lowest_y + 100
        
        self._done = False
        self._restart_timer = Timer()
        self._restart_delay = 10

        self.start_game()

        
    def _game_over(self, message_string):
        '''Ends game'''
        self._done = True
        self._restart_timer.restart()
        self._message_string = message_string

        self._winner_message = Text(self._message_string, 100, (100, 200, 100), 'middle', self._screen.get_height()/2)

        
    def start_game(self):
        '''Restarts game'''
        # reset players
        self._player1 = Player(self._level.get_player_positions()[0].get_top_left() , 0, self._debug, self.throw_bomb_wrapper(), self._lowest_y)
        self._player2 = Player(self._level.get_player_positions()[1].get_top_left() , 1, self._debug, self.throw_bomb_wrapper(), self._lowest_y)
        self._player_list = [self._player1, self._player2]

        # clear bomb list
        self._bomb_list = []

        
    def throw_bomb_wrapper(self):
        '''Returns throw bomb callback'''
        def throw_bomb_callback(velocity, bomb_type):

            self._bomb_list.append(Bomb(velocity, bomb_type))
            
        return throw_bomb_callback

    
    def update(self, events):
        '''Updates all game objects'''

        # Quit Game if escape is pressed
        if events.keyboard().is_pressed(pygame.K_ESCAPE) == Switch.pushed_down:
            self._go_back()

        self._screen = events.screen()
        
        if events.was_resized():
            super().update(self._screen)

        # set camera to track two players
        super().track(self._player1, self._player2)        
        
        # physics sim
        self._physics.update(events, self._player_list, self._bomb_list, self._platforms)

        # render platforms
        for platform in self._platforms:
            # if rectangle is visible, render it
            if super().is_visible(platform):
                super().render_rectangle(platform, color=(0,0,0))
        
        # render appropriate players
        for player in self._player_list:
            super().render_rectangle(player.return_healthbar_and_color()[0], color=player.return_healthbar_and_color()[1])
            super().render_rectangle(player.return_rectangle_and_color()[0], color=player.return_rectangle_and_color()[1])
            super().render(player.return_surface_and_pos())
            
            if self._debug:
                super().render_line(player.return_velocity_vector()*100)
        
        # render appropriate bomb
        for bomb in self._bomb_list:
            # if surface is visible, render it
            if super().is_visible(bomb.return_rect()):
                super().render_rectangle(bomb.return_rect(), color=bomb.get_color())

                
        # display fps
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
            
            super().render(self._winner_message.get_surface_and_pos(self._screen.get_width()), relative_screen=True)
            super().render(Text('Restarting in: '+str(round(self._restart_delay-self._restart_timer.read())), 100, (100, 200, 100), 'middle', self._screen.get_height()/2+110).get_surface_and_pos(self._screen.get_width()), relative_screen=True)


        # when restart timer finishes, game restarts
        if self._restart_timer.read() > self._restart_delay:

            self._restart_timer.stop()
            self.start_game()
            self._done = False
            

