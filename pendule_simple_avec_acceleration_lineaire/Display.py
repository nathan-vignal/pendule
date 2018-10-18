from tkinter import *
import time

def multiplication(MatriceA, MatriceB):
    matriceC = [[0] * (len(MatriceB[0]))]

    if len(MatriceA) != len(MatriceB[0]):
        print('Impossible de multiplier les deux matrices')
        return

    for i in range(len(MatriceB)):
        for j in range(len(MatriceA[0])):
            for k in range(len(MatriceA)):
                matriceC[i][j] += MatriceB[i][k] * MatriceA[j][k]
    return matriceC
class Display():
    def __init__(self):
        self.main = Tk()
        self.width = 1200
        self.height = 800
        self.decalageX = self.width * 0.5
        self.decalageY = self.height * 0.75
        self.size = 20
        self.zoom = 200
        self.objectAffiche = []

        self.main.geometry("1200x800")

        self.main.title("Pendule")
        self.canvas = Canvas(self.main, width=self.width, height=self.height)
        self.canvas.pack()

    ###################################################################################
    def display(self, simulation):
        self.affichageDesCentres(simulation)
        maxLenght = self.maxLenght(simulation)

        for i in range(0,maxLenght):
            for p in range(0, len(simulation.pendules)):
                if(i<len(simulation.listeDeplacement[p])):
                    #A*C+B*C = (A+B)*C  La multiplication matricielle est distributive sur l'addition
                    translation = [[self.zoom, 0, self.decalageX],
                                   [0, self.zoom, self.decalageY],
                                   [0, 0, 1]]
                    position = multiplication(translation, [simulation.listeDeplacement[p][i]])[0]
                    print(position)
                    print( simulation.listeDeplacement[p][i][0] * self.zoom + self.decalageX)
                    #afficher le point du pendule au centre du coordonné si le temps
                    self.createOval(simulation.listeDeplacement[p][i][0] * self.zoom + self.decalageX-self.size,
                                    -simulation.listeDeplacement[p][i][1] * self.zoom + self.decalageY-self.size,
                                    simulation.listeDeplacement[p][i][0] * self.zoom + self.decalageX + self.size,
                                    -simulation.listeDeplacement[p][i][1] * self.zoom + self.decalageY + self.size,
                                    simulation.pendules[p].color
                                    )

                    self.createLine(
                        ((simulation.pendules[p].origine[0] * self.zoom + self.decalageX) + (simulation.pendules[p].origine[0] * self.zoom + self.size / 2 + self.decalageX)) / 2
                        # moyenne entre les opposé de l'elipse pour avoir le centre
                        ,
                        ((-simulation.pendules[p].origine[1] * self.zoom + self.decalageY) + (-simulation.pendules[p].origine[1] * self.zoom + self.size / 2 + self.decalageY)) / 2
                        ,
                        simulation.listeDeplacement[p][i][0] * self.zoom + self.decalageX
                        ,
                        -simulation.listeDeplacement[p][i][1] * self.zoom + self.decalageY
                        ,
                        simulation.pendules[p].color )
            if(i==0):
                time.sleep(1)
            self.afficherImage(simulation)







        #on affiche tout
        self.main.mainloop()

    def afficherImage(self,simulation):
        self.canvas.update()
        time.sleep(0.01)
        for i in range(0, len(self.objectAffiche), 1):
            self.canvas.delete(self.objectAffiche[i])
        self.objectAffiche = []

    def createOval(self,x,y,i,j,color):
        point = self.canvas.create_oval(x, y, i, j,fill=color)
        self.objectAffiche.append(point)

    def createLine(self,x,y,i,j,color):
        ligne = self.canvas.create_line(x, y, i, j)
        self.objectAffiche.append(ligne)

    def affichageDesCentres(self, simulation):
        for k in range(0, len(simulation.pendules), 1): #affichage des fixations
            origineX = simulation.pendules[k].origine[0]
            origineY = simulation.pendules[k].origine[1]
            fixation = self.canvas.create_oval(origineX*self.zoom +self.decalageX,
                                               -origineY*self.zoom +self.decalageY,
                                               origineX*self.zoom+self.size/2 +self.decalageX,
                                               -origineY*self.zoom+self.size/2 +self.decalageY,
                                               fill=simulation.pendules[k].color
                                               )
            self.canvas.update()



    def maxLenght(self, simulation):
        maxLenght = 0
        for k in range(0, len(simulation.pendules), 1):
            if (len(simulation.listeDeplacement[k]) > maxLenght):
                maxLenght = len(simulation.listeDeplacement[k])
        return maxLenght