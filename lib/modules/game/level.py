from lib.modules.gui.rectangle import Rectangle, Point
from lib.modules.gui.platform import Platform


PLAYER_SIZE = Point(100,150)

PLAYER_POSITION_COLOR = [(255, 0, 0), (0, 0, 255)]
WRONG_PLACE_COLOR = (100, 100, 100)

class PlayerPosition(Rectangle):

    def __init__(self, center_point, player_num):
        '''Represents Player Position block'''
        super().__init__(Point(0,0), PLAYER_SIZE)
        super().set_center(center_point)
        
        self._placeable_color = PLAYER_POSITION_COLOR[player_num]
        self._wrong_color = WRONG_PLACE_COLOR
        self._is_placeable = True
        self._set_color()

    def _set_color(self):
        '''Sets color based on placeability'''
        if self._is_placeable:
            self._current_color = self._placeable_color
        else:
            self._current_color = self._wrong_color
        
    def get_color(self):
        '''Return color'''
        return self._current_color

    def is_placeable(self):
        '''Return is placeable'''
        return self._is_placeable

    def change_placeability(self, placeable_bool):
        '''Sets is placeable to placeable bool'''
        self._is_placeable = placeable_bool
        self._set_color()

    def __str__(self):
        '''Returns string for file writing'''
        top_left = super().get_top_left()
        return str(top_left.x()) + ' ' + str(top_left.y())



class Level:

    def __init__(self, file_name):
        '''Initialize level and load up level'''

        self._platforms = []
        # by default player positions are at origin
        self._player_positions = [PlayerPosition(Point(0,0), 0), PlayerPosition(Point(0,0), 1)]
        self._level = file_name
        self.read_level()

        
    def read_level(self):
        '''Load level platforms into level editor'''

        with open(self._level) as level_file:

            line_num = 0

            try:
            
                for line in level_file:
                    string_integers = line.strip().split()

                    if line_num <= 1:
                        self._player_positions[line_num] = PlayerPosition(Point(float(string_integers[0]), float(string_integers[1])), line_num)
                        print(self._player_positions[line_num])
                    else:
                        self._platforms.append(Platform(Rectangle(*[float(string_integer) for string_integer in string_integers])))

                    line_num += 1

            except Exception as e:
                print('File is possibly corrupt. Editing it now should fix that')
    

    def write_level(self):
        '''Write to level all platforms and player positions'''

        with open(self._level, 'w') as level_file:

            # write player top left positions first
            for player_pos in self._player_positions:
                level_file.write(str(player_pos)+'\n')
                
            # then write platform positions
            for platform in self._platforms:
                level_file.write(str(platform.copy())+'\n')


    def get_platforms(self):
        '''Returns platforms'''

        return self._platforms

    def get_player_positions(self):
        '''Returns player positions'''
        return self._player_positions


