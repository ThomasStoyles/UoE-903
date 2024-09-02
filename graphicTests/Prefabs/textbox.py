import pygame

# Textbox Class -> To type text.
class Textbox ():
    def __init__(self, width, height, text='', x=0, y=0, font=pygame.font.SysFont("Arial", 32), color=(100,100,100), textColor=(255,255,255)) -> None:
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
        self.rect = pygame.Rect(self.x,self.y, self.width,self.height)
        self.invert = False
        self.active = False
        pass

    def draw(self, screen):
        color1 = self.color
        color2 = self.textColor
        if self.active:
            color1 = (200,200,200)
            color2 = self.textColor
        self.surface.fill(color1);
        textObject = self.font.render(self.text, False, color2)
        self.surface.blit(textObject, (self.centreX - textObject.get_width()/2, self.centreY - textObject.get_height()/2))
        self.rect = screen.blit(self.surface, (self.x, self.y))
            

    def clickedCallback(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                    if event.key == pygame.K_RETURN:
                        print(self.text)
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode