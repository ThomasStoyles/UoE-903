import pygame
from enum import Enum

class Mode(Enum):
    NORMAL = 1
    ADD_NODE = 2
    LINK_NODE_ONE = 3
    LINK_NODE_TWO = 4
    LINK_NODE_PROCESS = 5
    PLAY_INIT = 6
    PLAY = 7 

class GraphWindow():
    def __init__(self, screen) -> None:
        self.zoom = 500
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.panX = 0
        self.panY = 0
        self.drag = False
        self.mode = Mode.NORMAL
        self.linknode1 = None
        self.linknode2 = None
        pass
    
    def draw(self, screen):
        font = pygame.font.SysFont("Arial", 18)
        
        if self.mode == Mode.ADD_NODE:
             x, y = pygame.mouse.get_pos()
             pygame.draw.circle(screen, (0,200,0), (x,y), 10)
        if self.mode == Mode.LINK_NODE_ONE:
             x, y = pygame.mouse.get_pos()
             textObject = font.render("1",True,(0,0,255))
             screen.blit(textObject, (x-20 - textObject.get_width()/2, y+20 - textObject.get_height()/2))
             pygame.draw.circle(screen, (0,0,255), (x,y), 10)
        if self.mode == Mode.LINK_NODE_TWO:
             x, y = pygame.mouse.get_pos()
             textObject = font.render("2",True,(0,255,255))
             screen.blit(textObject, (x-20 - textObject.get_width()/2, y+20 - textObject.get_height()/2))
             pygame.draw.circle(screen, (0,255,255), (x,y), 10)
        pass
    
    def drag_to_pan(self, event):
        if self.mode == Mode.NORMAL:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                        self.drag = True
                        # dragStartX, dragStartY = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                        self.drag = False
                        
            if event.type == pygame.MOUSEMOTION and self.drag:
                relX, relY = event.rel
                self.panX += relX
                self.panY += relY

                
                

        