import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

class Visualizer:
    def __init__(self):
        self.losses = []
        self.accs = []
        self.x_values = []

    def animat_graph(self,i):
        
        if len(self.x_values)>10:
            xs = self.x_values[-10:]
            acc_ys = self.accs[-10:]
            loss_ys = self.losses[-10:]
            
        else:
            xs = self.x_values
            acc_ys = self.accs
            loss_ys = self.losses
        
        self.acc_graph.clear()
        self.loss_graph.clear()
        
        self.acc_graph.plot(xs, acc_ys,"b-")
        self.loss_graph.plot(xs, loss_ys,"r-")

    def save_animat_graph(self,epoch,acc,loss):
        self.losses.append(loss)
        self.accs.append(acc)
        self.x_values.append(epoch)

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

    def start_animation(self,epochs,steps,in_size,layer_size,out_size):
        
        self.epochs = epochs
        style.use("dark_background")

        fig = plt.figure()
            
        self.Network = fig.add_subplot(212)
        self.Network.set_title('Neuronen')
        self.show_network(in_size,layer_size,out_size)
            
                                    #gridsize,stardingpoint,rowspan,columnspan
        self.acc_graph = fig.add_subplot(222)
        self.acc_graph.set_title("Accuracy")

        self.loss_graph = fig.add_subplot(221)
        self.loss_graph.set_title("Loss")

        ani = animation.FuncAnimation(fig, self.animat_graph, interval=1000)
        plt.show()
