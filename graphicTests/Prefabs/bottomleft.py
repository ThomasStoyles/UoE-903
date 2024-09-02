import pygame
from Prefabs.button import Button
from Prefabs.textbox import Textbox
from Prefabs.text import Text
from Prefabs.alignment import HAlignContainer

# BottomLeftSidebar - Houses Total Frame Data, Play Button and Frame Naviagation
class BottomLeftSidebar():
    def __init__(self, screen) -> None:
        self.x = 0
        self.y = screen.get_height() - 80
        self.framesText= Text(80,60,"0")
        self.playButton = Button(130,60, "Play")
        self.leftButton = Button(60,60, "<")
        self.rightButton = Button(60,60, ">")
        self.currentFrameText = Text(80,60,"0")
        self.backtoBeginButton = Button(60,60, "[<")
        self.forwardtoEndButton = Button(60,60, ">]")
        self.container = HAlignContainer([Text(130,60,"Total Frames:", 25),self.framesText,self.backtoBeginButton, self.leftButton,self.currentFrameText,self.rightButton,self.forwardtoEndButton, self.playButton])
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
        self.playButton.is_hovered()
        self.leftButton.is_hovered()
        self.rightButton.is_hovered()
        self.backtoBeginButton.is_hovered()
        self.forwardtoEndButton.is_hovered()

        