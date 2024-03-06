from forme_geometric import FormeGeometrique


class Rectangle(FormeGeometrique):

    def __init__(self, nom, longueur, largeur):
        super().__init__()
        self.name = nom
        self.longueur = longueur
        self.largeur = largeur

    def surface(self):
        return self.longueur * self.largeur

    def perimetre(self):
        return 2 * (self.longueur + self.largeur)

    def __str__(self):
        return f"Rectangle {self.name} de longueur (L = {self.longueur}) et de largeur l = ({self.largeur})"
