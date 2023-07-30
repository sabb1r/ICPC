class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        if round(self.x, 5) == round(other.x, 5) and round(self.y, 5) == round(other.y, 5):
            return True
        else:
            return False

    def distance(self, anotherPoint):
        if isinstance(anotherPoint, Point):
            return pow((self.x - anotherPoint.x) ** 2 + (self.y - anotherPoint.y) ** 2, 1 / 2)
        else:
            raise Exception('Bad Input!')

    def is_between(self, point1, point2):
        """
        :param point1: a Point object
        :param point2: a Point object
        :return: True if calling point is in between point1 and point2, False otherwise
        """
        distance1 = self.distance(point1)
        distance2 = self.distance(point2)

        # if any([x == 0 for x in (distance1, distance2)]):
        #     return False
        if round(distance1 + distance2, 5) == round(point1.distance(point2), 5):
            return True
        else:
            return False


class Line:
    def __init__(self, *args, slope=None):
        if len(args) == 2 and slope is None:
            if all([isinstance(arg, Point) for arg in args]):
                self.pointA = args[0]
                self.pointB = args[1]
                try:
                    self.slope = (self.pointB.y - self.pointA.y) / (self.pointB.x - self.pointA.x)
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

        if self.slope == 'Infinity':
            self.constant = None
        else:
            self.constant = self.pointA.y - self.slope * self.pointA.x

    def __repr__(self):
        if self.slope == 'Infinity':
            return 'x = {}'.format(self.pointA.x)
        elif self.slope == 0:
            return 'y = {}'.format(self.pointA.y)
        elif abs(self.slope) == 1:
            if self.constant > 0:
                return 'y = x + {}'.format(round(self.constant, 2)) if self.slope == 1 else 'y = -x + {}'.format(round(self.constant, 2))
            elif self.constant < 0:
                return 'y = x - {}'.format(round(abs(self.constant), 2)) if self.slope == 1 else 'y = -x - {}'.format(round(self.constant, 2))
            else:
                return 'y = x' if self.slope == 1 else 'y = -x'
        else:
            if self.constant > 0:
                return 'y = {}x + {}'.format(round(self.slope, 2), round(self.constant, 2))
            elif self.constant < 0:
                return 'y = {}x - {}'.format(round(self.slope, 2), round(abs(self.constant), 2))
            else:
                return 'y = {}x'.format(round(self.slope, 2))

    def solve(self, anotherLine):
        if not isinstance(anotherLine, Line):
            raise Exception('Bad Input!')

        if self.slope == anotherLine.slope:
            return None
        elif anotherLine.slope == 'Infinity':
            x = anotherLine.pointA.x
            y = self.slope * x + self.constant
        elif self.slope == 'Infinity':
            x = self.pointA.x
            y = anotherLine.slope * x + anotherLine.constant
        else:
            x = (anotherLine.constant - self.constant) / (self.slope - anotherLine.slope)
            y = (anotherLine.slope * self.constant - self.slope * anotherLine.constant) / (
                    anotherLine.slope - self.slope)

        return Point(x, y)

    def distance(self, anotherLine):
        if not isinstance(anotherLine, Line):
            raise Exception('Bad Input!')

        if self.slope == anotherLine.slope:
            if self.slope == 'Infinity':
                return abs(anotherLine.pointA.x - self.pointA.x)
            else:
                return abs(anotherLine.constant - self.constant)
        else:
            return None


def shortest_distance(p, ab):
    """
    :param p: a Point object
    :param ab: a Line object
    :return: shortest distance i.e. perpendicular distance of the line from the point
    """
    if not isinstance(p, Point) or not isinstance(ab, Line):
        raise Exception('Bad input!')

    if ab.slope == 'Infinity':
        return abs(ab.pointA.x - p.x)
    elif ab.slope == 0:
        return abs(ab.pointA.y - p.y)
    else:
        return abs(ab.slope * p.x - p.y + ab.constant) / pow(ab.slope ** 2 + 1, 1 / 2)
