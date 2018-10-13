from math import *
import Simulation
import Display
import Pendule

print('test')
terre = Pendule.Pendule('terre', 9.81, 1, pi / 2 , 1,"blue")
mars = Pendule.Pendule('mars', 3.711, 1, pi / 2, 1,"red")

# création de la simulation
simulation = Simulation.Simulation([terre,mars], 0.01)

simulation.recap()
simulation.simulate()
simulation.show()
