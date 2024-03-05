from display import *
from display import *
from point import Point
from point import Point
from carrer import Carre
print("Declarer deux point pour calculer la distance entre les deux")

p1 = lire_point_teminal()
p2 = lire_point_teminal()
calcul_surface_entre_deux_points(p1, p2)
print("Declarer un carre pour calculer la surface ")
carrer = lire_square()
calcul_surface_carrer(carrer)