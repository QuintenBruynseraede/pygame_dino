import pygame

dino = pygame.image.load('Assets/Images/dino.png')
jumpObstacle = pygame.image.load('Assets/Images/jumpobstacle.png')
duckObstacle = pygame.image.load('Assets/Images/duckobstacle.png')

def w(img):
    return img.get_rect().size[0]

def h(img):
    return img.get_rect().size[1]