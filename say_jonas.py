import numpy as np
from random import randrange as rr
from NeuralNetwork import NeuralNetwork
import Testgame
from collections import Counter

data_name = "Test1.npy"
#test_game = Testgame.Game(False,True,data_name)
#test_game.start_human_game()
data_array = np.load(data_name)

print(Counter([a[1][0] for a in data_array]))
    
X = np.array([data[0] for data in data_array])
Y = np.array([data[1] for data in data_array])
test_X = X
test_Y = Y

epochs = 1000
steps = 10000
LR = 1e-2

NN = NeuralNetwork(4,[3,2],1,False,show_after_init=False)
print("start Training (Enter to continue)")
NN.train(X,Y,test_X,test_Y,LR,epochs,steps,0,visualize=True,tqdm_=False)

run = True
machine_game = Testgame.Game(True,False)
game_info = [1,1,1,1]
input("learning finished Enter for Start playing: ")
while run:
    input_ = NN.predict(game_info)
    run,game_info = machine_game.start_machine_game(input_)





