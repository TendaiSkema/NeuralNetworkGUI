import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

class Visualizer:
    def __init__(self,live_vew=False,epochs=None,steps=None,in_size=None,layer_size=None,out_size=None):
        self.losses = []
        self.accs = []
        
        if live_vew:

            self.epochs = epochs

            style.use("dark_background")
            self.Network = plt.subplot2grid((7,2),(0,0),rowspan=4,colspan=2)
            self.Network.set_title('Neuronen')
            self.show_network(in_size,layer_size,out_size)
            
                                    #gridsize,stardingpoint,rowspan,columnspan
            self.acc_graph = plt.subplot2grid((7,2),(5,0),colspan=1,rowspan=2)
            self.acc_graph.set_title("Accuracy")
            self.acc_graph.axis([0,epochs,0,1])
            plt.ion()

            self.loss_graph = plt.subplot2grid((7,2),(5,1),colspan=1,rowspan=2)
            self.loss_graph.set_title("Loss")
            self.loss_graph.axis([0,epochs,0,5])
            plt.ion()


    def animat_graph(self,epoch,steps,acc,loss):
        self.acc_graph.scatter(epoch, acc,s=[5,5],c="b")
        self.accs.append(acc)
        self.losses.append(loss)
        self.loss_graph.axis([0,self.epochs,0,self.losses[0]])
        self.loss_graph.scatter(epoch, loss,s=[5,5],c="r")
        plt.pause(0.005)
        
    def show_graph(self,epoch,steps):
        iterations = epoch*steps
        x_values_loss = range(iterations)
        x_values_acc = []
        for x_value in range(epoch):
            x_values_acc.append(x_value*steps)

        loss_graph = plt.plot(x_values_loss,self.losses,"r-")
        acc_graph = plt.plot(x_values_acc,self.accs,"b-")
        plt.show()

    def show_network(self,input_size,layers,output_size):
        #------------------offset berechnung------------------
        max_layer_size = input_size
        for i in layers:
            if max_layer_size < i:
                max_layer_size = i
        if output_size > max_layer_size:
            max_layer_size = output_size
        middline = (max_layer_size/2)+1
        #-------------------Array erstellung-------------------
        hole_network = []
        x_values = []
        offset = middline-(input_size/2)
        for i in range(1,input_size+1):
            hole_network.append(i+offset)
            x_values.append(1)
        layer_index = 1
        for layer in layers:
            layer_index+=1
            offset = middline-(layer/2)
            for i in range(1,layer+1):
                hole_network.append(i+offset)
                x_values.append(layer_index)
        layer_index+=1
        offset = middline-(output_size/2)
        for i in range(1,output_size+1):
            hole_network.append(i+offset)
            x_values.append(layer_index)
        #----------------------Anzeigen------------------------
        self.Network = plt.scatter(x_values,hole_network,c="g",s=[20,20])
