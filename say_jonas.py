import numpy as np
from random import randrange as rr
from NeuralNetwork import NeuralNetwork

def get_letter(array):
    letters = [" ","J","o","n","a","s"]
    for i in range(len(letters)):
        if array[i] >0.9:
            return letters[i]

def create_data():
    X = [
        [1,0,0,0,0,0],
        [0,1,0,0,0,0],
        [0,0,1,0,0,0],
        [0,0,0,1,0,0],
        [0,0,0,0,1,0],
        [0,0,0,0,0,1],
        ]
    
    Y = [
        [0,1,0,0,0,0],
        [0,0,1,0,0,0],
        [0,0,0,1,0,0],
        [0,0,0,0,1,0],
        [0,0,0,0,0,1],
        [1,0,0,0,0,0],
        ]
    
    return np.array(X),np.array(Y)

NN = NeuralNetwork(6,[12,24,12],6,False,show_after_init=False)

X,Y = create_data()
test_X,test_Y = create_data()

epochs = 100
steps = 5000
LR = 1e-3

NN.train(X,Y,test_X,test_Y,LR,epochs,steps,0,visualize=True,tqdm_=False)




