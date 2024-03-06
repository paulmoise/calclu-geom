import forme_geometric


class Triangle(forme_geometric.FormeGeometrique):
    def __init__(self, nom, cote1, cote2, cote3):
        super().__init__()
        self.cote1 = cote1
        self.cote2 = cote2
        self.cote3 = cote3
        self.name = nom

    def surface(self):
        p = (self.cote1 + self.cote2 + self.cote3) / 2
        return (p * (p - self.cote1) * (p - self.cote2) * (p - self.cote3)) ** 0.5

    def perimetre(self):
        return self.cote1 + self.cote2 + self.cote3

    def __str__(self):
        return f"Triangle {self.name} de cote ({self.cote1} ; {self.cote2} et {self.cote3})"
