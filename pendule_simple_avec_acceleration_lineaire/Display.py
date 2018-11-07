from tkinter import *
import time
import Graphique
# MatriceA * MatriceB
def multiplication(MatriceA, MatriceB):
    matriceC = [[0] * (len(MatriceB[0]))]
    if len(MatriceA) != len(MatriceB[0]):
        print('Impossible de multiplier les deux matrices')
        print('Matrice A = ' + str(MatriceA))
        print('Matrice B = ' + str(MatriceB))
        return

    for i in range(len(MatriceB)):
        for j in range(len(MatriceA[0])):
            for k in range(len(MatriceA)):
                matriceC[i][j] += MatriceB[i][k] * MatriceA[j][k]
    return matriceC


##                           ##
##  Gestion de l'animation   ##
##                           ##

class Display():
    def __init__(self):
        self.main = Tk()

        # Une fenêtre Tk Inter à l'origine en haut à gauche avec l'axe des ordonnées opposé (positif vers le bas)

        self.width = 1200 # Largeur de la fenêtre
        self.height = 800 # Hauteur de la fenêtre
        self.decalageX = self.width * 0.5    # Translation en x de l'origine de la fenêtre
        self.decalageY = self.height * 0.75  # Translation en y de l'origine de la fenêtre
        self.zoom = 20  # Dilate les espaces entre les points
        self.size = self.zoom /20   # Taille de la masse du pendule

        self.objectAffiche = []     # Liste permettant l'accès aux objets affichés
                                    # Pour tous les supprimer entre chaques images


        # (origine du graphique ,largeur  ,hauteur )
        self.graphique = Graphique.Graphique([self.width-300, 400], 280, 399,2)
        self.listeGraphique = []    # Liste contenant la liste des valeurs de tous les pendules affichés dans le graphique

        # Pas important
        self.valeurGraphMax = -9999   #init valeur max
        self.valeurGraphMin = 9999    #init valeur min
        self.deltaExtremum = 0        #init deltaExtremum



        self.main.geometry(str(self.width)+"x"+str(self.height))

        # Nom de la fenêtre
        self.main.title("Pendules")

        # Création du canvas
        self.canvas = Canvas(self.main, width=self.width, height=self.height)

        # À ignorer
        self.canvas.pack()


    # Fonction principale pour la gestion de l'afficahge en fonction du temps
    def display(self, simulation):

        # Initialise la liste des points à afficher dans le graphique
        # La liste est composée d'autant de listes que de pendules
        for p in range(0, len(simulation.pendules)):
            self.listeGraphique.append([])

        # Calcule le plus grand extremum parmi les pendules
        for p in range(0, len(simulation.pendules)):
            if(simulation.pendules[p].deltaExtremum > self.deltaExtremum):
                self.deltaExtremum = simulation.pendules[p].deltaExtremum

        # Calcule la plus petite valeur 'min' parmi les pendules
        for p in range(0, len(simulation.pendules)):
            if(simulation.pendules[p].valeurGraphMin < self.valeurGraphMin):
                self.valeurGraphMin = simulation.pendules[p].valeurGraphMin

        # Calcule la plus grande valeur 'max' parmi les pendules
        for p in range(0, len(simulation.pendules)):
            if (simulation.pendules[p].valeurGraphMax > self.valeurGraphMax):
                self.valeurGraphMax = simulation.pendules[p].valeurGraphMax

        # Affiche les attaches des pendules
        self.affichageDesCentres(simulation)

        # Affiche les axes du graphique
        self.afficherAxes(simulation)

        # Calcule la longueur de la plus longue liste des positions à afficher
        maxLenght = self.maxLenght(simulation)





        # Pour chaque positions des pendules,  tant que la derniere position n'est pas affichée
        for i in range(0,maxLenght-1):

            # Affiche le temps écoulé depuis le début de la simulation
            self.createText(self.graphique.origine[0] + self.graphique.tailleX - 20,
                            self.graphique.origine[1] + 20,
                            round(i * simulation.tempsEntreImages, 3),
                            'black')

            # Pour chaque pendule
            for p in range(0, len(simulation.pendules)):

                # S'il reste des positions à afficher pour ce pendule
                if(i<len(simulation.listeDeplacement[p])-1):

                    # Matrice de translation pour emmener le point au centre de la simulation et appliquer le zoom
                    translation = [[self.zoom, 0, self.decalageX],#A*C+B*C == (A+B)*C  La multiplication matricielle est distributive sur l'addition
                                   [0, -self.zoom, self.decalageY], #C*A + B*C != (A+B)*C   !!!!
                                   [0, 0, 1]]

                    # Simulation.listeDeplacement[p][i]  = la position actuelle du pendule p dans la simulation
                    position = multiplication(translation, [simulation.listeDeplacement[p][i]])

                    # Translation nécessaire pour afficher le pendule(le bout),
                    # /!\ s'il vous plaît se référer au dossier /!\
                    translation = [[1, 0, -self.size],
                                   [0, 1, -self.size],
                                   [0, 0, 1]]
                    positiondroite = multiplication(translation, position)

                    # Translation nécessaire pour afficher le point
                    translation = [[1, 0, self.size],
                                   [0, 1, self.size],
                                   [0, 0, 1]]
                    positiongauche = multiplication(translation, position)


                    #affiche le pendule
                    self.createOval(positiongauche[0][0],
                                    positiongauche[0][1],
                                    positiondroite[0][0],
                                    positiondroite[0][1],
                                    simulation.pendules[p].color
                                    )

                    # Calcule la position de la fixation du pendule
                    # (on ne recheche pas l'optimisation mais la lisibilité
                    origine = [simulation.pendules[p].origine[0], simulation.pendules[p].origine[1], 1]
                    translation = [[self.zoom, 0, self.decalageX],
                                   [0, -self.zoom, self.decalageY],
                                   [0, 0, 1]]
                    origine = multiplication(translation, [origine])

                    # Affiche le fil du pendule
                    self.createLine(
                        origine[0][0]
                        ,
                        origine[0][1]
                        ,
                        position[0][0]
                        ,
                        position[0][1]
                        ,
                        simulation.pendules[p].color )

                    self.animerGraphique(simulation,i,p)

            # Temporise 1 seconde après l'ouverture de la fenêtre pour un démarrage moins brutal
            if(i==0):
                time.sleep(1)
                tempsPrecedent = time.time()
            tempsPrecedent = self.afficherImage(simulation.tempsEntreImages,i,tempsPrecedent)


        # Fonction de  tkInter ...
        self.main.mainloop()

    # Met à jour l'affichage
    # ( par exemple self.createLine n'affiche rien tant que la mise à jour n'est pas faite )

    def afficherImage(self,tempsEntreImage,i,tempsPrecedent):

        # Mise à jour de l'affichage
        self.canvas.update()

        # Temporise le temps entre deux images moins le temps de calcul du programme entre deux images
        # Permet de rester en temps réel
        time.sleep(tempsEntreImage - (time.time() - tempsPrecedent) )

        # Stocke quand le dernier affichage a été fait
        tempsPrecedent = time.time()

        # Supprimer tous les objets affichés
        for i in range(0, len(self.objectAffiche), 1):
            self.canvas.delete(self.objectAffiche[i])
        self.objectAffiche = []

        # Permet de récupérer le temps précécent plus tard
        return tempsPrecedent


        # Crée un point et l'ajoute aux objets affichés
        # ( liste des objets affichés dans l'image actuelle )
    def createOval(self,x,y,i,j,color):
        point = self.canvas.create_oval(x, y, i, j,fill=color)
        self.objectAffiche.append(point)

        # Crée un cercle avec pour centre (x,y) et rayon size
    def superCreateOval(self, x, y,size, color):
        centre = [x,y,1]
        translation = [[1, 0, -size],
                       [0, 1, -size],
                       [0, 0, 1]]
        gauche = multiplication(translation, [centre])[0]
        translation = [[1, 0, size],
                       [0, 1, size],
                       [0, 0, 1]]
        droite = [x,y,1]
        droite = multiplication(translation, [droite])[0]
        point = self.canvas.create_oval(gauche[0], gauche[1], droite[0], droite[1], fill=color)
        self.objectAffiche.append(point)

        # Crée une ligne et l'ajoute aux objets affichés
    def createLine(self,x,y,i,j,color):
        ligne = self.canvas.create_line(x, y, i, j)
        self.objectAffiche.append(ligne)

        # Crée du texte et l'ajoute aux objets affichés
    def createText(self,x,y,text,color):
        texte = self.canvas.create_text(x,y,text=text,fill=color)
        self.objectAffiche.append(texte)

        # Affiche l'axe de rotation de chaque pendule
    def affichageDesCentres(self, simulation):
        for k in range(0, len(simulation.pendules), 1): #affichage des fixations
            origine = [simulation.pendules[k].origine[0],simulation.pendules[k].origine[1],1]
            translation = [[self.zoom, 0, self.decalageX], # A*(B+C) = A*B + A*C
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

            self.canvas.create_oval(originegauche[0][0],    #[[x,y,1]]
                                    originegauche[0][1],
                                    originedroite[0][0],
                                    originedroite[0][1],
                                    fill=simulation.pendules[k].color
                                    )
            self.canvas.update()

    # Calcule la longueur de la plus longue liste de position à afficher
    def maxLenght(self, simulation):
        maxLenght = 0
        for k in range(0, len(simulation.pendules), 1):
            if (len(simulation.listeDeplacement[k]) > maxLenght):
                maxLenght = len(simulation.listeDeplacement[k])
        return maxLenght

    # Affiche les axes du graphique
    def afficherAxes(self,simulation):
        # Crée la verticale
        self.canvas.create_line(self.graphique.origine[0],self.graphique.origine[1],self.graphique.origine[0], (self.graphique.origine[1]-self.graphique.tailleY),fill='black')
        # Crée l'abscisse
        self.canvas.create_line(self.graphique.origine[0], self.graphique.origine[1] - self.graphique.tailleY*(- self.valeurGraphMin / self.deltaExtremum), self.graphique.origine[0]+self.graphique.tailleX,
                                self.graphique.origine[1] - self.graphique.tailleY*(- self.valeurGraphMin / self.deltaExtremum), # lire (0- self.valeurGraphMin / self.deltaExtremum) -> le ratio que vaut la valeur 0
                                fill='black',)  # créer l'horizontal
        self.canvas.create_text(self.graphique.origine[0]-40, self.graphique.origine[1]-self.graphique.tailleY+10,text='max = ' + str(round(self.valeurGraphMax,2))+'m/s' ,fill="black")

        self.canvas.update()



    def animerGraphique(self, simulation,i,p):


        indice = i
        nombrePoints = self.graphique.deltaT/simulation.tempsEntreImages  #nombre de points à afficher au max dans le graphique
        distanceEntrePoints = self.graphique.tailleX/nombrePoints         #espace entre deux points sur les cotés (x)

        # Décale les points vers la gauche
        translationEntrePoints = [[1, 0, -distanceEntrePoints],
                                  [0, 1, 0],
                                  [0, 0, 1]]
        ratioValeurValeurMax = (simulation.pendules[p].listeGraph[indice] - self.valeurGraphMin) / self.deltaExtremum

        # Le premier point est le point de plus à droite du graphique, la valeur actuelle du paramètre suivi
        # Petit amusement avec  les matrices de translations au bout de 25 fois ça devient ennuyant
        #  Ne sert à rien on est d'accord
        premierPoint = [[1,1,1]]
        translation = [[0, 0, self.graphique.origine[0] +self.graphique.tailleX],
                       [0, 0, self.graphique.origine[1] - self.graphique.tailleY*ratioValeurValeurMax],
                       [0, 0, 1]]
        premierPoint= multiplication(translation, premierPoint)[0]

        # Affiche le point le plus à droite
        self.superCreateOval(premierPoint[0]
                             ,premierPoint[1]
                             ,3
                             ,simulation.pendules[p].color)

        # Affiche la valeur du point actuel (en bas à gauche du graphique dans la simulation)
        self.createText(self.graphique.origine[0]-30,
                        self.graphique.origine[1]+p*20,
                        round(simulation.pendules[p].listeGraph[indice],2),
                        simulation.pendules[p].color)

        # Décrémenté à chaque points du graphique affiché pour une image
        indice -= 1

        # Cette liste stocke tous les points affichés pour chaque pendules
        self.listeGraphique[p].append(premierPoint)

        # Tant qu'il reste des points à afficher et que il n'y a pas trop de points dans le graphique
        while(indice>0 and self.graphique.deltaT > (i-indice)*simulation.tempsEntreImages):

            # Translate tous les points affichés vers la gauche
            self.listeGraphique[p][i-indice] = multiplication(translationEntrePoints,[self.listeGraphique[p][i-indice]])[0]
            self.superCreateOval(self.listeGraphique[p][i-indice][0],self.listeGraphique[p][i-indice][1],2,simulation.pendules[p].color)#( x, y,size, color)

            # - 1 point à translater
            indice -= 1

        # Supprimer le point qui n'est plus affiché
        if(len(self.listeGraphique[p])>nombrePoints):
            self.listeGraphique[p].pop(0)










