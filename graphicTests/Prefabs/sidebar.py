import pygame
from Prefabs.button import Button
from Prefabs.alignment import VAlignContainer

# Sidebar - Houses node operation buttons
class Sidebar():
    def __init__(self, screen) -> None:
        self.x = screen.get_width() - 150
        self.y = 0
        self.addNodeButton = Button(130,60, "Add Node")
        self.addLinkButton = Button(130,60, "Add Link")
        self.mutateButton = Button(130,60, "Mutate")
        self.container = VAlignContainer([self.addNodeButton, self.addLinkButton, self.mutateButton])
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
        self.addNodeButton.is_hovered()
        self.addLinkButton.is_hovered()
        self.mutateButton.is_hovered()
        

        
        