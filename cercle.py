from forme_geometric import FormeGeometrique
from math import pi
from point import Point


class Cercle(FormeGeometrique):
    def __init__(self, name, rayon):
        super().__init__()
        self.name = name
        self.rayon = rayon

    def __init__(self, name, rayon, Point):
        super().__init__()
        self.name = name
        self.rayon = rayon
        self.point = Point

    def surface(self):
        return pi * self.rayon * self.rayon

    def perimetre(self):
        return 2 * pi * self.rayon

    def __str__(self):
        return f"Cercle {self.name} de centre ({self.rayon})"
    
    def calcule_centre(self):
        return Point(self.name, self.point.x, self.point.y)
