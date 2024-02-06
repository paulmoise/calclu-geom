class Point:

    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y


    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
    
    def display(self):
        print(f"{self.name}({self.x}; {self.y})")