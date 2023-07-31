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


def find_barrier_edges(pointA, pointB, crossing=True):
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
            if not crossing:
                if intersecting_point in [edge.pointA, edge.pointB, pointA, pointB]:
                    continue
                else:
                    barrier_lines.append(edge)
            else:
                barrier_lines.append(edge)

    return barrier_lines


def find_barrier_vertices(barrier_lines):
    barrier_points = []

    for ind, line in enumerate(barrier_lines):
        # have to test whether the lines are up boundary or down boundary
        boundary_index = boundary.index(line)
        if line.pointA.x > line.pointB.x or line.pointA.x > boundary[boundary_index + 1].pointB.x:
            # It is upward boundary
            if ind % 2 == 0:
                barrier_points.append(line.pointA)
            else:
                barrier_points.append(line.pointB)
        else:
            if ind % 2 == 0:
                barrier_points.append(line.pointB)
            else:
                barrier_points.append(line.pointA)

        if len(barrier_points) > 1 and barrier_points[-1] == barrier_points[-2]:
            del (barrier_points[-1])

    return barrier_points


def create_sight_line():
    for point in barrier_vertices:
        crossings = find_barrier_edges(point, statuePoint, crossing=False)
        # print('Crossing lines for sightLine creation:', crossings)
        if len(crossings) == 0:
            probable_line = Line(point, statuePoint)
            break
        else:
            if barrier_vertices.index(point) == len(barrier_vertices) - 1:
                for p in find_barrier_vertices(crossings):
                    if len(find_barrier_edges(p, statuePoint, crossing=False)) == 0:
                        probable_line = Line(p, statuePoint)
                        break
            else:
                continue

    for edge in boundary:
        intersecting_point = edge.solve(probable_line)
        if intersecting_point is None:
            continue
        elif (intersecting_point.is_between(edge.pointA, edge.pointB)) and (
                not intersecting_point.is_between(probable_line.pointA, probable_line.pointB)) and (
                intersecting_point.distance(probable_line.pointA) < intersecting_point.distance(probable_line.pointB)):
            if len(find_barrier_edges(intersecting_point, probable_line.pointA, crossing=False)) == 0:
                return Line(intersecting_point, probable_line.pointA)
            else:
                continue

        # sightLine = find_barrier_edges(intersecting_point, probable_line.pointA)


def can_see_sightLine(pointX):
    barrier_line1 = find_barrier_edges(pointX, sightLine.pointA, crossing=False)
    barrier_line2 = find_barrier_edges(pointX, sightLine.pointB, crossing=False)

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
    # Option 1.

    # perpendicularLine = Line(current_pivot, slope=perpendicularLine_slope)
    # intersecting_point = perpendicularLine.solve(sightLine)
    # edges_towards_sightLine = find_barrier_edges(current_pivot, intersecting_point, crossing=False)
    # edge_vertices = find_barrier_vertices(edges_towards_sightLine)

    # for p in barrier_vertices:
    #     if len(find_barrier_edges(current_pivot, p, crossing=False)) == 0:
    #         return p

    # Option 2
    probable_point = barrier_vertices.pop(0)
    barriers = find_barrier_edges(current_pivot, probable_point, crossing=False)
    if len(barriers) == 0:
        return probable_point
    else:
        barrier_vertices.insert(0, probable_point)
        barrier_points = find_barrier_vertices(barriers)
        probable_point = barrier_points[-1]
        return probable_point


def can_reach_sighLine(pointX):
    perpendicularLine = Line(pointX, slope=perpendicularLine_slope)
    perpendicularPoint = perpendicularLine.solve(sightLine)
    # perpendicular_distance = pointX.distance(perpendicularPoint)
    if not perpendicularPoint.is_between(sightLine.pointA, sightLine.pointB):
        return False
    else:
        if len(find_barrier_edges(pointX, perpendicularPoint, crossing=False)) == 0:
            return True
        else:
            return False


def take_input():
    file_path = os.path.join(os.getcwd(), 'input.txt')  # Assuming the input file is put in the working directory as
    # a name
    # "input.txt"
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
barrier_edges = find_barrier_edges(guardPoint, statuePoint, crossing=False)
path.append(guardPoint)

if len(barrier_edges) == 0:
    print(path)
    print('The required distance =', distance_covered)
else:
    barrier_vertices = find_barrier_vertices(barrier_edges)
    barrier_vertices.sort(key=lambda x:x[0])

    sightLine = create_sight_line()
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
            next_pivot = next_pivot_point(pivot_point)
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
        print(p, '->', end=' ')
    print()
    print('Total distance covered=', distance_covered)
# --- Plotting Section --- #
plt.plot(guardPoint.x, guardPoint.y, 'ob')
plt.plot(statuePoint.x, statuePoint.y, 'og')
draw_boundary()
plt.axis('scaled')
plt.show()
