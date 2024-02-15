from point import Point
from carrer import Carre

def calcul_surface_entre_deux_points(p1: Point, p2: Point):
    print("calcul de distance entre",p1.name," et ",p2.name," : ")
    print(p1.distance(p2))

p1 = Point("A", 1, 2)
p2 = Point("B", 5, 5)
calcul_surface_entre_deux_points(p1, p2)

def calcul_surface_carrer(carrer: Carre):
    print("calcul de surface de ",carrer.name," : ",carrer.surface())

carrer = Carre("carrer1", 5)
calcul_surface_carrer(carrer)

