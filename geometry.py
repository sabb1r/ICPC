class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def distance(self, anotherPoint):
        if isinstance(anotherPoint, Point):
            return round(pow((self.x - anotherPoint.x) ** 2 + (self.y - anotherPoint.y) ** 2, 1/2), 5)
        else:
            raise print('Bad Input!')