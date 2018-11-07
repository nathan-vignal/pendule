from math import *

class Fluide :
    def __init__(self, name, c,b,a,v,w,h ):

        self.name = name
        if (self.name == 'eau') :

            self.c = '' # coefficient de frottement solide
            self.b = '' # coefficient de frottement visqueux
            self.a = '(r * p)/2m'  # coefficient quadratique de frottement fluide
            self.v = '' # vitesse du fluide
            self.w = '' # pulsation du fluide
            self.h = '' #viscosité dynamique
            self.r = '' #masse volumique
            self

        if (self.name == 'air') :

            self.c = '' # coefficient de frottement solide
            self.b = '' # coefficient de frottement visqueux
            self.a = '(r * p)/2m'  # coefficient quadratique de frottement fluide
            self.v = '' # vitesse du fluide
            self.w = '' # pulsation du fluide
            self.h = 1.8 * 10^-5 #viscosité dynamique à 20°
            self.r = 1.2 * 10^-3 #masse volumique  à 20°

        if (self.name == 'miel') :

            self.c = '' # coefficient de frottement solide
            self.b = '' # coefficient de frottement visqueux
            self.a = '(r * p)/2m'  # coefficient quadratique de frottement fluide
            self.v = '' # vitesse du fluide
            self.w = '' # pulsation du fluide
            self.h = '' #viscosité dynamique
            self.r = '' #masse volumique





