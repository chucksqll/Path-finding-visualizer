import tkinter as tk
import sys, pygame
import numpy as np
import math
from time import time
pygame.init()
BLACK=(0, 0, 0)
BLACKSHADOW=(100,100,100)
SHADOW = (192, 192, 192)
WHITE = (255, 255, 255)
LIGHTGREEN = (0, 255, 0)
GREEN = (0, 200, 0)
LIGHTBLUE= (0, 0, 255) 
RED=(255,0,0)
GOLD=(255,215,0)
start_color=LIGHTBLUE
walls_color=BLACK
dest_color=LIGHTBLUE
path_color=GOLD
visited_node_color=GREEN
unvisited_node_color=BLACKSHADOW
frame_color=BLACKSHADOW
class Node:
    def __init__(self,x,y,color=SHADOW,prev_x=None,prev_y=None,is_visited=False):
        self.x=x
        self.y=y
        self.previous_x=prev_x
        self.previous_y=prev_y
        self.side_size=10
        self.is_visited=is_visited
        self.color=color
    def draw(self):
        pygame.draw.rect(screen, self.color, 
                pygame.Rect(self.x*self.side_size, self.y*self.side_size,
                 self.side_size, self.side_size))
        pygame.display.update()

class Map:
    def __init__(self,width,height,side_size):
        self.side_size=side_size
        # self.rows=int(width/side_size)
        self.rows=self.columns=int(height/side_size)
        self.grid=[]
        self.start=None
        self.end=None
        
    def create_grid(self):
        for i in range(self.rows):
            self.grid.append([0 for j in range(self.columns)])
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i][j]=Node(i,j)
        #create frame
        for i in range(self.rows):
            self.grid[i][0].is_visited=True
            self.grid[i][0].color=frame_color
            self.grid[i][self.columns-1].is_visited=True
            self.grid[i][self.columns-1].color=frame_color

        for i in range(self.columns):
            self.grid[0][i].is_visited=True
            self.grid[0][i].color=frame_color
            self.grid[self.columns-1][i].is_visited=True
            self.grid[self.columns-1][i].color=frame_color

    def draw_grid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i][j].draw()
    def create_walls(self,x,y):
        #check if in the grid
        if (x>0 and x <self.rows-1) and (y>0 and y<self.columns-1):
            if (not (x==self.start[0] and y==self.start[1])) and (not (x==self.end[0] and y==self.end[1])):
                self.grid[x][y].is_visited=True
                self.grid[x][y].color=walls_color
                self.grid[x][y].draw()
    def is_cord_on_map(self,x,y):
        if 0<x and x <self.rows-1 and 0<y and y<self.columns-1:
            return True
        else:
            return False
    def set_start(self,x,y):
        self.start=(x, y)
        self.grid[x][y].color=start_color
        self.grid[x][y].is_visited=True
        self.grid[x][y].draw()
    def set_end(self,x,y):
        self.end=(x,y)
        self.grid[x][y].color=dest_color
        self.grid[x][y].draw()
    def restart(self):
        mapa.create_grid()
        mapa.draw_grid()
        mapa.set_start(17,6)
        mapa.set_end(27,29)
    def begin(self):
        open_list=[]
        def make_step(node):
            open_list.remove(node)
            temp =[-1, 1]
            for i in temp:   
                if self.grid[node.x+i][node.y].is_visited==False:
                    self.grid[node.x+i][node.y]=Node(node.x+i,node.y,visited_node_color,
                                                node.x,node.y,True)
                    open_list.append(self.grid[node.x+i][node.y])
                    self.grid[node.x+i][node.y].draw()

                if self.grid[node.x][node.y+i].is_visited==False:
                    self.grid[node.x][node.y+i]=Node(node.x,node.y+i,visited_node_color,
                                                node.x,node.y,True)

                    open_list.append(self.grid[node.x][node.y+i])
                    self.grid[node.x][node.y+i].draw()
                self.grid[self.end[0]][self.end[1]].color=dest_color
                self.grid[self.end[0]][self.end[1]].draw()
                # pygame.display.update()
        def find_dest():
            open_list.append(self.grid[self.start[0]][self.start[1]])
            make_step(self.grid[self.start[0]][self.start[1]])
            i=0
            counter =0
            while not self.grid[self.end[0]][self.end[1]].is_visited and counter <=self.rows*self.columns :
                i+=1
                if i>10000:
                    counter+=1
                    i=0
                    temp=open_list.copy()
                    for node in temp:
                        make_step(node)
        
        def make_path():
            i, j=self.grid[self.end[0]][self.end[1]].previous_x,  self.grid[self.end[0]][self.end[1]].previous_y
            path=[]
            if self.grid[self.end[0]][self.end[1]].is_visited==True:
                while not( self.grid[i][j].x==self.start[0] and self.grid[i][j].y==self.start[1]):
                    path.append((i,j))
                    self.grid[i][j].color=path_color
                    i, j=self.grid[i][j].previous_x,  self.grid[i][j].previous_y
                    
            self.grid[self.end[0]][self.end[1]].color=dest_color
 
        open_list.append(self.grid[self.start[0]][self.start[1]])
        make_step(self.grid[self.start[0]][self.start[1]])
        find_dest()
        make_path()

        self.draw_grid()

