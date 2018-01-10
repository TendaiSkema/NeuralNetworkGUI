import pygame
from random import randrange as rand
from random import shuffle
import numpy as np
from collections import Counter
from time import sleep

class Graph:

        def __init__(self,screen,size,start_point,thickness,color,edge_thickness):
                #static colors
                self.RED = (255,0,0)
                self.GREEN = (0,255,0)
                self.BLUE = (0,0,255)
                self.BLACK = (0,0,0)
                self.WHITE = (255,255,255)

                #var definition
                self.screen = screen
                self.size = size
                self.x_offset = start_point[0]
                self.y_offset = start_point[1]
                self.line_width = thickness
                self.color = color
                self.edge = edge_thickness

                #init all screen vars
                self.rec_size = (self.size[0]+self.x_offset,self.size[1]+self.y_offset)

        def update(self,points):

                #draw main window
                pygame.draw.rect(self.screen, self.WHITE, (self.x_offset-1,self.y_offset-1,self.rec_size[0]+1,self.rec_size[1]+1))
                
                #if the point array has less then 2 elements jump over 
                if len(points)>1:
                
                        #convert arrays
                        points = np.array(points)
                        unit_size = (self.rec_size[0]/points[-1][0],self.rec_size[1]/np.amax([i[1] for i in points]))                       

                        #connect all points
                        for i in range(1,len(points)):

                                #calculate all points
                                x1 = self.x_offset+points[i-1][0]*unit_size[0]
                                y1 = self.y_offset+self.rec_size[1]-points[i-1][1]*unit_size[1]
                                x2 = self.x_offset+points[i][0]*unit_size[0]
                                y2 = self.y_offset+self.rec_size[1]-points[i][1]*unit_size[1]

                                #draw the line
                                pygame.draw.line(self.screen,self.color,(x1,y1),(x2,y2),self.line_width)
                        pygame.draw.rect(self.screen, self.BLACK, (self.x_offset-self.edge,self.y_offset-self.edge,self.rec_size[0]+self.edge+2,self.rec_size[1]+self.edge+2),self.edge)
