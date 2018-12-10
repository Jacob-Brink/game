
class Animation():

    def __init__(self, image_surface_list):
        '''Organizes an animation'''
        self._position = 0
        self._image_surface_list = image_surface_list
        self._list_length = len(self._image_surface_list)
        
    def return_next(self):
        '''Returns next image in the sequence'''
        
        # change position to be next index or if at end restart
        self._position = (self._position+1)%self._list_length

        return self._image_surface_list[self._position]
