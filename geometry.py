class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def distance(self, anotherPoint):
        if isinstance(anotherPoint, Point):
            return round(pow((self.x - anotherPoint.x) ** 2 + (self.y - anotherPoint.y) ** 2, 1 / 2), 5)
        else:
            raise Exception('Bad Input!')


class Line:
    def __init__(self, *args, slope=None):
        if len(args) == 2 and slope is None:
            if all([isinstance(arg, Point) for arg in args]):
                self.pointA = args[0]
                self.pointB = args[1]
                try:
                    self.slope = round((self.pointB.y - self.pointA.y) / (self.pointB.x - self.pointA.x), 5)
                except ZeroDivisionError:
                    self.slope = 'Infinity'
            else:
                raise Exception('Bad Input!')

        elif len(args) == 1 and (isinstance(slope, int) or isinstance(slope, float) or slope == 'Infinity'):
            if isinstance(args[0], Point):
                self.pointA = args[0]
                self.slope = slope
            else:
                raise Exception('Bad Input!')

        else:
            raise Exception('Bad Input!')

        if slope == 'Infinity':
            self.constant = None
        else:
            self.constant = round(self.pointA.y - self.slope * self.pointA.x, 5)

    def __repr__(self):
        if self.slope == 'Infinity':
            return 'x = {}'.format(self.pointA.x)
        elif self.slope == 0:
            return 'y = {}'.format(self.pointA.y)
        else:
            if self.constant > 0:
                return 'y = {}x + {}'.format(self.slope, self.constant)
            elif self.constant < 0:
                return 'y = {}x - {}'.format(self.slope, abs(self.constant))
            else:
                return 'y = {}x'.format(self.slope)

    def solve(self, anotherLine):
        if not isinstance(anotherLine, Line):
            raise Exception('Bad Input!')

        if self.slope == anotherLine.slope:
            return None
        elif anotherLine.slope == 'Infinity':
            x = anotherLine.pointA.x
            y = round(self.slope * x + self.constant, 5)
        elif self.slope == 'Infinity':
            x = self.pointA.x
            y = round(anotherLine.slope * x + anotherLine.constant, 5)
        else:
            x = round((anotherLine.constant - self.constant) / (self.slope - anotherLine.slope), 5)
            y = round((anotherLine.slope * self.constant - self.slope * anotherLine.constant) / (
                    anotherLine.slope - self.slope), 5)

        return Point(x, y)

    def distance(self, anotherLine):
        if not isinstance(anotherLine, Line):
            raise Exception('Bad Input!')

        if self.slope == anotherLine.slope:
            if self.slope == 'Infinity':
                return round(abs(anotherLine.pointA.x - self.pointA.x), 5)
            else:
                return round(abs(anotherLine.constant - self.constant), 5)
        else:
            return None


def shortest_distance(p, ab):
    if not isinstance(p, Point) or not isinstance(ab, Line):
        raise Exception('Bad input!')

    if ab.slope == 'Infinity':
        return round(abs(ab.pointA.x - p.x), 5)
    elif ab.slope == 0:
        return round(abs(ab.pointA.y - p.y), 5)
    else:
        return round(abs(ab.slope * p.x - p.y + ab.constant) / pow(ab.slope ** 2 + 1, 1/2), 5)
