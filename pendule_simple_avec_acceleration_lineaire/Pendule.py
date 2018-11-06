import time
import tests
from tkinter import *
from math import *

def createTranslation(tx, ty) :
    matrice = [[1, 0, tx], [0, 1, ty], [0, 0, 1]]
    return matrice

#récupère sois la valeur minimale sois la valeur max qu'a value le paramètre suivis(celui affiché dans le graphique)
def getextreme(liste, getMin):
    if(getMin):
        extremum = 9999999
    else:
        extremum = -99999
    for valeur in liste:
        if(valeur<extremum and getMin or valeur>extremum and not getMin):
            extremum = valeur

    return extremum


class Pendule:
    def __init__(self, name, g, l, theta, masse,color,k, origine='not defined'):
        self.name = name
        self.g = g
        self.l = l
        self.k = k #round(6*pi*(1/1000)*50,4)        #6*pi*(coeffvisqositémillieu)*rayonboule
        self.theta = round(theta,4)
        self.masse = masse
        self.T = 2 * pi * sqrt(self.l / self.g) * (1 + (self.theta * self.theta) / 16) # formule borda
        self.color = color
        self.listeGraph = []
        self.valeurGraphMin = 0
        self.valeurGraphMax = 0
        self.deltaExtremum = 0
        if origine == 'not defined':  # permet un parametre par défaut pour origine en fonction de l
            self.origine = (0, l)
        else:
            self.origine = (origine,l)

    #affiche dans le terminale les infos du pendule
    def show(self):
        print('----' + self.name + '----')
        print('g = ' + str(self.g) + 'm/s^2')
        print('l = ' + str(self.l))
        print('theta = ' + str(self.theta))
        print('masse = ' + str(self.masse) + 'Kg')
        print('k = ' + str(self.k))
        print
        print

    # MatriceA * MatriceB
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


    #fait une rotation par rapport à la fixation du pendule
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


    #calcul toute les positions du pendule tant qu'il a un minimum de vitesse
    def simulate(self, tempsEntreImages, ):  # but : renvoyer une liste avec les positions en fonctions du temps


        actualTheta = self.theta
        previousTheta = actualTheta

        #upperTheta représente le theta à chaque fin d'un aller (ex: pi/2 au début puis -pi/2-frottement)
        upperTheta = actualTheta
        upperPreviousTheta = 9999


        # calcul premiere position
        liste = [[self.origine[0]+ sin(actualTheta)* self.l , (self.origine[1] - cos(actualTheta)* self.l) , 1]]
        # initialise le booléen :(pendule à droite) du coté opposé pour des raisons de programme
        if (liste[len(liste) - 1][0] > self.origine[0]):
            penduleADroite = 0
        else:
            penduleADroite = 1
        # tant que le pendule bouge encore à une vitesse
        while (1):
            print('début')
            # gestion de la fin du bloc aller (dépend du coté du pendule)
            if (liste[len(liste) - 1][0] > self.origine[0]): #si le pendule est à droite
                if(penduleADroite):   # est qu'il était déjà à droite
                    break  #arrête la simulation
                penduleADroite = 1
            else:                       #même chose coté gauche
                if (not penduleADroite):
                    break
                penduleADroite = 0

            upperPreviousTheta = upperTheta
            actualTheta = upperTheta
            ########## bloc gérant un aller#############
            temps = tempsEntreImages
            vitesse = 0
            i = 0
            while (1) :
                # vitesse  =  vitesse + accélération * temps entre image
                vitesse += (-((self.g / self.l) * sin(actualTheta)) - (self.k / (self.masse * (
                        self.l * self.l))) * vitesse) * tempsEntreImages
                #nouvel angle = ancien angle + vitesseAngulaire * temps entre images
                actualTheta += vitesse * tempsEntreImages
                #delta est la rotation a effectué pour avoir la nouvelle position du pendule
                delta = actualTheta - previousTheta
                previousTheta = actualTheta

                temps += tempsEntreImages
                #si la vitesse relativement petite  (par rapport au temps entre image et à la longeur du cable) en fonction du côté
                # car la vitesse est négative de droite à gauche, et l'opposé de gauche à droite: la vitesse angulaire est dans le sens trigonométrique
                if (not (((vitesse <= -0.05*tempsEntreImages/self.l) and penduleADroite) or ((vitesse > 0.05*tempsEntreImages/self.l) and (not penduleADroite)))):
                    upperTheta = actualTheta
                    break
                else:
                    #si la vitesse est assé grande on rajoute la position du pendule à la liste des position
                    liste.append(self.rotate(delta, [liste[len(liste) - 1]]))# nouvelle position = ancienne tourné de la différence d'angle entre les deux, par rapport à la fixation


                    self.listeGraph.append(vitesse)
            ########## fin bloc gérant un aller#############





        #après avoir calculer toute les positions de pendule
        #récupère les extrème des valeurs à affiché sur le graphique
        self.valeurGraphMin = getextreme(self.listeGraph, 1)
        self.valeurGraphMax = getextreme(self.listeGraph, 0)
        self.deltaExtremum = self.valeurGraphMax - self.valeurGraphMin
        #on renvoie toute les positions
        return liste