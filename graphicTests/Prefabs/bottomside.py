import pygame
from Prefabs.button import Button
from Prefabs.textbox import Textbox
from Prefabs.text import Text
from Prefabs.alignment import VAlignContainer

# BottomSidebar - Houses simulation operation buttons and textboxes
class BottomSidebar():
    def __init__(self, screen) -> None:
        self.x = screen.get_width() - 150
        self.y = screen.get_height() - 500
        self.animationDelayTextBox = Textbox(130,60, "0.05")
        self.relativeFitnessTextBox = Textbox(130,60, "1.6")
        self.statusText = Text(130,20," ",18)
        self.simulateButton = Button(130,60, "Simulate")
        self.container = VAlignContainer([Text(130,20,"Animation Delay",18),self.animationDelayTextBox,Text(130,20,"Relative Fitness",18),self.relativeFitnessTextBox, self.simulateButton, self.statusText])
        self.container.x = self.x
        self.container.y = self.y
        info = pygame.display.Info()
        self.surface = pygame.Surface((info.current_w, 120))
        pass

    def draw(self, screen):
        self.container.draw(screen)
        # self.openFileButton.draw(screen)
        # self.simulateButton.draw(screen)
        # self.hideButton.draw(screen)
        self.simulateButton.is_hovered()

        