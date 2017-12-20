import numpy as np
from random import randrange as rr
from NeuralNetwork import NeuralNetwork

def create_data(value):
    X = []
    Y = []
    for i in range(value):
        x1 = rr(0,10)
        x2 = rr(0,10)

        if x1<x2:
            X.append([x1,x2])
            Y.append([0,1])
        else:
            X.append([x1,x2])
            Y.append([1,0])

    return np.array(X),np.array(Y)

def create_linear_data(value):
    X = []
    Y = []
    for i in range(value):
        x1 = rr(0,10)
        x2 = rr(0,10)

        X.append([x1,x2])
        Y.append([x1+x2])
    return np.array(X),np.array(Y)

NN = NeuralNetwork(2,[3,6,3],2,True)

X,Y = create_data(1000)
test_X,test_Y = create_data(100)

#X2,Y2 = create_linear_data()

epochs = 5
steps = 2500
LR = 1e-3

NN.train(X,Y,test_X,test_Y,LR,epochs,steps,0,True)



