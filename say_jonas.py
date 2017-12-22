import numpy as np
from random import randrange as rr
from NeuralNetwork import NeuralNetwork
import Testgame

data_name = "Test1.npy"
test_game = Testgame.Game(False,True,data_name)
test_game.start_human_game()
data_array = np.load(data_name)

zeros = 0
ones = 0
for i in data_array:
    if i[1]:
        ones+=1
    else:
        zeros+=1
print("0:{}, 1:{}".format(zeros,ones))
    
X = np.array([data[0] for data in data_array])
Y = np.array([data[1] for data in data_array])
test_X = X
test_Y = Y

epochs = 100
steps = 2500
LR = 1e-3

NN = NeuralNetwork(4,[12,24,12],1,False,show_after_init=False)
NN.train(X,Y,test_X,test_Y,LR,epochs,steps,0,visualize=True,tqdm_=True)






