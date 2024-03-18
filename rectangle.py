from forme_geometric import FormeGeometrique


class Rectangle(FormeGeometrique):

    def __init__(self, nom, longueur, largeur, point=None):
        super().__init__()
        self.name = nom
        self.longueur = longueur
        self.largeur = largeur
        self.point = point

    def surface(self):
        return self.longueur * self.largeur

    def perimetre(self):
        return 2 * (self.longueur + self.largeur)

    def __str__(self):
        if self.point:
            obj_str = (f"Rectangle: Nom = {self.name};  Longueur = {self.longueur}; Largeur = {self.largeur}; "
                       f"Point = {self.point}")
        obj_str = f"Rectangle: Nom = {self.name};  Longueur = {self.longueur}; Largeur = {self.largeur}"
        return obj_str

    def calculate_center(self):
        return round(self.longueur / 2, 2), round(self.largeur / 2, 2)
