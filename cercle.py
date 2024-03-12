from forme_geometric import FormeGeometrique
from math import pi


class Cercle(FormeGeometrique):
    def __init__(self, name, rayon, point=None):
        super().__init__()
        self.name = name
        self.rayon = rayon
        self.point = point

    def surface(self):
        return pi * self.rayon * self.rayon

    def perimetre(self):
        return 2 * pi * self.rayon

    def __str__(self):
        return f"Cercle {self.name} de centre ({self.rayon})"
