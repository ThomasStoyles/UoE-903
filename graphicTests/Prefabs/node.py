import pygame
import globals
from Prefabs.graphWindow import Mode

class Node():
    def __init__(self, px=0, py=0, id=0) -> None:
        self.id = id
        self.mutant = False
        self.connected = []
        self.weights = []
        self.pX = px
        self.pY = py
        self.x = px - 20
        self.y = py - 20
        self.surface = pygame.Surface((40,40),pygame.SRCALPHA)
        self.centreX = (1/2 * 40)
        self.centreY = (1/2 * 40)
        self.rect = None
        self.font = pygame.font.SysFont("Arial", 32)
        self.drag = False
        self.selected = False
        pass
    
    def draw(self, screen):
        #global globals.selectedNode
        if globals.selectedNode != self.id:
            self.selected = False
            
        self.surface.fill((0,0,0,0))
        color = (255,0,0)
        if self.mutant == False:
            color = (0,200,200)
        if self.selected == True:
            pygame.draw.circle(self.surface, (0,0,0), (20, 20), 40)
            pygame.draw.circle(self.surface, (255,255,255), (20, 20), 22)
        pygame.draw.circle(self.surface, color, (20, 20), 20)   
        textObject = self.font.render(str(self.id), False, (255,255,255))
        self.surface.blit(textObject, (self.centreX - textObject.get_width()/2, self.centreY - textObject.get_height()/2))
        self.rect = screen.blit(self.surface, (self.x, self.y))
        pass

    def get_pos(self):
        return (self.pX,self.pY)
    
    def set_pos(self, px, py):
        self.pX = px
        self.pY = py
        self.x = px - 20
        self.y = py - 20
        
    def move_node(self,event, dict, graphWindow):
        #global globals.selectedNode
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered() == True:
            if event.button == 1:
                if globals.selectedNode != self.id:
                    self.drag = False
                    globals.selectedNode = self.id
                    self.selected = True
                elif globals.selectedNode == self.id:
                    self.drag = True
                    self.selected = True
                    globals.selectedNode = self.id
            elif event.button == 3:
                self.selected = False
                globals.selectedNode = -1
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            
                self.drag = False
                
        
        if event.type == pygame.MOUSEMOTION and self.drag == True:
            mX, mY = pygame.mouse.get_pos()
            self.pX = mX
            self.pY = mY
            oX = (self.pX-(1/2) * graphWindow.width - graphWindow.panX)/graphWindow.zoom
            oY = (self.pY-(1/2) * graphWindow.height - graphWindow.panY)/graphWindow.zoom
            dict[self.id] = [oX,oY]

    def is_clicked(self, graphWindow, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if graphWindow.mode == Mode.LINK_NODE_ONE:
                if self.is_hovered():
                    if event.button == 1:
                        graphWindow.linknode1 = self.id
                        graphWindow.mode = Mode.LINK_NODE_TWO
            elif graphWindow.mode == Mode.LINK_NODE_TWO:
                if self.is_hovered():
                    if event.button == 1:
                        graphWindow.linknode2 = self.id
                        graphWindow.mode = Mode.LINK_NODE_PROCESS

    def is_hovered(self):
        mouse_position = pygame.mouse.get_pos()
        if self.rect != None:
            if self.rect.collidepoint(mouse_position):
                return True
            else:
                return False
