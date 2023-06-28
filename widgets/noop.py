import pygame
import widgets.iWidget

class Noop(widgets.iWidget.IWidget):
    def render(self):
        """" Do nothing """

