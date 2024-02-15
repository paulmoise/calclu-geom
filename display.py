from point import Point

def calcul_surface_entre_deux_points(p1: Point, p2: Point):
    print("calcul de distance entre",p1.name," et ",p2.name," : ")
    print(p1.distance(p2))

p1 = Point("A", 1, 2)
p2 = Point("B", 5, 5)
calcul_surface_entre_deux_points(p1, p2)
