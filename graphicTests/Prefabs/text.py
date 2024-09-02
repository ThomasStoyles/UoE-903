import pygame

# Text Class -> Text Prefab for writing text to screen.
class Text ():
    def __init__(self, width, height, text='', fontSize=32, x=0, y=0, color=(200,200,200,0.1), textColor=(0,0,0)) -> None:
        self.color = color
        self.textColor = textColor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.surface = pygame.Surface((self.width, self.height))
        self.font = pygame.font.SysFont("Arial", fontSize)
        self.centreX = (1/2 * self.width)
        self.centreY = (1/2 * self.height)
        self.rect = pygame.Rect(self.x,self.y, self.width,self.height)
        pass

    def draw(self, screen):
        color1 = self.color
        color2 = self.textColor
        self.surface.fill(color1);
        textObject = self.font.render(self.text, True, color2)
        self.surface.blit(textObject, (self.centreX - textObject.get_width()/2, self.centreY - textObject.get_height()/2))
        self.rect = screen.blit(self.surface, (self.x, self.y))
