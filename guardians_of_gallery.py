import os
from geometry import *
from matplotlib import pyplot as plt


def create_boundary():
    boundary_list = []
    for i in range(len(vertices) - 1):
        edge = Line(vertices[i], vertices[i + 1])
        boundary_list.append(edge)

    i += 1
    boundary_list.append(Line(vertices[i], vertices[0]))

    return boundary_list


def draw_boundary():
    abscissa = [p.x for p in vertices]
    abscissa.append(vertices[0].x)

    ordinate = [p.y for p in vertices]
    ordinate.append(vertices[0].y)

    plt.plot(abscissa, ordinate, 'r')


def find_barrier_edges(pointA, pointB, touch=True):
    barrier_lines = []
    lineAB = Line(pointA, pointB)
    for edge in boundary:
        intersecting_point = lineAB.solve(edge)
        if intersecting_point is None:
            continue
        elif not intersecting_point.is_between(edge.pointA, edge.pointB):
            continue
        elif not intersecting_point.is_between(pointA, pointB):
            continue
        else:
            if not touch:
                if intersecting_point in [edge.pointA, edge.pointB] or intersecting_point in [pointA, pointB]:
                    continue
                else:
                    barrier_lines.append(edge)
            else:
                barrier_lines.append(edge)

    return barrier_lines


def find_barrier_vertices(barrier_lines):
    barrier_points = []

    for ind, line in enumerate(barrier_lines):
        nextPoint = vertices[vertices.index(line.pointB) % len(vertices) + 1]

        position = line.pointB.relative_position(nextPoint)

        if position['Right'] and not position['Left']:
            if line.pointB.y > line.pointA.y:
                barrier_points.append(line.pointB)
            else:
                barrier_points.append(line.pointA)
        elif position['Left'] and not position['Right']:
            if line.pointB.y > line.pointA.y:
                barrier_points.append(line.pointA)
            else:
                barrier_points.append(line.pointB)

        if len(barrier_points) > 1 and barrier_points[-1] == barrier_points[-2]:
            del (barrier_points[-1])

    return barrier_points


def create_sight_line():
    for point in barrier_vertices:
        crossings = find_barrier_edges(point, statuePoint, touch=False)
        if len(crossings) == 0:
            probable_line = Line(statuePoint, point)
            break
        else:
            if barrier_vertices.index(point) == len(barrier_vertices) - 1:
                for p in find_barrier_vertices(crossings):
                    if len(find_barrier_edges(p, statuePoint, touch=False)) == 0:
                        probable_line = Line(statuePoint, p)
                        break
            else:
                continue

    for edge in boundary:
        intersecting_point = edge.solve(probable_line)
        if intersecting_point is None:
            continue
        elif (intersecting_point.is_between(edge.pointA, edge.pointB)) and (
                not intersecting_point.is_between(probable_line.pointA, probable_line.pointB)) and (
                intersecting_point.distance(probable_line.pointB) < intersecting_point.distance(probable_line.pointA)):
            if len(find_barrier_edges(intersecting_point, probable_line.pointB, touch=False)) == 0:
                return Line(probable_line.pointB, intersecting_point)
            else:
                continue


def can_see_sightLine(pointX):
    barrier_line1 = find_barrier_edges(pointX, sightLine.pointA, touch=False)
    barrier_line2 = find_barrier_edges(pointX, sightLine.pointB, touch=False)

    if len(barrier_line1) == 0 and len(barrier_line2) != 0:
        return True, sightLine.pointA
    elif len(barrier_line1) != 0 and len(barrier_line2) == 0:
        return True, sightLine.pointB
    elif len(barrier_line1) == 0 and len(barrier_line2) == 0:
        if pointX.distance(sightLine.pointA) <= pointX.distance(sightLine.pointB):
            return True, sightLine.pointA
        else:
            return True, sightLine.pointB
    else:
        return False, None


def next_pivot_point(current_pivot):
    probable_point = barrier_vertices.pop(0)
    barriers = find_barrier_edges(current_pivot, probable_point, touch=False)
    if len(barriers) == 0:
        return probable_point
    else:
        barrier_vertices.insert(0, probable_point)
        barrier_points = find_barrier_vertices(barriers)
        probable_point = barrier_points[-1]
        return probable_point


