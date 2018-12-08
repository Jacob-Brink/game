from lib.modules.physics.vector import Vector
from lib.modules.physics.line import Line
from lib.modules.physics.parallelogram import Parallelogram
import math
import pygame

def list_points(_rect):
    '''Return points in clockwise order'''
    return [_rect.topleft, _rect.topright, _rect.bottomright, _rect.bottomleft]

class Physics:

    def __init__(self, debug_mode=False):
        self._debug_mode = debug_mode

    def _collision(self, rigid_body, rect_list):
        past_velocity_vector = rigid_body.return_past_velocity()
        past_rect = rigid_body.return_past_rect()
        current_rect = rigid_body.return_rect()
    
    def return_greatest_parallelogram(self, rect1, velocity_vector):
        '''Return parrallelogram from two rects being connected'''
        #FIX OR DELETE, ONLY USEFUL FOR PREVENTING SUPER FAST COLLISIONS WHERE MOTION PARALLELOGRAM IS NEEDED
        greatest_p = None
        greatest_area = 0

        # figure out greatest parallelogram formed from sides and velocity
        rect_points = list_points(rect1)
        for index in range(0, len(rect_points)):
            point1 = rect_points[index]
            point2 = rect_points[(index+1)%len(rect_points)]
            p = Parallelogram(Vector(point1, x_component=(point2[0]-point1[0]), y_component=(point2[1]-point1[1])), Vector(point1, direction=velocity_vector.return_direction(), magnitude=velocity_vector.return_magnitude()))
            # if the area of the figure is greater than the greatest area, update the greatest parallelogram
            if p.return_area() > greatest_area:
                greatest_p = p
                greatest_area = p.return_area()
                           
        # check diagonals
        for index in range(0, 2):
            point1 = rect_points[index]
            point2 = rect_points[(index+2)%len(rect_points)]
            p = Parallelogram(Vector(point1, x_component=(point2[0]-point1[0]), y_component=(point2[1]-point1[1])), Vector(point1, direction=velocity_vector.return_direction(), magnitude=velocity_vector.return_magnitude()))
            # if the area of the figure is greater than the greatest area, update the greatest parallelogram
            if p.return_area() > greatest_area:
                print('diagonal is bigger!!')
                greatest_p = p
                greatest_area = p.return_area()

        return greatest_p
    
    
    def _return_x_collision(self, vector, y_line, rect):
        '''Returns x position of where vector and y_line intersect'''
        line = Line(vector.return_slope(), (rect.topleft))
        return line.x_value(y_line)
        
    def _return_y_collision(self, vector, x_line, rect):
        '''Returns y posiiton of where vector and x_line intersect'''
        line = Line(vector.return_slope(), (rect.topleft))
        return line.y_value(x_line)

    def reposition(self, player_list, rigid_body_list, immovable_rect_list, delta_time):
        '''Return new rectangle based on how two rectangles collided'''
        MARGIN_PIXEL = 1
        for player in player_list:

            for platform in immovable_rect_list:
            # if a collision occurs, figure out how what side the player collided
                if player.collides_with(platform):
                    past_rect = player.return_past_rect()
                    rect = player.return_rect()
                    body_velocity = player.return_velocity_vector()
                    body_direction = body_velocity.return_direction()


                    # on top
                    if past_rect.y+past_rect.h <= platform.y:
                        print('correcting top')
                        player.set_rect(pygame.Rect(rect.x, platform.y-rect.h-MARGIN_PIXEL, rect.w, rect.h))

                    # on bottom
                    if past_rect.y >= platform.y + platform.h:
                        print('correcting bottom')
                        player.set_rect(pygame.Rect(rect.x, platform.y+platform.h+MARGIN_PIXEL, rect.w, rect.h))

                    # on left
                    if past_rect.x >= platform.x + platform.w:
                        print('correcting to left')
                        player.set_rect(pygame.Rect(platform.x+platform.w+MARGIN_PIXEL, rect.y, rect.w, rect.h))

                    # on right
                    if past_rect.x+past_rect.w <= platform.x:
                        print('correcting to right')
                        player.set_rect(pygame.Rect(platform.x-rect.w-MARGIN_PIXEL, rect.y, rect.w, rect.h))
                        
                    # apply appropriate force
                    print('Collision Occurred')
                    player.set_velocity(body_velocity*(-.2))
                    


    def update(self, events, player_list, rigid_body_list, platform_list):
        '''Calculate collisions, reposition from collisions, work with forces, etc'''
        for player in player_list:
            player.update(events)
            

        self.reposition(player_list, rigid_body_list, platform_list, events.delta_time())
        
if __name__ == '__main__':
    '''Tests'''

    p = Physics()
    rectangle = pygame.Rect(0,0,10, 5)
    vertical = Vector((0,0), direction=0, magnitude=50)
    print(p.return_greatest_parallelogram(rectangle, vertical))

    
