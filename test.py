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

    def test_camera(self):
        # import, initialize, and test transformations provided by camera
        from lib.modules.gui.camera import Camera

        screen_size = (640, 480)
        camera = Camera(return_screen(), (0,0))

        rect = pygame.Rect(0, 0, 10, 20)

        # test camera is visible
        assert camera.is_visible(rect) == True
        assert camera.return_camera_position() == (0,0)
        assert camera.return_disp_rect(rect).width == 10
        center = camera._view_rect.center
        camera.zoom(2)

        # test that center of camera stays in place
        assert camera._view_rect.center == center
        
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
