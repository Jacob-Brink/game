

class Camera:

    def __init__(self, view_rect):
        self._change_x = 0
        self._change_y = 0
        self._view_rect = view_rect

    def move(self, change_x, change_y):
        self._change_x += change_x
        self._change_y += change_y
        self._view_rect = self._view_rect.move(self._change_x, self._change_y)

    def zoom(self, magnitude):

        #zoom stuff ha ha ha
        pass

    def return_position(self, object_rect):

        return (object_rect.x - self._view_rect.x, object_rect.y - self._view_rect.y)

    def return_visible(self, object_rect):

        return object_rect.colliderect(self._view_rect)

if __name__ == '__main__':

    from pygame import Rect
    
    c = Camera(Rect(0, 0, 10, 10))
    r = Rect(1, 1, 2, 3)

    #checks visibility function
    assert(c.return_visible(r) == True)

    r = r.move(100, 0)

    assert(c.return_visible(r) == False)

    print('tests have passed')
