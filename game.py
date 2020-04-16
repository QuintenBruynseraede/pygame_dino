import pygame
import pygame.freetype
import utils
from utils import getTime
import assets
from assets import w,h
from obstacle import Obstacle, JumpObstacle, DuckObstacle
import random

pygame.init()
(width,height) = (1080,480)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Dinosaur Game')
clock = pygame.time.Clock()
font = pygame.freetype.SysFont('Roboto',13)
font_dead = pygame.freetype.SysFont('Roboto',28)

debug = False
dead = False
stop = False


#Variables for dino physics
x, y = 64,200
ax, ay = 0,0.002
vx, vy = 0,0
max_y = 400

#Variables for obstacles
jumpObstacles = []
duckObstacles = []
lastObstacle = 0
Pgenerate = 0.0009     #Parameter for obstacle generation
Tmin = 900          #Minimum ms between generating obstacles
obst_vx,obst_vy = -6,0

score = 0


def dino_rects():
    width = w(assets.dino)
    height = h(assets.dino)
    cx = x+width/2
    cy = y+height/2
    dino_rects = [pygame.Rect(cx,y,width/2,height/4),pygame.Rect(cx,y,width/4,height*0.7),pygame.Rect(cx-30,y,34,height)]
    return dino_rects


while stop == False:
    if dead == False:
        dt = clock.tick(60)
        '''EVENT HANDLING'''
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #If on ground
                    if (y + h(assets.dino) == max_y):
                        vy = -0.8

            elif event.type == pygame.QUIT:
                stop = True

        '''GAME UPDATE'''
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        if y + vy*dt + h(assets.dino) < max_y:
            y += vy * dt
        else:
            y = max_y - h(assets.dino)
            vy = 0

        #Increase difficulty and score
        Pgenerate = min(0.8,Pgenerate+0.00005)
        obst_vx = max(-25,obst_vx-0.008)
        score += 1

        #Generate obstacles
        if random.random() < Pgenerate and getTime() - lastObstacle > Tmin:
            if random.random() > 0.5:
                jumpObstacles.append(JumpObstacle(1150,max_y - h(assets.jumpObstacle),w(assets.jumpObstacle),h(assets.jumpObstacle)))
            else:
                duckObstacles.append(DuckObstacle(1150,max_y - h(assets.duckObstacle)-h(assets.dino)-24,w(assets.duckObstacle),h(assets.duckObstacle)))
               
            lastObstacle = utils.getTime()

        #Update obstacles position
        for o in jumpObstacles:
            o.move(obst_vx,obst_vy)
        for o in duckObstacles:
            o.move(obst_vx,obst_vy)

        #Delete obstacles that are off-screen
        for o in jumpObstacles:
            if o.x < -100:
                jumpObstacles.remove(o)
                del o
        for o in duckObstacles:
            if o.x < -100:
                duckObstacles.remove(o)
                del o

        #Detect collisions with obstacles
        for dino_rect in dino_rects():
            if dino_rect.collidelist(jumpObstacles+duckObstacles) != -1:
                dead = True

    elif dead == True:
        dt = clock.tick(60)
        '''EVENT HANDLING'''
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("Restart")
                    dead = False
                    jumpObstacles.clear()
                    duckObstacles.clear()

                    #Variables for dino physics
                    x, y = 64,200
                    ax, ay = 0,0.002
                    vx, vy = 0,0
                    max_y = 400

                    #Variables for obstacles
                    jumpObstacles = []
                    duckObstacles = []
                    lastObstacle = 0
                    Pgenerate = 0.0009    #Parameter for obstacle generation
                    Tmin = 900          #Minimum ms between generating obstacles
                    obst_vx,obst_vy = -6,0

                    score = 0

            elif event.type == pygame.QUIT:
                print("Exit")
                stop = True


    '''DRAW'''
    screen.fill(utils.white)

    screen.blit(assets.dino,(x,y))
    pygame.draw.line(screen,utils.red,(0,max_y),(1080,max_y),2)

    #Draw obstacles
    for o in jumpObstacles:
        screen.blit(assets.jumpObstacle,(o.x,o.y+5))
    for o in duckObstacles:
        screen.blit(assets.duckObstacle,(o.x,o.y+5))

    #Draw text if dead
    if dead:
        font_dead.render_to(screen, (300, 32), "Game over. Press R to restart.".format(x), utils.black)

    #Draw score
    font.render_to(screen, (64, 32), "Score: {0}".format(score), utils.black)


    
    if debug:
        font.render_to(screen, (800, 32), "x: {:.4f}".format(x), utils.green)
        font.render_to(screen, (800, 52), "y: {:.4f}".format(y), utils.green)
        font.render_to(screen, (800, 72), "vx: {:.4f}".format(vx), utils.green)
        font.render_to(screen, (800, 92), "vy: {:.4f}".format(vy), utils.green)
        font.render_to(screen, (800, 112), "ax: {:.5f}".format(ax), utils.green)
        font.render_to(screen, (800, 132), "ay: {:.5f}".format(ay), utils.green)
        font.render_to(screen, (800, 152), "no obst: {}".format(len(duckObstacles)+len(jumpObstacles)), utils.green)
        font.render_to(screen, (800, 172), "obst_vx: {:.5f}".format(obst_vx), utils.green)
        font.render_to(screen, (800, 192), "Pgenerate: {:.5f}".format(Pgenerate), utils.green)


        for rect in dino_rects():
            pygame.draw.rect(screen,utils.green,rect,1)
        for o in jumpObstacles+duckObstacles:
            pygame.draw.rect(screen,utils.red,o.rect,1)

    pygame.display.update()
            
        