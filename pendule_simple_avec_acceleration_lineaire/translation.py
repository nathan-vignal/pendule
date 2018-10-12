import importlib

moduleName = input('main.py')
importlib.import_module(moduleName)
def createTranslation(tx, ty) :
    matrice = [[1, 0, 0], [0, 1 ,0],[tx, ty, 1]]
    return matrice

A = [ [1, 1, 1] ]

translation = createTranslation(1, 1)
print(A)
print(translation)
print(x)







