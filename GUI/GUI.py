import numpy as np
import pygame
from Pygame_additions.PygameGraph import Graph

class GUI:
    def __init__(self):
        #Befehls Liste
        #GUI_EVENTS =
        #[
            
        #]
        #static colors
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.RED = (0,0,255)
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        #start pygame
        pygame.init()
        #Window vars
        self.dimension = (800,600)
        self.background_color = (46,46,46)

        #Init screen
        self.screen = pygame.display.set_mode(self.dimension)

        #loop vars
        self.clock = pygame.time.Clock()

    def get_gui_events(self):
        #get key events
        pressed = pygame.key.get_pressed()
        

    def start(self):

        acc_graph = Graph(self.screen,(186,160),(40,40),2,(0,128,46),3)
        loss_graph = Graph(self.screen,((186,160)),(40+160+80,40),2,(0,128,0),3)
        points = [[1,1]]
        
        print(acc_graph.get_info())
        print(loss_graph.get_info())
        
        #----------main loop------------------
        run = True
        while run:
            points.append([points[-1][0]+1,points[-1][1]+1])
            #reset screen
            self.screen.fill(self.background_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:#exit if cross was klicked
                    run = False

            events = self.get_gui_events()

            #final updates
            acc_graph.update(points)
            loss_graph.update(points)
            pygame.draw.rect(self.screen,self.WHITE,(0,0,533,400),5)
            pygame.display.update()         #update all
            self.clock.tick(60)             #wait (in FPS)

        pygame.quit()

gui = GUI()
gui.start()
#quit()
