import unittest
import pygame


def test_callback():
    pass

def return_screen():
     pygame.init()
     screen = pygame.display.set_mode((640,480))
     pygame.display.set_caption('Test Mode')
     pygame.display.flip()
     return screen   

class TestGame(unittest.TestCase):

    def test_point(self):
        from lib.modules.gui.rectangle import Point
        p = Point(2, 3)
        assert p.x() == 2
        assert p.y() == 3
        assert str(p) == '<2,3>'

        p.change_x(4)
        p.change_y(5)

        assert p.x() == 4
        assert p.y() == 5
    
    def test_rectangle(self):
        '''Test rectangle'''
        from lib.modules.gui.rectangle import Rectangle

        # test invalid rectangles
        try:
            invalid = Rectangle('asfd', 3, 4, 5)
            assert False
        except:
            pass

        try:
            invalid = Rectangle((1,2,4),3)
            assert False
        except:
            pass

        # test normalize with negative sizes
        assert Rectangle(1,2,-3,4) == Rectangle(-2, 2, 3, 4)
        assert Rectangle(3, 5, -2, -2) == Rectangle(1, 3, 2, 2)

        # test basic functions
        assert Rectangle(1,2,3,4).list_basic_values == [1,2,3,4]

        r = Rectangle(1,2,3,4)
        assert r.copy() is not r

        assert isinstance(r.return_pygame_rect(), pygame.Rect)
        
        rect = Rectangle((0,0), (4,5))

        # test accessor methods
        assert rect.get_x() == 0
        assert rect.get_y() == 0
        assert rect.get_w() == 4
        assert rect.get_h() == 5

        print(rect.get_center())
        assert rect.get_center() == Point(2, 2.5)

        assert rect.get_bottom_left() == Point(0, 5)
        assert rect.get_bottom_right() == Point(4, 5)
        assert rect.get_top_left() == Point(0,0)
        assert rect.get_top_right() == Point(4,0)

        assert rect.get_size() == Point(4,5)
        
        # test mutator methods
        r = Rectangle(-2, 3, 4, 5)
        r.change_top_left(Point(1,2))
        
        assert r.get_top_left() == Point(1,2)
        assert r.get_size() == Point(4,5)

        r.change_top_right(Point(2,3))
        assert r.get_top_right() == Point(2,3)
        assert r.get_size() == Point(4,5)

        r.change_bottom_left(Point(-4,4))
        assert r.get_size() == Point(4,5)
        assert r.get_bottom_left(Point(-4,4))

        r.change_bottom_right(Point(-5,4))
        assert r.get_bottom_right() == Point(-5,4)
        assert r.get_size() == Point(4,5)

        # test move and scale
        r = Rectangle(-3, 4, 5, 2)
        r.move(Point(10, 20))
        assert r.get_size() == Point(5,2)
        assert r.get_top_left() == Point(7, 24)

        r = Rectangle(1, 2, 3, 6)
        r.scale(10)
        assert r.get_size() == Point(30, 60)
        assert r.get_get_center() == Point(2,4)

        # test pretty print
        assert str(Rectangle(1, 2, 3, 4)) == '1 2 3 4'

        # test collide function
        colliding = [[(0,0,4,4), (1,2,-3,-4)],[(0,0,1,1), (1,1,2,2)], [(0,0,10,5),(-2,-3,3,4)]]
        separate = [[(1,1,2,2), (5,5,1,1)],[(0,0,3,4),(1,40,10,1)]]
        for r in colliding:
            assert Rectangle(r[0]).collides_with(Rectangle(r[1]))
        for r in separate:
            assert not Rectangle(r[0]).collides_with(Rectangle(r1))
        
    def test_camera(self):
        '''Test camera'''
        # import, initialize, and test transformations provided by camera
        from lib.modules.gui.camera import Camera

        screen_size = (640, 480)
        camera = Camera(return_screen(), (0,0))

        rect = pygame.Rect(0, 0, 10, 20)

        # test camera is visible
        assert camera.is_visible(rect) == True
        assert camera.return_camera_position() == (0,0)
        assert camera.return_disp_rect(rect).width == 10
        center = camera._view_rect.get_center()
        camera.zoom(2)

        # test that center of camera stays in place
        assert camera._view_rect.get_center() == center

        print(camera.return_camera_position())
        assert camera.return_camera_position() == (160.0, 120.0)
        assert camera.return_disp_rect(rect).width == 20
        assert camera.return_true_rect(camera.return_disp_rect(rect)).width == 10


        point = (24, 56)

        camera.zoom(4)
        
        # test camera true and display returning functions
        assert camera.return_camera_position() == (400.0, 300.0)
        assert camera._view_rect.size == (screen_size[0]/4, screen_size[1]/4)

        assert camera.return_true_position(camera.return_display_position(point)) == (24, 56)
        assert camera.return_display_position(point) == (-1504.0, -976.0)

        # test zoom and unzoom features
        assert camera.zoom_values(1,2,3) == [4,8,12]
        assert camera.unzoom_values(4, 8, 12) == [1, 2, 3]
        
    

if __name__ == '__main__':
    unittest.main()
