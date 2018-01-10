import numpy as np
import pygame

class GUI:
    def __init__(self):
        #Befehls Liste
        GUI_EVENTS =
        [
            
        ]
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
        #----------main loop------------------
        run = True
        while run:
            #reset screen
            self.screen.fill(self.background_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:#exit if cross was klicked
                    run = False

            events = self.get_gui_events()

            #final updates
            pygame.display.update()         #update all
            self.clock.tick(60)                  #wait (in FPS)

    pygame.quit()


gui = GUI()
gui.start()
quit()