width, height= 640, 480
screen = pygame.display.set_mode((width, height))

mapa=Map(width,height,10)
mapa.create_grid()
mapa.draw_grid()
mapa.set_start(17,6)
mapa.set_end(27,29)

class Button:
    def __init__(self,x_pos,y_pos,width,height,text,color,font_size,font_color):
        self.rect=pygame.Rect(x_pos,y_pos,width,height)
        self.width=width
        self.height=height
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.font=pygame.font.SysFont('Arial', font_size)
        self.text=text
        self.color =color
        self.font_color=font_color
    def draw(self):
        pygame.draw.rect(screen,self.color,self.rect)
        screen.blit(self.font.render(self.text, True, self.font_color), (self.x_pos, self.y_pos))

# button to run/restart 
start_button =Button(500,400,120,40,"  START",LIGHTBLUE,30,LIGHTGREEN)
start_button.draw()
##button origin point
origin_node_button=Button(490,110,120,30,"PICK START",LIGHTBLUE,20,LIGHTGREEN)
origin_node_button.draw()
##button destination point
dest_node_button=Button(490,150,120,30, "  PICK END", LIGHTBLUE,20,LIGHTGREEN)
dest_node_button.draw()
##
starting_button_on=True
origin_button_on=False
dest_button_on=False
##
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        elif event.type ==pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left mouse button down.
                mapa.create_walls(math.floor(event.pos[0]/10),math.floor(event.pos[1]/10))

        elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos[0],event.pos[1]):
                    # prints current location of mouse
                    if starting_button_on== True:
                        mapa.begin()
                        start_button.text=" RESET"
                        starting_button_on=False
                        origin_button_on=False
                        dest_button_on=False
                    else:
                        mapa.restart()
                        start_button.text="  START"
                        starting_button_on=True
                elif origin_node_button.rect.collidepoint(event.pos[0],event.pos[1]):
                    origin_button_on=True
                    dest_button_on=False

                elif dest_node_button.rect.collidepoint(event.pos[0],event.pos[1]):
                    dest_button_on=True 
                    origin_button_on=False

                elif origin_button_on==True:
                    origin_button_on=False
                    if(mapa.is_cord_on_map(math.floor(event.pos[0]/10),math.floor(event.pos[1]/10)) ):
                        mapa.grid[mapa.start[0]][mapa.start[1]]=Node(mapa.start[0],mapa.start[1])
                        mapa.grid[mapa.start[0]][mapa.start[1]].draw()
                        mapa.set_start(math.floor(event.pos[0]/10),math.floor(event.pos[1]/10))

                elif dest_button_on==True:
                    dest_button_on=False
                    if(mapa.is_cord_on_map(math.floor(event.pos[0]/10),math.floor(event.pos[1]/10)) ):
                        mapa.grid[mapa.end[0]][mapa.end[1]]=Node(mapa.end[0],mapa.end[1])
                        mapa.grid[mapa.end[0]][mapa.end[1]].draw()
                        mapa.set_end(math.floor(event.pos[0]/10),math.floor(event.pos[1]/10))

    start_button.draw()
    pygame.display.flip()