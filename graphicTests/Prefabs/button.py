import pygame

# Button Class -> To easily confirm actions.
class Button ():
    def __init__(self, width, height, text='', x=0, y=0, font=pygame.font.SysFont("Arial", 32), color=(0,0,0), textColor=(255,255,255)) -> None:
        self.color = color
        self.textColor = textColor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.surface = pygame.Surface((self.width, self.height))
        self.font = font
        self.centreX = (1/2 * self.width)
        self.centreY = (1/2 * self.height)
        self.rect = None
        self.invert = False
        pass

    def draw(self, screen):
        color1 = self.color
        color2 = self.textColor
        if self.invert:
            color1 = self.textColor
            color2 = self.color
        self.surface.fill(color1);
        textObject = self.font.render(self.text, False, color2)
        self.surface.blit(textObject, (self.centreX - textObject.get_width()/2, self.centreY - textObject.get_height()/2))
        self.rect = screen.blit(self.surface, (self.x, self.y))
            

    def is_hovered(self):
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            self.invert = True
            return True
        else:
            self.invert = False
            return False

    def clickedCallback(self, event, callback):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered() == True:
            callback()

