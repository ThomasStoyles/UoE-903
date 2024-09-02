import pygame
from Prefabs.button import Button
from Prefabs.textbox import Textbox
from Prefabs.alignment import HAlignContainer

# TopBar - Houses the Open File, Simulate and Hide Buttons
class Topbar():
    def __init__(self) -> None:
        self.x = 10
        self.y = 10
        self.openFileButton = Button(130,60, "Open File")
        self.presetTextBox = Textbox(80,60,"0")
        self.loadPresetButton = Button(180,60, "Load Preset")
        self.container = HAlignContainer([self.openFileButton,self.presetTextBox, self.loadPresetButton])
        info = pygame.display.Info()
        self.surface = pygame.Surface((info.current_w, 120))
        pass

    def draw(self, screen):
        self.container.draw(screen)
        # self.openFileButton.draw(screen)
        # self.simulateButton.draw(screen)
        # self.hideButton.draw(screen)
        self.openFileButton.is_hovered()
        self.loadPresetButton.is_hovered()
        

        
        