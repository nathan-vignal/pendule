import time
import tests
from tkinter import *
from math import *
import Pendule
import Display
import Graphique

class Simulation:

    def __init__(self, pendules, tempsEntreImages):
        self.listeDeplacement = []
        self.pendules = pendules
        self.tempsEntreImages = tempsEntreImages
        for pendule in pendules:
            if (pendule.T <= tempsEntreImages or tempsEntreImages <= 0):
                print('merci de ne pas faire n\'importe quoi et de mettre un temps entre image raisonable')

    def recap(self):
        for pendule in self.pendules:
            pendule.show()

    def simulate(self):
        for j in range(0, len(self.pendules), 1):
            self.listeDeplacement.append(self.pendules[j].simulate(self.tempsEntreImages))


    def show(self):

        display = Display.Display()
        display.display(self)
