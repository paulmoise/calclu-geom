import forme_geometric
class Carre(forme_geometric):
    
    def __init__(self, nom,cote):
        self.name = nom
        self.cote = cote

    def surface(self):
        return self.cote ** 2
    def perimetre(self):
        return self.cote * 4



