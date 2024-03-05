class Rectangle:

    def __init__(self, nom,longueur,largeur):
        self.name = nom
        self.longueur = longueur
        self.largeur = largeur

    def surface(self):
        return self.longueur * self.largeur
    
    def perimetre(self):
        return 2 * (self.longueur + self.largeur)