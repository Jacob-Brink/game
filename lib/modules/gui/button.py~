import pygame

from lib.modules.gui.text import Text

class Button:

    def __init__(self, normal_text_surface, hover_text_surface, callback):
        '''
        Constructs a button with the text, creates surface constants: one for when the mouse hovers
        over the button, and one for when the mouse does not hover over the button.
        '''

        self._clicked = False
        self._callback = callback

        self._HOVER_SURFACE = hover_text_surface
        self._NORMAL_SURFACE = normal_text_surface

        self._rect = self._NORMAL_SURFACE.get_rect()

        self._shown_surface = self._NORMAL_SURFACE

    def return_surface(self):
        return self._shown_surface

    def return_callback(self):
        return self._callback

    def is_clicked(self):
        return self._clicked

    def update(self, event):
        '''
        Update function updates the Button with mouse events. If the mouse hovers, the displayed text
        surface is assigned the hover surface. If not, the displayed text will be the normal surface
        '''
        self._clicked = False
        # if mouse hovers over button
        if self._rect.collidepoint(event.mouse().get_position()):

            self._shown_surface = self._HOVER_SURFACE

            # if mouse is clicked call callback
            if event.mouse().left_button():

                self._clicked = True

        # if mouse does not hover over button
        else:

            self._shown_surface = self._NORMAL_SURFACE
