import pygame
from random import randrange as rand

def start_game():

        #main init
        pygame.init()

        #init all screen vars
        screen_with = 800                       #screen with
        screen_hight = 600                      #screen height
        screen_home_color = (255,255,255)       #main default background (white)
        screen = pygame.display.set_mode((screen_with, screen_hight))   #set screen to size screen with*screen height
        #background image
        background_img = pygame.image.load("Game_pics\GameBackground.jpg") #load
        background_img = pygame.transform.scale(background_img,(screen_with, screen_hight))
        screen.blit(background_img,(0,0)) #add to screen

        #create gametimer
        clock = pygame.time.Clock()

        #ground
        block_size = 60
        counter = block_size
        ground_level = screen_hight*0.7
        ground_image_path = "Game_pics\Brick.jpg"
        ground_blocks = [Ground(ground_level,i,ground_image_path,block_size) for i in range(0,screen_with,block_size+1)]

        #player
        player_x_size = 40
        player_y_size = 55
        player_image_path = "Game_pics\player_mario.png"
        player = Player(ground_level-player_y_size,60,player_x_size,player_y_size,player_image_path)
        
        #start gameloop
        run = True
        while run:
                screen.blit(background_img,(0,0)) #reshow background
                
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                run = False

                #get key events
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_SPACE]:
                        player.set_jump()

                #player updating
                player.check_jumping()
                
                #ground updating AND hole creation
                if not counter:
                        if rand(0,6) != 0:
                                new_ground = Ground(screen_hight*0.7,screen_with+1,ground_image_path,block_size)
                                ground_blocks.append(new_ground)
                        counter = block_size
                else:
                        counter -=1
                update_ground(screen,ground_blocks)
                player.draw(screen)

                #final updates
                pygame.display.update()         #update all
                clock.tick(60)                  #wait

        pygame.quit()

def update_ground(screen,ground_blocks):
        for ground in ground_blocks:
                ground.add_to_x_pos()                   #move block
                if ground.x_pos<-(ground.x_len):
                        ground_blocks.remove(ground)    #create a hole
                        
                ground.draw(screen)                     #draw ground

class Ground:
        
        def __init__(self,y_pos,x_pos,image_url,size):
              self.y_pos = y_pos
              self.x_pos = x_pos
              self.x_len = size
              self.image = pygame.image.load(image_url)
              self.image = pygame.transform.scale(self.image,(self.x_len, self.x_len))

        def draw(self,screen):
                screen.blit(self.image,(self.x_pos,self.y_pos))
                
        def add_to_x_pos(self,value=1):
                self.x_pos -= value


class Player:
        def __init__(self,y_pos,x_pos,x_size,y_size,image_path):
                
                self.y_pos = y_pos
                self.x_pos = x_pos

                self.jump_hight = y_pos-60
                self.in_air = False
                self.jump =  False
                
                self.x_size = x_size
                self.y_size = y_size
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image,(x_size,y_size))

        def check_jumping(self):
                                
                if self.jump:
                        self.y_pos -=1
                        if self.y_pos == self.jump_hight:
                                self.jump = False
                                self.in_air = True
                elif self.in_air:
                        self.y_pos +=1

        def draw(self,screen):
                screen.blit(self.image,(self.x_pos,self.y_pos))

        def set_jump(self):
                self.jump = True

        def reset_in_air(self):
                self.in_air = False

        

start_game()