def next_pivot_point_ver2(pivot):
    new_barrier = find_barrier_edges(pivot, midPoint, touch=False)
    new_barrier_vertices = find_barrier_vertices(new_barrier)
    probable_point = new_barrier_vertices[0]

    barriers = find_barrier_edges(pivot, probable_point, touch=False)
    if len(barriers) == 0:
        return probable_point
    else:
        barrier_points = find_barrier_vertices(barriers)
        probable_point = barrier_points[0]
        return probable_point


def can_reach_sighLine(pointX):
    perpendicularLine = Line(pointX, slope=perpendicularLine_slope)
    perpendicularPoint = perpendicularLine.solve(sightLine)
    new_barriers = find_barrier_edges(pointX, perpendicularPoint, touch=False)
    if not perpendicularPoint.is_between(sightLine.pointA, sightLine.pointB):
        return False
    else:
        if len(new_barriers) == 0:
            return True
        else:
            return False


def take_input():
    file_path = os.path.join(os.getcwd(), 'input.txt')
    with open(file_path, 'r') as file:
        no_vertex = int(file.readline().strip())
        for i in range(no_vertex):
            vertex = Point(*[float(x) for x in file.readline().strip().split()])
            vertices.append(vertex)

        global guardPoint, statuePoint
        guardPoint = Point(*[float(x) for x in file.readline().strip().split()])
        statuePoint = Point(*[float(x) for x in file.readline().strip().split()])


vertices = []
guardPoint = None
statuePoint = None
path = []
distance_covered = 0

take_input()
boundary = create_boundary()
barrier_edges = find_barrier_edges(guardPoint, statuePoint, touch=False)
path.append(guardPoint)

if len(barrier_edges) == 0:
    print(path)
    print('The required distance =', distance_covered)
else:
    barrier_vertices = find_barrier_vertices(barrier_edges)
    barrier_vertices.sort(key=lambda x: x[0])

    sightLine = create_sight_line()
    midPoint = Point((sightLine.pointA.x + sightLine.pointB.x) / 2, (sightLine.pointA.y + sightLine.pointB.y) / 2)
    plt.plot([sightLine.pointA.x, sightLine.pointB.x], [sightLine.pointA.y, sightLine.pointB.y], '--c')

    if sightLine.slope == 0:
        perpendicularLine_slope = 'Infinity'
    elif sightLine.slope == 'Infinity':
        perpendicularLine_slope = 0
    else:
        perpendicularLine_slope = -1 / sightLine.slope

    pivot_point = guardPoint

    while not can_reach_sighLine(pivot_point):
        try:
            # next_pivot = next_pivot_point(pivot_point)
            next_pivot = next_pivot_point_ver2(pivot_point)
        except IndexError:
            distance1 = pivot_point.distance(sightLine.pointA)
            distance2 = pivot_point.distance(sightLine.pointB)
            if distance1 < distance2:
                distance = distance1
                path.append(sightLine.pointA)
            else:
                distance = distance2
                path.append(sightLine.pointB)

            distance_covered += distance
            break

        yes, p = can_see_sightLine(pivot_point)
        if yes:
            if pivot_point.distance(p) < shortest_distance(next_pivot, sightLine) + pivot_point.distance(next_pivot):
                path.append(p)
                distance_covered += pivot_point.distance(p)
                break

        plt.plot([pivot_point.x, next_pivot.x], [pivot_point.y, next_pivot.y], '--g')
        distance_covered += pivot_point.distance(next_pivot)
        pivot_point = next_pivot
        path.append(pivot_point)


    else:
        finalLine = Line(pivot_point, slope=perpendicularLine_slope)
        finalPoint = finalLine.solve(sightLine)
        path.append(finalPoint)
        distance_covered += pivot_point.distance(finalPoint)
        plt.plot([pivot_point.x, finalPoint.x], [pivot_point.y, finalPoint.y], '--g')

    for p in path:
        if path.index(p) == len(path) - 1:
            print(p)
        else:
            print(p, '->', end=' ')
    print('Total distance covered=', distance_covered)

# --- Plotting Section --- #
plt.plot(guardPoint.x, guardPoint.y, 'ob')
plt.plot(statuePoint.x, statuePoint.y, 'og')
draw_boundary()
plt.axis('scaled')
plt.show()
