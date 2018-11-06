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


##                       ##
 ##  gère l'animation   ##
##                       ##
class Display():
    def __init__(self):
        self.main = Tk()
        #une fenêtre tk inter à l'origine en haut à gauche avec l'axe des ordonné opposé (positif vers le bas)
        self.width = 1200 #largeur de la fenêtre
        self.height = 800 #hauteur de la fenêtre
        self.decalageX = self.width * 0.5    #translation en x de l'origine de la fenêtre
        self.decalageY = self.height * 0.75  #translation en y de l'origine de la fenêtre
        self.zoom = 200  #dilate les espaces entre les points
        self.size = self.zoom /20   #taille de la masse du pendule

        self.objectAffiche = []     # cette liste permet de pouvoir garder un moyen d'accéder à un object affiché
                                    # de manière à pouvoir tous les supprimer entre chaques images


        # (origine du graphique ,largeur  ,hauteur )
        self.graphique = Graphique.Graphique([self.width-300, 120], 280, 119,2)
        self.listeGraphique = []    #liste qui va contenir la liste des valeurs de chaque pendule affiché dans le graphique

        #pas important
        self.valeurGraphMax = -9999   #init valeur max
        self.valeurGraphMin = 9999    #init valeur min
        self.deltaExtremum = 0        #init deltaExtremum



        self.main.geometry("1200x800")
        #nom de la fenêtre
        self.main.title("Pendules")
        #création du canvas
        self.canvas = Canvas(self.main, width=self.width, height=self.height)
        self.canvas.pack()


    # fonction principale gère l'afficahge en fonction du temps
    def display(self, simulation):

        #initialise la liste des points à afficher dans le graphique
        # comme une liste composé d'autant de liste que de pendules
        for p in range(0, len(simulation.pendules)):
            self.listeGraphique.append([])

        # calcul le plus grand extremum parmis les pendules
        for p in range(0, len(simulation.pendules)):
            if(simulation.pendules[p].deltaExtremum > self.deltaExtremum):
                self.deltaExtremum = simulation.pendules[p].deltaExtremum

        # calcul la plus petite valeur min parmis les pendules
        for p in range(0, len(simulation.pendules)):
            if(simulation.pendules[p].valeurGraphMin < self.valeurGraphMin):
                self.valeurGraphMin = simulation.pendules[p].valeurGraphMin

        # calcul la plus grande valeur max parmis les pendules
        for p in range(0, len(simulation.pendules)):
            if (simulation.pendules[p].valeurGraphMax > self.valeurGraphMax):
                self.valeurGraphMax = simulation.pendules[p].valeurGraphMax

        #affiche les attaches des pendules
        self.affichageDesCentres(simulation)
        #affiche les axes du graphique
        self.afficherAxes(simulation)
        #calcul la longueur de la plus longue liste de position à afficher
        maxLenght = self.maxLenght(simulation)





        #pour chaque position des pendules temps que la derniere position n'est pas affichée
        for i in range(0,maxLenght-1):

            #affiche le temps écoulé depuis le début de la simulation
            self.createText(self.graphique.origine[0] + self.graphique.tailleX - 20,
                            self.graphique.origine[1] + 20,
                            round(i * simulation.tempsEntreImages, 3),
                            'black')
            #pour chaque pendule
            for p in range(0, len(simulation.pendules)):

                #si il reste des positions à afficher pour ce pendule
                if(i<len(simulation.listeDeplacement[p])-1):

                    #matrice de translation de pour amener le point au centre de la simulation et appliquer le zoom
                    translation = [[self.zoom, 0, self.decalageX],#A*C+B*C = (A+B)*C  La multiplication matricielle est distributive sur l'addition
                                   [0, -self.zoom, self.decalageY],
                                   [0, 0, 1]]
                    #simulation.listeDeplacement[p][i]  = la position actuel du pendule p dans la simulation
                    position = multiplication(translation, [simulation.listeDeplacement[p][i]])

                    #translation nécessaire pour afficher le pendule(le bout) voir le dossier trop compliqué pour expliquer ici
                    translation = [[1, 0, -self.size],
                                   [0, 1, -self.size],
                                   [0, 0, 1]]
                    positiondroite = multiplication(translation, position)

                    # translation nécessaire pour afficher le point
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
                    # calcul la position de la fixation du pendule   (on ne recheche pas l'obtimisation mais la lisibilité
                    origine = [simulation.pendules[p].origine[0], simulation.pendules[p].origine[1], 1]
                    translation = [[self.zoom, 0, self.decalageX],
                                   [0, -self.zoom, self.decalageY],
                                   [0, 0, 1]]
                    origine = multiplication(translation, [origine])
                    #affiche le fil du pendule
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
            #temporise 1 seconde après l'ouverture de la fenêtre pour faire un démarage moins brutal
            if(i==0):
                time.sleep(1)
                tempsPrecedent = time.time()
            tempsPrecedent = self.afficherImage(simulation.tempsEntreImages,i,tempsPrecedent)


        #fonction de  tkInter ...
        self.main.mainloop()

    #met à jour l'affichage ( par exemple self.createLine n'affiche rien tant que la mise à jour n'est pas faite
    #
    def afficherImage(self,tempsEntreImage,i,tempsPrecedent):
        #mise à jour de 'laffichage
        self.canvas.update()
        #temporise le temps entre deux images moins le temps de calcul du programme entre deux images
        #permet de rester en temps réel
        time.sleep(tempsEntreImage - (time.time() - tempsPrecedent) )
        #stocke quand le dernier affichage a été fait
        tempsPrecedent = time.time()

        # supprimer tout les objets affiché
        for i in range(0, len(self.objectAffiche), 1):
            self.canvas.delete(self.objectAffiche[i])
        self.objectAffiche = []
        #permet de récupérer le temps précécent plus tard
        return tempsPrecedent

        #crée un point et l'ajoute aux objets affichés ( liste des objets affiché dans l'image actuelle )
    def createOval(self,x,y,i,j,color):
        point = self.canvas.create_oval(x, y, i, j,fill=color)
        self.objectAffiche.append(point)

        #même chose que la métode juste au dessus mais en délégant les translations à cette fonction
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

        # crée une ligne et l'ajoute aux objets affichés
    def createLine(self,x,y,i,j,color):
        ligne = self.canvas.create_line(x, y, i, j)
        self.objectAffiche.append(ligne)
        # crée du texte et l'ajoute aux objets affichés
    def createText(self,x,y,text,color):
        texte = self.canvas.create_text(x,y,text=text,fill=color)
        self.objectAffiche.append(texte)

        #affiche l'axe de rotation de chaque pendule
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

    # calcul la longueur de la plus longue liste de position à afficher
    def maxLenght(self, simulation):
        maxLenght = 0
        for k in range(0, len(simulation.pendules), 1):
            if (len(simulation.listeDeplacement[k]) > maxLenght):
                maxLenght = len(simulation.listeDeplacement[k])
        return maxLenght

    # affiche les axes du graphique
    def afficherAxes(self,simulation):
        self.canvas.create_line(self.graphique.origine[0],self.graphique.origine[1],self.graphique.origine[0], (self.graphique.origine[1]-self.graphique.tailleY),fill='black')# créer la verticale

        self.canvas.create_line(self.graphique.origine[0], self.graphique.origine[1] - self.graphique.tailleY*(- self.valeurGraphMin / self.deltaExtremum), self.graphique.origine[0]+self.graphique.tailleX,
                                self.graphique.origine[1] - self.graphique.tailleY*(- self.valeurGraphMin / self.deltaExtremum), # lire (0- self.valeurGraphMin / self.deltaExtremum) -> le ratio que vaut la valeur 0
                                fill='black',)  # créer l'horizontal
        self.canvas.create_text(self.graphique.origine[0]-40, self.graphique.origine[1]-self.graphique.tailleY+10,text='max = ' + str(round(self.valeurGraphMax,2))+'m/s' ,fill="black")
        print(self.graphique.tailleY*(- self.valeurGraphMin / self.deltaExtremum))
        print(self.valeurGraphMin)
        self.canvas.update()


    def animerGraphique(self, simulation,i,p):


        indice = i
        nombrePoints = self.graphique.deltaT/simulation.tempsEntreImages  #nombre de points à afficher au max dans le graphique
        distanceEntrePoints = self.graphique.tailleX/nombrePoints         #espace entre deux points sur les cotés (x)

        #décale les points vers la gauche
        translationEntrePoints = [[1, 0, -distanceEntrePoints],
                                  [0, 1, 0],
                                  [0, 0, 1]]
        ratioValeurValeurMax = (simulation.pendules[p].listeGraph[indice] - self.valeurGraphMin) / self.deltaExtremum

        #le premier point est le point de plus à droite du graphique, la valeur actuel du paramètre suivis
        # petit amusement avec  les matrices de translations au bout de 25 fois ça devient ennuyant
        premierPoint = [[1,1,1]]
        translation = [[0, 0, self.graphique.origine[0] +self.graphique.tailleX-(distanceEntrePoints *(indice -i))],
                       [0, 0, self.graphique.origine[1] - self.graphique.tailleY*ratioValeurValeurMax],
                       [0, 0, 1]]
        premierPoint= multiplication(translation, premierPoint)[0]

        #affiche le point le plus à droite
        self.superCreateOval(premierPoint[0]
                             ,premierPoint[1]
                             ,2
                             ,simulation.pendules[p].color)

        #affiche la valeur du point actuel (en bas à gauche du graphique dans la simulation)
        self.createText(self.graphique.origine[0]-30,
                        self.graphique.origine[1]+p*20,
                        round(simulation.pendules[p].listeGraph[indice],2),
                        simulation.pendules[p].color)

        #décrémenté à chaque point du graphique affiché pour une image
        indice -= 1
        #cette liste stocke tout les points affiché pour chaque pendule
        self.listeGraphique[p].append(premierPoint)

        #tant qu'il reste des points à affiché et que il n'y a pas trop de points dans le graphique
        while(indice>0 and self.graphique.deltaT > (i-indice)*simulation.tempsEntreImages):
            #translate tout les points affiché vers la gauche
            self.listeGraphique[p][i-indice] = multiplication(translationEntrePoints,[self.listeGraphique[p][i-indice]])[0]
            self.superCreateOval(self.listeGraphique[p][i-indice][0],self.listeGraphique[p][i-indice][1],2,simulation.pendules[p].color)#( x, y,size, color)

            #- 1 point à translater
            indice -= 1

        #si il ya trop de points affiché supprimer le plus à gauche
        if(len(self.listeGraphique[p])>nombrePoints):
            self.listeGraphique[p].pop(0)










