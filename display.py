from point import Point
from carre import Carre


def calcul_surface_entre_deux_points(p1: Point, p2: Point):
    print("calcul de distance entre", p1.name, " et ", p2.name, " : ")
    print(p1.distance(p2))


def extract_details(user_input: str) -> tuple[str, float, float]:
    # Split the expression by '=' to separate the name and the point creation
    name, point_str = user_input.split('=')

    # Strip whitespace from name
    name = name.strip()

    # Remove leading and trailing whitespaces and split the point string by ';'
    sep = ';' if ';' in point_str else ','
    point_str = point_str.strip()[len('Point('):-1]
    x_str, y_str = point_str.split(sep)

    try:
        x = float(x_str)
        y = float(y_str)
        return name, x, y
    except ValueError:
        raise ValueError("Les coordonnées doivent être des nombres")


def lire_point_teminal() -> Point:
    user_input = input(f"Declarer un point nom=point(x,y) \n")
    name, x, y = extract_details(user_input)
    return Point(name, x, y)


def calcul_surface_carrer(carrer: Carre):
    print("calcul de surface de ", carrer.name, " : ", carrer.surface())


def lire_square():
    print("Declarer un carre nom=carre(x)")
    input_str = input()
    nom, reste = input_str.split("=")
    cote = reste.split("(")[1].split(")")[0]
    cote = cote.strip()
    if not cote.isdigit():
        raise ValueError("La longueur du côté doit être un nombre.")
    cote = float(cote)
    carre = Carre(nom, cote)

    return carre
