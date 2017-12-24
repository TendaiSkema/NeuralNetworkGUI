import numpy as np
from PyQt4 import QtGui

class window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init_()
        self.setGeometrie(50,50,800,600)
        self.show()

