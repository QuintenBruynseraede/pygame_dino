import pygame

class Obstacle(object):
    x = 0
    y = 0
    w = 0
    h = 0
    rect = pygame.Rect(x,y,w,h)
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def move(self,dx,dy):
        self.x += dx
        self.y += dy
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)

class JumpObstacle(Obstacle):
    def __init__(self,x,y,w,h):
        super().__init__(x,y,w,h)

class DuckObstacle(Obstacle):
    def __init__(self,x,y,w,h):
        super().__init__(x,y,w,h)
