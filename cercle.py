class Cercle:
    def __init__(self, rayon):
        self.rayon = rayon

    def surface(self):
        return 3.14 * self.rayon * self.rayon
    
    def perimetre(self):
        return 2 * 3.14 * self.rayon