import pygame

class Camera:

    def __init__(self, view_rect):
        '''Constructor contructs new camera object determined by the provided viewing rectangle'''
        self._change_x = 0
        self._change_y = 0
        self._view_rect = view_rect


    def move(self, change_x, change_y):
        '''Public method called to move camera to new location. Note that move does not provide any travel by itself and that the calling code must take this into account.'''
        self._change_x += change_x
        self._change_y += change_y
        self._view_rect = self._view_rect.move(change_x, change_y)

    def zoom(self, magnitude):
        '''Zoom if I can get to this part'''
        pass

    def return_true_position(self, disp_position_tuple):
        '''Returns absolute position of object when given position coordinates of type tuple'''
        return (disp_position_tuple[0] + self._view_rect.x, disp_position_tuple[1] + self._view_rect.y)

    def return_display_position(self, tru_position_tuple):
        '''Returns display position of given object by returning the difference in coordinates'''
        return (tru_position_tuple[0] - self._view_rect.x, tru_position_tuple[1] - self._view_rect.y)

    def return_true_rect(self, disp_rect):
        '''Returns rectangle with absolute / true positions'''
        return pygame.Rect(disp_rect.x + self._view_rect.x, disp_rect.y + self._view_rect.y, disp_rect.w, disp_rect.h)

    def return_disp_rect(self, tru_rect):
        '''Returns rectangle with positions relative to window screen'''
        return pygame.Rect(tru_rect.x - self._view_rect.x, tru_rect.y - self._view_rect.y, tru_rect.w, tru_rect.h)

    def is_visible(self, object_rect):
        '''Boolean value of whether given object is in the camera's viewing rectangle. True for is visible and False for invisible.'''
        return object_rect.colliderect(self._view_rect)


if __name__ == '__main__':
    '''
    Tests for camera class.
    '''


    from pygame import Rect

    c = Camera(Rect(0, 0, 10, 10))
    r = Rect(1, 1, 2, 3)

    #checks visibility function
    assert(c.is_visible(r) == True)

    r = r.move(100, 0)

    assert(c.is_visible(r) == False)

    print('\nAll Tests Have Passed.')
