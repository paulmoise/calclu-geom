from forme_geometric import FormeGeometrique


class Carre(FormeGeometrique):

    def __init__(self, nom, cote, point=None):
        super().__init__()
        self.point = point
        self.name = nom
        self.cote = cote

    def surface(self):
        return self.cote ** 2

    def perimetre(self):
        return self.cote * 4

    def __str__(self):
        if self.point:
            return (f"Carre: Nom = {self.name};  Cote = {self.cote}; "
                    f"Point = {self.point.name} ({self.point.x}; {self.point.y})")
        return f"Carre: Nom {self.name}; Cote ({self.cote})"

    def calculate_center(self):
        return round(self.cote / 2, 2), round(self.cote / 2, 2)