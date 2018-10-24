from tkinter import *
import time
import Graphique
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
        self.zoom = 300
        self.objectAffiche = []

        self.graphique = Graphique.Graphique([self.width-300, 140], 280, 135,2) #(self,origine,tailleX,tailleY):


        self.main.geometry("1200x800")

        self.main.title("Pendule")
        self.canvas = Canvas(self.main, width=self.width, height=self.height)
        self.canvas.pack()

    ###################################################################################
    def display(self, simulation):
        self.affichageDesCentres(simulation)
        self.afficherAxes()
        maxLenght = self.maxLenght(simulation)

        for i in range(0,maxLenght):
            for p in range(0, len(simulation.pendules)):

                if(i<len(simulation.listeDeplacement[p])):
                    #A*C+B*C = (A+B)*C  La multiplication matricielle est distributive sur l'addition
                    translation = [[self.zoom, 0, self.decalageX],
                                   [0, -self.zoom, self.decalageY],
                                   [0, 0, 1]]


                    position = multiplication(translation, [simulation.listeDeplacement[p][i]])

                    translation = [[1, 0, -self.size],
                                   [0, 1, -self.size],
                                   [0, 0, 1]]
                    positiondroite = multiplication(translation, position)
                    translation = [[1, 0, self.size],
                                   [0, 1, self.size],
                                   [0, 0, 1]]
                    positiongauche = multiplication(translation, position)
                    #afficher le point du pendule au centre du coordonné si le temps

                    self.createOval(positiongauche[0][0],
                                    positiongauche[0][1],
                                    positiondroite[0][0],
                                    positiondroite[0][1],
                                    simulation.pendules[p].color
                                    )

                    origine = [simulation.pendules[p].origine[0], simulation.pendules[p].origine[1], 1]
                    translation = [[self.zoom, 0, self.decalageX],
                                   [0, -self.zoom, self.decalageY],
                                   [0, 0, 1]]
                    origine = multiplication(translation, [origine])
                    self.createLine(
                        origine[0][0]
                        # moyenne entre les opposé de l'elipse pour avoir le centre
                        ,
                        origine[0][1]
                        ,
                        position[0][0]
                        ,
                        position[0][1]
                        ,
                        simulation.pendules[p].color )
                    self.animerGraphique(simulation,i,p)
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

    def superCreateOval(self, x, y,size, color):
        gauche = [x,y,1]
        translation = [[1, 0, -size],
                       [0, 1, -size],
                       [0, 0, 1]]
        gauche = multiplication(translation, [gauche])[0]
        translation = [[1, 0, size],
                       [0, 1, size],
                       [0, 0, 1]]
        droite = [x,y,1]
        droite = multiplication(translation, [droite])[0]
        point = self.canvas.create_oval(gauche[0], gauche[1], droite[0], droite[1], fill=color)
        self.objectAffiche.append(point)

    def createLine(self,x,y,i,j,color):
        ligne = self.canvas.create_line(x, y, i, j)
        self.objectAffiche.append(ligne)

    def affichageDesCentres(self, simulation):
        for k in range(0, len(simulation.pendules), 1): #affichage des fixations
            origine = [simulation.pendules[k].origine[0],simulation.pendules[k].origine[1],1]
            translation = [[self.zoom, 0, self.decalageX],
                           [0, -self.zoom, self.decalageY],
                           [0, 0, 1]]
            origine = multiplication(translation,[origine])

            translation = [[1, 0, -self.size/3],
                           [0, 1, -self.size/3],
                           [0, 0, 1]]
            originegauche = multiplication(translation,origine)
            translation = [[1, 0, self.size / 3],
                           [0, 1, self.size / 3],
                           [0, 0, 1]]
            originedroite = multiplication(translation, origine)

            self.canvas.create_oval(originegauche[0][0],
                                               originegauche[0][1],
                                               originedroite[0][0],
                                               originedroite[0][1],
                                               fill=simulation.pendules[k].color
                                               )
            self.canvas.update()



    def maxLenght(self, simulation):
        maxLenght = 0
        for k in range(0, len(simulation.pendules), 1):
            if (len(simulation.listeDeplacement[k]) > maxLenght):
                maxLenght = len(simulation.listeDeplacement[k])
        return maxLenght
    def afficherAxes(self):
         self.canvas.create_line(self.graphique.origine[0],self.graphique.origine[1],self.graphique.origine[0], (self.graphique.origine[1]-self.graphique.tailleY),fill='black')# créer la verticale

         self.canvas.create_line(self.graphique.origine[0], self.graphique.origine[1], self.graphique.origine[0]+self.graphique.tailleX,
                                        self.graphique.origine[1],
                                        fill='black')  # créer l'horizontal
         self.canvas.update()

    def animerGraphique(self, simulation,i,p):


        indice = i
        nombrePoints = self.graphique.deltaT/simulation.tempsEntreImages
        distanceEntrePoints = self.graphique.tailleX/nombrePoints
        listePoint = []
        translationEntrePoints = [[1, 0, distanceEntrePoints],
                                  [0, 1, 0],
                                  [0, 0, 1]]
        premierPoint = [[1,1,1]]
        ratioValeurValeurMax = (simulation.pendules[p].listeGraph[indice] - simulation.pendules[p].valeurGraphMin)/simulation.pendules[p].deltaExtremum
        translation = [[0, 0, self.graphique.origine[0] +self.graphique.tailleX-(distanceEntrePoints *(indice -i))],
                       [0, 0, self.graphique.origine[1] - self.graphique.tailleY*ratioValeurValeurMax],
                       [0, 0, 1]]
        premierPoint= multiplication(translation, premierPoint)[0]

        self.superCreateOval(premierPoint[0]
                             ,premierPoint[1]
                             ,3
                             ,"black")
        listePoint.append(premierPoint)
        while(indice>0 and self.graphique.deltaT > -(indice-i)*simulation.tempsEntreImages):
            #COME BACK HERE LISTEPOINT

            indice -= 1




