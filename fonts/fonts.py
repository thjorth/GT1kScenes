import pygame
import singleton

FONT_SIZE_EFFECT = 28
FONT_SIZE_SCENE = 450
FONT_SIZE_SCENE_LABEL = 36
FONT_SIZE_EDIT = 48

FONT_PATH = "fonts/NewsflashBB.ttf"

class Fonts(singleton.SingletonClass):
    def __init__(self):
        self.effect_font = pygame.font.Font(FONT_PATH, FONT_SIZE_EFFECT)
        self.scene_font = pygame.font.Font(FONT_PATH, FONT_SIZE_SCENE)
        self.scene_label_font = pygame.font.Font(FONT_PATH, FONT_SIZE_SCENE_LABEL)
        self.edit_font = pygame.font.Font(FONT_PATH, FONT_SIZE_EDIT)