import numpy as np
from random import randrange as rr
from random import shuffle
from NeuralNetwork import NeuralNetwork
import Testgame
from collections import Counter
from tqdm import tqdm

def balance_data(array):
    counted_array = Counter([a[1][0] for a in array])
    while counted_array[1]< counted_array[0]:
        shuffle(array)
        for element in array:
            if element[1][0] == 0:
                array.remove(element)
                counted_array = Counter([a[1][0] for a in array])
                break
    return np.array(array)

def create_data(iterations):
    machine_game = Testgame.Game(True,False)
    game_info = [1,1,1,1]
    input_ = 0
    data = []
    for i in tqdm(range(iterations)):
        run,game_info = machine_game.start_machine_game([input_])
        if not run:
            break
        if game_info[1]:
            input_ = 1
        else:
            input_ = 0
        data.append([game_info,[input_]])
        
    machine_game.Quit()
    data = balance_data(data)
    return data


#data_name = "Test1.npy"
data_name = "maschine_created.npy"
#test_game = Testgame.Game(False,True,data_name)
#test_game.start_human_game()
data_array = np.load(data_name)[:400]
print(Counter([a[1][0] for a in data_array]))
    
X_es = np.array([data[0] for data in data_array])
Y_s = np.array([data[1] for data in data_array])
test_X = X_es[:100]
test_Y = Y_s[:100]
X = X_es[100:]
Y = Y_s[100:]

epochs = 10
steps = 1000
LR = 1e-3

NN = NeuralNetwork(4,[3,2],1,False,show_after_init=False)
input("start Training (Enter to continue)")
NN.train(X,Y,test_X,test_Y,LR,epochs,steps,0,visualize=True,tqdm_=False)

run = True
machine_game = Testgame.Game(True,False)
game_info = [1,1,1,1]
input("learning finished\nEnter for Start playing: ")
while run:
    input_ = NN.predict(game_info)
    run,game_info = machine_game.start_machine_game(input_)





