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

        p.change_x(4)
        p.change_y(5)

        assert p.x() == 4
        assert p.y() == 5

        # test overloading
        
        p = Point(1,2)
        s = Point(1,2)

        assert p == s

        s = Point(0,0)

        assert not p == s

        assert str(p) == '<1,2>'
        
    def test_rectangle(self):
        '''Test rectangle'''
        from lib.modules.gui.rectangle import Rectangle
        from lib.modules.gui.rectangle import Point

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
        assert Rectangle(1,2,-3,4).get_center() == Rectangle(-2, 2, 3, 4).get_center()
        assert Rectangle(3, 5, -2, -2) == Rectangle(1, 3, 2, 2)

        # test basic functions
        assert Rectangle(1,2,3,4).list_basic_values() == [1,2,3,4]

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
        assert r.get_bottom_left() == Point(-4,4)

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
        assert r.get_center() == Point(2.5,5)

        # test pretty print
        assert str(Rectangle(1, 2, 3, 4)) == '1 2 3 4'

        # test collide function
        colliding = [[(0,0,4,4), (1,2,-3,-4)],[(0,0,1,1), (1,1,2,2)], [(0,0,10,5),(-2,-3,3,4)]]
        separate = [[(1,1,2,2), (5,5,1,1)],[(0,0,3,4),(1,40,10,1)]]

        for r in colliding:
            assert Rectangle(*r[0]).collides_with(Rectangle(*r[1]))
        for r in separate:
            assert not Rectangle(*r[0]).collides_with(Rectangle(*r[1]))

        # test collide point function
        rect = Rectangle(0,0,2,3)

        colliding_points = [Point(0,0), Point(0,3), Point(2,3), Point(2,0)]
        noncolliding_points = [Point(3,4), Point(-1,-1), Point(4,4), Point(8,0)]

        for point in colliding_points:
            assert rect.collide_point(point) == True

        for point in noncolliding_points:
            assert rect.collide_point(point) == False
        
        
    def test_camera(self):
        '''Test camera'''
        # import, initialize, and test transformations provided by camera
        from lib.modules.gui.camera import Camera
        from lib.modules.gui.rectangle import Rectangle, Point
        
        screen_size = Point(640, 480)
        camera = Camera(return_screen(), (0,0))

        rect = pygame.Rect(0, 0, 10, 20)

        # test camera is visible
        assert camera.is_visible(Rectangle(1,2,3,4)) == True
        assert camera.return_rectangle().get_top_left() == Point(0,0)
        assert camera.return_disp_rect(Rectangle(10,20,10,0)).width == 10

        center = camera.return_rectangle().get_center()
        camera.zoom(.5)

        # test that center of camera stays in place and that width and height are scaled appropriately
        assert camera.return_rectangle().get_center() == center
        assert camera.return_rectangle().get_size() == Point(screen_size.x()*2, screen_size.y()*2)
        assert camera.return_rectangle().get_top_left() == Point(-320.0, -240.0)

        # test that zoom causes good scaling
        assert camera.return_disp_rect(Rectangle(1,2,8,6)).width == 4
        assert camera.return_true_rect(camera.return_disp_rect(Rectangle(1,2,10,13))).get_w() == 10


        point = Point(24, 56)

        camera.zoom(1)
        
        # test camera true and display returning functions
        assert camera.return_rectangle().get_top_left() == Point(0, 0)
        assert camera.return_rectangle().get_size() == Point(screen_size.x(), screen_size.y())

        assert camera.return_true_position(camera.return_display_position(point)) == Point(24, 56)
        assert camera.return_display_position(point) == Point(24, 56)

        camera.zoom(.5)
        
        # test zoom and unzoom features
        assert camera.zoom_values(4,8,12) == [2,4,6]
        assert camera.unzoom_values(2, 4, 6) == [4, 8, 12]
        
    

if __name__ == '__main__':
    unittest.main()
