class Light:
    def __init__(self,values):
        self.name = str(values[0])
        self.x = float(values[1])
        self.y = float(values[2])
        self.z = float(values[3])
        self.r = float(values[4])
        self.g = float(values[5])
        self.b = float(values[6])
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.r == other.r and self.g == other.g and self.b == other.b
