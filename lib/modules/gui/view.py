

class View:
    def __init__(self):
        '''
        Constructs a view object with given id and view_class. View class must have update function and a switch return that returns next id of view.
        '''

        self._visible = False
        self._next_view_id = 0
        self._switch_view = False

    def get_visibility(self):

        return self._visible
        
    def set_visibility(self, visible_bool):
        '''
        Sets visibility to given visibility value. Used when inheriting object such as a menu has a button pressed 
        for another view to be opened, such as the Game view.
        '''
        
        self._visible = visible_bool

       
    def switch(self, ID):
        '''
        Called by view when a new view must be shown. E.g. A menu inheriting view will call switch when the editor is selected.
        '''
        print(ID)
        self._switch_view = True
        self._next_view_id = ID
        self._visible = False
        print(self._next_view_id)
        
    def get_new_view(self):
        '''
        If the view switches to another view, this function returns new view id.
        If the current view does not change, this function returns 0
        '''

        print(self._next_view_id)
        return self._next_view_id
        

        
        
if __name__ == '__main__':

    from menu import Menu

    m = Menu(1, 'left', 'title', 123)
