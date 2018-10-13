import time
import tests
from tkinter import *
from math import *
def createTranslation(tx, ty) :
    matrice = [[1, 0, tx], [0, 1, ty], [0, 0, 1]]
    return matrice

class Pendule:
    def __init__(self, name, g, l, theta, masse,color, origine='not defined'):
        self.name = name
        self.g = g
        self.l = l
        self.theta = theta
        self.masse = masse
        self.T = 2 * pi * sqrt(self.l / self.g) * (1 + (self.theta * self.theta) / 16)
        self.color = color
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



    def rotate(self, t, dernierCoordonne,):
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
        liste = [[self.origine[0]+sin(actualTheta) * self.l, (self.l - cos(actualTheta)) * self.l, 1]]
        if (liste[len(liste) - 1][0] > 0):   #initialise pendule à droite du coté opposé
            penduleADroite = 0
        else:
            penduleADroite = 1
        while (abs(upperPreviousTheta - upperTheta) > 0.01):
            print(self.name)
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
        return liste