import pygame

class HAlignContainer():
    def __init__(self, children = [], gap=10, pad=10) -> None:
        self.x = 0
        self.y = 0
        self.children = children
        self.xGap = gap
        self.childSize = len(self.children)
        self.verticalPad = pad
        pass
    
    def draw(self, screen):
        if self.childSize != 0:
            acc = self.x + self.xGap
            for child in self.children:
                child.x = acc 
                child.y = self.y + self.verticalPad
                child.draw(screen)
                acc += self.xGap + child.width
        pass

class VAlignContainer():
    def __init__(self, children = [], gap=10, pad=10) -> None:
        self.x = 0
        self.y = 0
        self.children = children
        self.yGap = gap
        self.childSize = len(self.children)
        self.horizontalPad = pad
        pass
    
    def draw(self, screen):
        if self.childSize != 0:
            acc = self.y + self.yGap
            for child in self.children:
                child.x = self.x + self.horizontalPad
                child.y = acc 
                child.draw(screen)
                acc += self.yGap + child.height
        pass
            