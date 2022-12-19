class Sphere:
    def __init__(self,values):
        self.name = str(values[0])
        self.x = float(values[1])
        self.y = float(values[2])
        self.z = float(values[3])
        self.sx = float(values[4])
        self.sy = float(values[5])
        self.sz = float(values[6])
        self.r = float(values[7])
        self.g = float(values[8])
        self.b = float(values[9])
        self.ka = float(values[10])
        self.kd = float(values[11])
        self.ks = float(values[12])
        self.kr = float(values[13])
        self.n = int(values[14])
    def __str__(self):
        return str(self.name)
    def __repr__(self):
        return str(self)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.sx == other.sx and self.sy == other.sy and self.sz == other.sz and self.r == other.r and self.g == other.g and self.b == other.b and self.ka == other.ka and self.kd == other.kd and self.kr == other.kr and self.ks == other.ks and self.n == other.n
