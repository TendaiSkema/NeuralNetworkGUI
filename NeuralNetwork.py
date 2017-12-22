import numpy as np
from random import randrange as rr
from Network_Visualizer import Visualizer
from time import time
from tqdm import tqdm

class NeuralNetwork:
    def __init__(self,in_size,layer_size,out_size,init_with_zeros=False,show_after_init=True):
        self.in_size = in_size
        self.layer_size = layer_size
        self.out_size = out_size
        
        self.z = []
        self.a = []
        self.w = []

        w_in = []
        for i in range(in_size):
            columns = []
            for j in range(layer_size[0]):
                weight = (rr(-100,100)/100)*(not init_with_zeros)
                columns.append(weight)
            w_in.append(columns)
        self.w.append(np.array(w_in))

        w_mid = []
        for i in range(len(layer_size)-1):
            w_mid = []
            for k in range(layer_size[i]):
                columns = []
                for j in range(layer_size[i+1]):
                    weight = (rr(-100,100)/100)*(not init_with_zeros)
                    columns.append(weight)
                w_mid.append(columns)
            self.w.append(np.array(w_mid))

        w_out = []
        for i in range(layer_size[-1]):
            columns = []
            for j in range(out_size):
                weight = (rr(-100,100)/100)*(not init_with_zeros)
                columns.append(weight)
            w_out.append(columns)
        self.w.append(np.array(w_out))

    def sig(self,z):
        return 1/(1+np.exp(-z))
    
    def sigmoidPrime(self,z):
        return np.exp(-z)/((1+np.exp(-z))**2)

    def forward(self,inputs):
        self.z = []
        self.a = []
        
        self.z.append(np.dot(inputs,self.w[0]))
        self.a.append(np.array(self.sig(self.z[0])))

        for i in range(1,len(self.layer_size)):
            self.z.append(np.dot(self.a[i-1],self.w[i]))
            self.a.append(self.sig(self.z[i]))
        self.z.append(np.dot(self.a[-1],self.w[-1]))
        yHat = self.sig(self.z[-1])
        return np.array(yHat)

    def Cost(self,Y,yHat):
        J = np.sum(0.5*(Y-yHat)**2)
        return J

    def jump_over(self,j,value):
        if j<value:
            return False
        return True

    def costFunction(self,X,Y,yHat):
        dJw = []
        delta = []
        delta.append(np.multiply(-(Y-yHat),self.sigmoidPrime(self.z[-1])))
        dJw.append(np.dot(self.a[-1].T,delta[0]))
        
        for i in range(1,len(self.layer_size)):
            delta.append(np.dot(delta[-1],np.array(self.w[-i]).T)*self.sigmoidPrime(self.z[-(i+1)]))
            dJw.append(np.dot(self.a[-(i+1)].T,delta[-1]))
            
        delta.append(np.dot(delta[-1],np.array(self.w[1]).T)*self.sigmoidPrime(self.z[0]))
        dJw.append(np.dot(X.T,delta[-1]))

        return dJw

    def fit(self,dJw,LR):
        for  i in range(len(self.w)):
            self.w[i] = self.w[i]-LR*dJw[-(i+1)]

    def predict(self,X):
        out = self.forward(X)
        return out

    def get_acc(self,test_x,test_y):
        preds = self.forward(test_x)
        score = 0
        for i in range(len(preds)):
            pred = np.around(preds[i],1)
            try:
                if pred[0] == test_y[i][0]:
                    score +=1
                return score/len(test_y)
            except:
                print(len(pred),len(test_y))
                print("pred:{}, test_y:{}".format(pred,test_y))
                return 404

    def save(self,model_name):
        np.save('{}'.format(model_name),(self.w))
        return True

    def load_model(self,model_name):
        self.w = np.load('{}.npy'.format(model_name))
        return True

    def train(self,X,Y,test_x,test_y,LR=0.001,epochs=10,steps=2500,jump_value=0,visualize=False,tqdm_=False):
        if visualize:
            vr = Visualizer(True,epochs,steps,self.in_size,self.layer_size,self.out_size)

        print('----------------------------------------------------')
        
        for i in range(1,epochs+1):
                s_time = time()
                last_loss = 0
                
                if tqdm_:
                    for j in range(steps):
                        yHat = self.forward(X)
                        last_loss = self.Cost(Y,yHat)
                            
                        if jump_value>0:
                            if not self.jump_over(last_loss,jump_value):
                                dJw = self.costFunction(X,Y,yHat)
                                self.fit(dJw,LR)
                        else:
                            dJw = self.costFunction(X,Y,yHat)
                            self.fit(dJw,LR)
                            
                else:
                    for j in range(steps):
                        yHat = self.forward(X)
                        last_loss = self.Cost(Y,yHat)
                        
                        if jump_value>0:
                            if not self.jump_over(last_loss,jump_value):
                                dJw = self.costFunction(X,Y,yHat)
                                self.fit(dJw,LR)
                        else:
                            dJw = self.costFunction(X,Y,yHat)
                            self.fit(dJw,LR)
            
                acc = self.get_acc(test_x,test_y)
                if visualize:
                    vr.animat_graph(i,steps,acc,last_loss)
                print('Epoch: {}, time: {}ms, state: {}%'.format(i,round(time()-s_time,6),int((i/epochs)*100)))
                print('NN1 loss: {}, acc: {}'.format(round(last_loss,7),round(acc,7)))
                print('----------------------------------------------------')
                
