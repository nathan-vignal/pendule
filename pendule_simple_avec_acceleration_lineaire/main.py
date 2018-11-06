from math import *
import Simulation
import Display
import Pendule

#déclaration des pendules
#      paramètres         (name, g, l, theta, masse,color,k, origine->optionnel)
foucault = Pendule.Pendule('foucault', 9.81, 20, pi/2, 10,"blue",0.05,0.5)
terre = Pendule.Pendule('terre', 9.81, 1, pi/2, 20,"blue",0.5,0.5)
mars = Pendule.Pendule('mars', 3.711, 1, pi / 2, 1,"red",0.5,-1)
lune = Pendule.Pendule('lune', 1.62, 1, pi / 2, 1,"white",0.5)

# création de la simulation
#           paramètres            ([pendule1,pendule2,...,pendule n], temps entre Image)
simulation = Simulation.Simulation([terre,mars,lune], 0.04)

#affiche dans le terminal les paramètres des pendules
simulation.recap()

#effectue les calculs
simulation.simulate()

#affiche l'animations
simulation.show()
