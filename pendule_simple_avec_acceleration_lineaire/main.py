import time
from tkinter import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import *
def createTranslation(tx, ty) :
    matrice = [[1,0,0],[0,1,0],[tx,ty,1]]
    return matrice

class Pendule:
    def __init__(self, name, g, l, theta, masse, origine='not defined'):
        self.name = name
        self.g = g
        self.l = l
        self.theta = theta
        self.masse = masse
        self.T = 2 * pi * sqrt(self.l / self.g) * (1 + (self.theta * self.theta) / 16)
        self.deplacement = [(sin(self.theta) * self.l, (1 - cos(self.theta)) * self.l)]
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

    def multiplication(self, matrix, Coordonne):
        result = (matrix[0][0] * Coordonne[0] + matrix[0][1] * Coordonne[1]), (
                matrix[1][0] * Coordonne[0] + matrix[1][1] * Coordonne[1])
        return result

    def rotate(self, t, dernierCoordonne):
        # parametre
        dernierCoordonne = (dernierCoordonne[0] - self.origine[0],
                            dernierCoordonne[1] - self.origine[1])  # coordonne par rapport à l'origine du pendule
        rotation = [((cos(t)), (-sin(t))), ((sin(t)), (cos(t)))]
        result = self.multiplication(rotation, dernierCoordonne)
        result = ((result[0] - self.origine[0]),
                  (result[1] + self.origine[1]), 1)  ##coordonne par rapport à l'origine du graphique
        return result
    #def tranlation(self,tx,ty):



    def simulate(self, tempsEntreImages, ):  # but : renvoyer une liste avec les positions en fonctions du temps

        actualTheta = self.theta
        previousTheta = actualTheta
        upperTheta = actualTheta
        upperPreviousTheta = 9999

        # premiere position
        liste = [(0, 0,1)]
        liste[0] = (sin(actualTheta) * self.l, (1 - cos(actualTheta)) * self.l, 1)
        while (abs(upperPreviousTheta - upperTheta) > 0.1):
            # BLOC ALLER
            if (liste[len(liste) - 1][0] > 0):
                penduleADroite = 1
            else:
                penduleADroite = 0

            upperPreviousTheta = upperTheta
            actualTheta = upperTheta
            temps = tempsEntreImages
            vitesse = 0
            while (1) :
                vitesse += ((-((self.g / self.l) * sin(actualTheta)) - (1 / (self.masse * (
                        self.l * self.l))) * vitesse) * tempsEntreImages)  # la valeur en dur est k le coefficient de frottement
                actualTheta += vitesse * tempsEntreImages
                delta = actualTheta - previousTheta
                previousTheta = actualTheta

                temps += tempsEntreImages
                if (not (((vitesse <= 0) and penduleADroite) or ((vitesse >= 0) and (not penduleADroite)))):
                    upperTheta = actualTheta
                    break
                else:
                    liste.append(self.rotate(delta, liste[len(liste) - 1]))
        #animation boule



            # FIN BLOC ALLER

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
        zoom = 150
        main = Tk()
        main.geometry("1200x800+220+100")
        main.title("Pendule")
        canvas = Canvas(main, width=width, height=height)
        canvas.pack()
        for k in range(0, len(self.pendules), 1):
            origineX = self.listeDeplacement[k][0][0]+cos(-2*self.pendules[k].theta)*self.pendules[k].l
            origineY = self.listeDeplacement[k][0][1]+sin(-2*self.pendules[k].theta)*self.pendules[k].l
            fixation = canvas.create_oval(origineX*zoom +decalageX,
                               -origineY*zoom +decalageY,
                               origineX*zoom+size/1.5 +decalageX,
                               -origineY*zoom+size/1.5 +decalageY)
            canvas.update()
            time.sleep(1)
        for k in range(0, len(self.pendules), 1):

            for i in range(0, len(self.listeDeplacement[k])-1, 1):
                point = canvas.create_oval(self.listeDeplacement[k][i][0] * zoom +decalageX,
                                              -self.listeDeplacement[k][i][1] * zoom +decalageY,
                                              self.listeDeplacement[k][i][0] * zoom + decalageX + size,
                                              -self.listeDeplacement[k][i][1] * zoom + decalageY + size,
                                              fill="black")

                lien = canvas.create_line((origineX*zoom +decalageX+origineX*zoom+size/1.5 +decalageX)/2 ,
                                          (-origineY*zoom +decalageY+-origineY*zoom+size/1.5 +decalageY)/2,
                                          (self.listeDeplacement[k][i][0] * zoom +decalageX +
                                          self.listeDeplacement[k][i][0] * zoom + decalageX + size)/2,
                                          (-self.listeDeplacement[k][i][1] * zoom + decalageY+
                                          -self.listeDeplacement[k][i][1] * zoom + decalageY + size)/2)
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
terre = Pendule('terre', 9.81, 1, pi / 2, 1)
mars = Pendule('terre', 3.711, 1, pi / 2, 1)
# création de la simulation
simulation = Simulation([mars,terre], 0.01)

simulation.recap()
simulation.simulate()
simulation.show()
