from math import *
import Simulation
import Display
import Pendule

print('test')
terre = Pendule.Pendule('terre', 9.81, 1, pi / 2 , 1,"blue",0.05,1.5)
mars = Pendule.Pendule('mars', 3.711, 1, pi / 2, 1,"red",0.05)
lune = Pendule.Pendule('lune', 1.62, 1, pi / 2, 1,"white",0.05)

# création de la simulation
simulation = Simulation.Simulation([terre,mars,lune], 0.01)

simulation.recap()
simulation.simulate()
simulation.show()
