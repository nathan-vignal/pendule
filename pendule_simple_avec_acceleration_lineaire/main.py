import time
from tkinter import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import *
def createTranslation(tx, ty) :
    matrice = [[1, 0, tx], [0, 1, ty], [0, 0, 1]]
    return matrice

class Pendule:
    def __init__(self, name, g, l, theta, masse, origine='not defined'):
        self.name = name
        self.g = g
        self.l = l
        self.theta = theta
        self.masse = masse
        self.T = 2 * pi * sqrt(self.l / self.g) * (1 + (self.theta * self.theta) / 16)
        if origine == 'not defined':  # permet un parametre par défaut pour origine en fonction de l
            self.origine = (0, l)
        else:
            self.origine = (origine,l)

    def show(self):
        print('----' + self.name + '----')
        print('g = ' + str(self.g) + 'm/s^2')
        print('l = ' + str(self.l))
        print('theta = ' + str(self.theta))
        print('masse = ' + str(self.masse) + 'Kg')
        print
        print

    def multiplication(MatriceA, MatriceB):
        matriceC = [[0]*(len(MatriceB[0]))]

        if len(MatriceA) != len(MatriceB[0]):
            print('Impossible de multiplier les deux matrices')
            return

        for i in range(len(MatriceB)):
            for j in range(len(MatriceA[0])):
                for k in range(len(MatriceA)):
                    matriceC[i][j] += MatriceB[i][k] * MatriceA[j][k]
        return matriceC



    def rotate(self, t, dernierCoordonne):
        # parametre

        translation = [[1, 0, -self.origine[0]],
                       [0, 1, -self.origine[1]],
                       [0, 0, 1]]
        dernierCoordonne = Pendule.multiplication(translation, dernierCoordonne)

        rotation = [[cos(t), -sin(t),0], [sin(t), cos(t),0], [0,0,1]]
        dernierCoordonne = Pendule.multiplication(rotation, dernierCoordonne)

        translation = [[1, 0,   self.origine[0]],
                       [0, 1,   self.origine[1]],
                       [0, 0, 1]]
        dernierCoordonne  = Pendule.multiplication( translation,dernierCoordonne)
        return dernierCoordonne[0]



    def simulate(self, tempsEntreImages, ):  # but : renvoyer une liste avec les positions en fonctions du temps

        actualTheta = self.theta
        previousTheta = actualTheta
        upperTheta = actualTheta
        upperPreviousTheta = 9999

        # premiere position
        liste = [[sin(actualTheta) * self.l, (1 - cos(actualTheta)) * self.l, 1]]
        if (liste[len(liste) - 1][0] > 0):   #initialise pendule à droite du coté opposé
            penduleADroite = 0
        else:
            penduleADroite = 1
        while (abs(upperPreviousTheta - upperTheta) > 0.01):

            # BLOC ALLER
            if (liste[len(liste) - 1][0] > 0):
                if(penduleADroite):
                    break
                penduleADroite = 1
            else:
                if (not penduleADroite):
                    break
                penduleADroite = 0

            upperPreviousTheta = upperTheta
            actualTheta = upperTheta
            temps = tempsEntreImages
            vitesse = 0
            while (1) :
                vitesse += ((-((self.g / self.l) * sin(actualTheta)) - (0.1/ (self.masse * (
                        self.l * self.l))) * vitesse) * tempsEntreImages)  # la valeur en dur est k le coefficient de frottement
                actualTheta += vitesse * tempsEntreImages
                delta = actualTheta - previousTheta
                previousTheta = actualTheta

                temps += tempsEntreImages
                if (not (((vitesse <= -0.5*tempsEntreImages) and penduleADroite) or ((vitesse > 0.5*tempsEntreImages) and (not penduleADroite)))):
                    upperTheta = actualTheta
                    break
                else:
                    liste.append(self.rotate(delta, [liste[len(liste) - 1]]))
        #animation boule



        # FIN BLOC ALLER
        print(len(liste))
        return liste


class Simulation:
    listeDeplacement = []

    def __init__(self, pendules, tempsEntreImages):
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
        #settings
        width = 1200
        height= 800
        decalageX = width*0.5
        decalageY = height*0.75
        size = 30
        zoom = 200
        main = Tk()
        main.geometry("1200x800+220+100")
        main.title("Pendule")
        canvas = Canvas(main, width=width, height=height)
        canvas.pack()
        for k in range(0, len(self.pendules), 1):
            origineX = self.pendules[k].origine[0]
            origineY = self.pendules[k].origine[1]
            fixation = canvas.create_oval(origineX*zoom +decalageX,
                                          -origineY*zoom +decalageY,
                                          origineX*zoom+size/1.5 +decalageX,
                                          -origineY*zoom+size/1.5 +decalageY)
            canvas.update()
            for i in range(0, len(self.listeDeplacement[k]) - 1, 1):
                point = canvas.create_oval(self.listeDeplacement[k][i][0] * zoom + decalageX,
                                           -self.listeDeplacement[k][i][1] * zoom + decalageY,
                                           self.listeDeplacement[k][i][0] * zoom + decalageX + size,
                                           -self.listeDeplacement[k][i][1] * zoom + decalageY + size,
                                           fill="black")

                lien = canvas.create_line(
                    ((origineX * zoom + decalageX) + (origineX * zoom + size / 1.5 + decalageX)) / 2
                    # moyenne entre les opposé de l'elipse pour avoir le centre
                    ,
                    ((-origineY * zoom + decalageY) + (-origineY * zoom + size / 1.5 + decalageY)) / 2
                    ,
                    (self.listeDeplacement[k][i][0] * zoom + decalageX +  # centre du pendule
                     self.listeDeplacement[k][i][0] * zoom + decalageX + size) / 2
                    ,
                    (-self.listeDeplacement[k][i][1] * zoom + decalageY +
                     -self.listeDeplacement[k][i][1] * zoom + decalageY + size) / 2)
                canvas.update()
                time.sleep(0.01)
                canvas.delete(point)
                canvas.delete(lien)
            canvas.delete(fixation)


        main.mainloop()


#https://brushingupscience.com/2016/06/21/matplotlib-animations-the-easy-way/



# print(point(self.listeDeplacement[k]))
#animation = animate([point(j) for j in self.listeDeplacement[0]], xmin=-1.1, xmax=1.1, ymin=-1.1, ymax=1.1)
#animation.show()


# création des pendules
# name, g, l, theta, masse, origine=(0,l)):
terre = Pendule('terre', 9.81, 3, pi / 2 , 1)
mars = Pendule('terre', 3.711, 1, pi / 2, 1)
# création de la simulation
simulation = Simulation([terre,mars], 0.0001)

simulation.recap()
simulation.simulate()
simulation.show()
