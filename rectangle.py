from forme_geometric import FormeGeometrique


class Rectangle(FormeGeometrique):

    def __init__(self, longueur, largeur):
        super().__init__()
        self.name = nom
        self.longueur = longueur
        self.largeur = largeur

    def surface(self):
        return self.longueur * self.largeur

    def perimetre(self):
        return 2 * (self.longueur + self.largeur)
