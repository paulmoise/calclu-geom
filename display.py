from point import Point

def calcul_surface_entre_deux_points(p1: Point, p2: Point):
    print("calcul de distance entre",p1.name," et ",p2.name," : ")
    print(p1.distance(p2))

p1 = Point("A", 1, 2)
p2 = Point("B", 5, 5)
calcul_surface_entre_deux_points(p1, p2)
def lire_square():
    print("Entrez le nom et la longueur du côté du carré dans le format suivant : Nom = Carre(cote)")
    input_str = input("Nom et côté : ")
    nom, reste = input_str.split("=")
    cote = reste.split("(")[1].split(")")[0]
    cote = cote.strip()
    if not cote.isdigit():
        raise ValueError("La longueur du côté doit être un nombre.")
    cote = float(cote)
    return nom.strip(), cote

nom_du_carre, cote_du_carre = lire_square()
print("Nom du carré :", nom_du_carre)
print("Longueur du côté du carré :", cote_du_carre)
