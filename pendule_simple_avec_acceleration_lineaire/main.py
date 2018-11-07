from math import *
import Simulation
import Display
import Pendule

# Déclaration des pendules
# Paramètres (name, g, l, theta, masse,color,k, origine->optionnel)
foucault = Pendule.Pendule('foucault', 9.81, 20, pi/2, 10,"blue",100,0.5)
terre = Pendule.Pendule('terre', 9.81, 1, pi/2, 20,"blue",0.5,0.5)
mars = Pendule.Pendule('mars', 3.711, 1, pi / 2, 1,"red",0.5,-1)
lune = Pendule.Pendule('lune', 1.62, 1, pi / 2, 1,"white",0.5)

# Création de la simulation
# Paramètres ([pendule1,pendule2,...,pendule n], temps entre Image)
simulation = Simulation.Simulation([foucault,terre,mars,lune], 0.04)

# Affiche dans le terminal les paramètres des pendules
simulation.recap()

# Effectue les calculs
simulation.simulate()

# Affiche l'animation
simulation.show()