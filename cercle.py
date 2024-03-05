from forme_geometric import FormeGeometrique


class Cercle(FormeGeometrique):
    def __init__(self, rayon):
        super().__init__()
        self.rayon = rayon

    def surface(self):
        return 3.14 * self.rayon * self.rayon

    def perimetre(self):
        return 2 * 3.14 * self.rayon
