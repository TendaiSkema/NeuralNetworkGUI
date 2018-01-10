import pygame
from random import randrange as rand
from random import shuffle
import numpy as np
from collections import Counter

class Game:
        def __init__(self,is_machine,do_save,save_name=None):
                pygame.init()
                self.is_machine = is_machine
                self.score = 0
                self.last_block_not_solid = False
                self.do_save = do_save
                self.save_name = save_name

                #init all screen vars
                self.screen_with = 800                       #screen with
                self.screen_hight = 600                      #screen height
                self.screen_home_color = (255,255,255)       #main default background (white)
                self.screen = pygame.display.set_mode((self.screen_with, self.screen_hight))   #set screen to size screen with*screen height
                #background image
                self.background_img = pygame.image.load("Game_pics/GameBackground.jpg") #load
                self.background_img = pygame.transform.scale(self.background_img,(self.screen_with, self.screen_hight))
                self.screen.blit(self.background_img,(0,0)) #add to screen

                #create gametimer
                self.clock = pygame.time.Clock()

                #ground
                self.block_size = 60
                self.counter = self.block_size
                self.ground_level = self.screen_hight*0.8
                self.ground_image_path = "Game_pics/Brick.jpg"
                self.ground_blocks = [Ground(self.ground_level,i-1,self.ground_image_path,self.block_size,True) for i in range(0,self.screen_with,self.block_size)]

                #player
                self.player_x_size = 40
                self.player_y_size = 55
                self.player_jump_speed = 3
                self.player_image_path = "Game_pics/player_mario.png"
                self.player = Player(self.screen_hight,self.player_jump_speed,self.ground_level-self.player_y_size,100,self.player_x_size,self.player_y_size,self.player_image_path)
                
        def start_human_game(self):
                last_block_not_solid = False
                save_array = []
                #start gameloop
                run = True
                while run:
                        self.screen.blit(self.background_img,(0,0)) #reshow background
                        self.score += 1
                        
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        run = False

                        #get key events
                        pressed = pygame.key.get_pressed()
                        if pressed[pygame.K_SPACE] and not self.player.in_air:
                                self.player.set_jump()

                         #ground updating AND hole creation
                        if not self.counter:
                                rand_value = rand(0,4)
                                if rand_value > 0 or last_block_not_solid:
                                        new_ground = Ground(self.ground_level,self.screen_with-1,self.ground_image_path,self.block_size,True)
                                        self.ground_blocks.append(new_ground)
                                        self.counter = self.block_size
                                        last_block_not_solid = False
                                elif not last_block_not_solid:
                                        new_ground = Ground(self.ground_level,self.screen_with-1,self.ground_image_path,self.block_size,False)
                                        self.ground_blocks.append(new_ground)
                                        self.counter = self.block_size
                                        last_block_solid = True
                        else:
                                self.counter -=2
                                

                        #player updating
                        self.update_ground()
                        self.check_kollision()
                        self.player.check_jumping()
                        
                        if not self.player.alive:
                                run = False
                                
                        self.player.draw(self.screen)

                        #final updates
                        pygame.display.update()         #update all
                        if self.do_save:
                                game_infos = self.binary_interpreter()
                                save_array.append([game_infos,[pressed[pygame.K_SPACE]]])
                        self.clock.tick(60)                  #wait
                        
                np.save(self.save_name,np.array(self.balance_data(save_array[200:-10]))) #save full game
                pygame.quit()

        def start_machine_game(self,input_): #inpud designe [jump(1,0)]
                #start gameloop
                run = True
                self.screen.blit(self.background_img,(0,0)) #reshow background
                self.score += 1
                        
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                        run = False

                #input
                if input_[0] and not self.player.in_air:
                        self.player.set_jump()

                #ground updating AND hole creation
                if not self.counter:
                        rand_value = rand(0,6)
                        if rand_value > 0 or self.last_block_not_solid:
                                new_ground = Ground(self.ground_level,self.screen_with-1,self.ground_image_path,self.block_size,True)
                                self.ground_blocks.append(new_ground)
                                self.counter = self.block_size
                                self.last_block_not_solid = False
                        elif not self.last_block_not_solid:
                                new_ground = Ground(self.ground_level,self.screen_with-1,self.ground_image_path,self.block_size,False)
                                self.ground_blocks.append(new_ground)
                                self.counter = self.block_size
                                self.last_block_solid = True
                else:
                        self.counter -=2
                                

                        #player updating
                self.update_ground()
                self.check_kollision()
                self.player.check_jumping()
                        
                if not self.player.alive:
                        run = False
                        pygame.quit()
                        return run,None
                                
                self.player.draw(self.screen)

                #final updates
                pygame.display.update()         #update all
                return run,self.binary_interpreter()

        def update_ground(self):
                for ground in self.ground_blocks:
                        ground.add_to_x_pos(2)           #move block
                        if ground.x_pos<-(2*ground.x_len):
                                self.ground_blocks.remove(ground)    #delete last ground block
                        if ground.solid:
                                ground.draw(self.screen)                     #draw ground

        def check_kollision(self):
                p_box = self.player.get_hitbox()             #{x min,x max,y min, y max} Dix
                p_in_air = True
                for ground in self.ground_blocks:
                        if ground.solid:
                                g_box = ground.get_hitbox()
                                if p_box["y_max"]== g_box["y_min"] or (p_box["y_max"]<= g_box["y_min"]+5 and p_box["y_max"] > g_box["y_min"]):
                                        if p_box["x_min"]>=g_box["x_min"] and p_box["x_max"]<=g_box["x_max"]:
                                                p_in_air = False
                                                break
                                        elif p_box["x_min"]<=g_box["x_min"] and p_box["x_max"]<=g_box["x_max"] and p_box["x_max"]>=g_box["x_min"]:
                                                p_in_air = False
                                                break

                                        elif p_box["x_min"]>=g_box["x_min"] and p_box["x_max"]>=g_box["x_max"] and p_box["x_min"]<=g_box["x_max"]:
                                                p_in_air = False
                                                break
                self.player.set_in_air(p_in_air)

        def binary_interpreter(self):
                binarry_array = []
                for gnd in self.ground_blocks[2:6]:
                        binarry_array.append(int(not gnd.solid))
                return binarry_array

        def balance_data(self,array):
                counted_array = Counter([a[1][0] for a in array])
                while counted_array[1]< counted_array[0]:
                        shuffle(array)
                        for element in array:
                                if element[1][0] == 0:
                                        array.remove(element)
                                        counted_array = Counter([a[1][0] for a in array])
                                        break
                return array
        def Quit(self):
                pygame.quit()
                                
