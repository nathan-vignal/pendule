import time
import tests
from tkinter import *
from math import *
import Pendule
import Display
import Graphique

class Simulation:

    def __init__(self, pendules, tempsEntreImages):
        # Liste qui va accueillir la liste de déplacement de chaque pendule
        self.listeDeplacement = []
        #liste des pendules de la simulation
        self.pendules = pendules
        self.tempsEntreImages = tempsEntreImages

        # On vérifie que pour chaque pendules le temps de faire un aller n'est pas inférieur au temps entre images
        for pendule in pendules:
            if (pendule.T/2 <= tempsEntreImages or tempsEntreImages > 0):
                print('merci de ne pas faire n\'importe quoi et de mettre un temps entre image raisonable')

    # Affiche les infos des pendules de la simulation
    def recap(self):
        for pendule in self.pendules:
            pendule.show()

    # Calcule tous les déplacements de chaque pendules
    def simulate(self):
        for j in range(0, len(self.pendules), 1):
            self.listeDeplacement.append(self.pendules[j].simulate(self.tempsEntreImages))

    # Affiche l'animation
    def show(self):
        display = Display.Display()
        display.display(self)