class Ground:
        
        def __init__(self,y_pos,x_pos,image_path,size,solid):
              self.y_pos = y_pos
              self.x_pos = x_pos
              self.x_len = size
              self.solid = solid
              self.image = pygame.image.load(image_path)
              self.image = pygame.transform.scale(self.image,(self.x_len, self.x_len))

        def draw(self,screen):
                screen.blit(self.image,(self.x_pos,self.y_pos))
                
        def add_to_x_pos(self,value=1):
                self.x_pos -= value

        def get_hitbox(self):
                x_min = self.x_pos
                x_max = self.x_pos+self.x_len
                
                y_min = self.y_pos
                y_max = self.y_pos-self.x_len

                return {"x_min":x_min,"x_max":x_max,"y_min":y_min,"y_max":y_max}

class Player:
        def __init__(self,screen_hight,jump_speed,y_pos,x_pos,x_size,y_size,image_path):
                
                self.y_pos = y_pos
                self.x_pos = x_pos
                self.die_point = screen_hight

                self.jump_hight = y_pos-100
                self.jump_speed = jump_speed
                self.in_air = False
                self.jump =  False
                self.alive = True
                
                self.x_size = x_size
                self.y_size = y_size
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image,(x_size,y_size))

        def check_jumping(self):
                                
                if self.jump:
                        self.y_pos -= self.jump_speed*(self.y_pos/(self.jump_hight))
                        if self.y_pos <= self.jump_hight:
                                self.jump = False
                                self.in_air = True
                elif self.in_air:
                        self.y_pos += self.jump_speed*(self.y_pos/self.jump_hight)
                if self.y_pos > self.die_point:
                        self.alive = False

        def draw(self,screen):
                screen.blit(self.image,(self.x_pos,self.y_pos))

        def set_jump(self):
                self.jump = True

        def set_in_air(self,boolean):
                self.in_air = boolean

        def get_hitbox(self):
                x_min = self.x_pos
                x_max = self.x_pos+self.x_size
                
                y_min = self.y_pos
                y_max = self.y_pos+self.y_size

                return {"x_min":x_min,"x_max":x_max,"y_min":y_min,"y_max":y_max}


#game = Game(False,True,"Test1.npy")
#game.start_human_game()
