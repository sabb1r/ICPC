import os
from geometry import *
from matplotlib import pyplot as plt


def create_boundary():
    boundary = []
    for i in range(len(vertices) - 1):
        edge = Line(vertices[i], vertices[i + 1])
        boundary.append(edge)

    i += 1
    boundary.append(Line(vertices[i], vertices[0]))

    return boundary


def draw_boundary():
    abscissa = [p.x for p in vertices]
    abscissa.append(vertices[0].x)

    ordinate = [p.y for p in vertices]
    ordinate.append(vertices[0].y)

    plt.plot(abscissa, ordinate, 'r')


def find_barrier_edges(pointA, pointB):
    barrier_edges = []
    line_ab = Line(pointA, pointB)
    for edge in boundary:
        intersecting_point = line_ab.solve(edge)
        if intersecting_point is None:
            continue
        elif intersecting_point in [edge.pointA, edge.pointB, pointA, pointB]:
            continue
        else:
            if intersecting_point.is_between(edge.pointA, edge.pointB) and intersecting_point.is_between(line_ab.pointA,
                                                                                                         line_ab.pointB):
                barrier_edges.append(edge)

    return barrier_edges


def find_barrier_vertices(barrier_lines):
    barrier_vertices = []

    for ind, line in enumerate(barrier_lines):
        if ind % 2 == 0:
            barrier_vertices.append(line.pointB)
        else:
            barrier_vertices.append(line.pointA)

    return barrier_vertices


def create_sight_line():
    for point in barrier_vertices:
        crossings = find_barrier_edges(point, statuePoint)
        # print('Crossing lines for sightLine creation:', crossings)
        if len(crossings) == 0:
            line = Line(point, statuePoint)
            break

    for edge in boundary:
        intersecting_point = edge.solve(line)
        if intersecting_point is None:
            continue
        elif intersecting_point.is_between(edge.pointA, edge.pointB) and not intersecting_point.is_between(line.pointA,
                                                                                                           line.pointB) and intersecting_point.distance(
            line.pointA) < intersecting_point.distance(line.pointB):
            return Line(intersecting_point, statuePoint)


def can_see_sightLine(pointX):
    barrier_line1 = find_barrier_edges(pointX, sightLine.pointA)
    barrier_line2 = find_barrier_edges(pointX, sightLine.pointB)

    if not barrier_line1:
        return True, sightLine.pointA
    elif not barrier_line2:
        return True, sightLine.pointB
    else:
        return False, None


# --- Input Taking Section --- #
file_path = os.path.join(os.getcwd(), 'input.txt')  # Assuming the input file is put in the working directory as a name
# "input.txt"
with open(file_path, 'r') as file:
    no_vertex = int(file.readline().strip())

    vertices = []
    for i in range(no_vertex):
        vertex = Point(*[float(x) for x in file.readline().strip().split()])
        vertices.append(vertex)

    guardPoint = Point(*[float(x) for x in file.readline().strip().split()])
    statuePoint = Point(*[float(x) for x in file.readline().strip().split()])

boundary = create_boundary()
barrier_edges = find_barrier_edges(guardPoint, statuePoint)

distance_covered = 0

if not barrier_edges:
    print('VOILA!!!')
    print('The required distance =', distance_covered)
else:
    barrier_vertices = find_barrier_vertices(barrier_edges)
    # print('Barrier vertices for pointGuard and pointStatue:', barrier_vertices)
    # for p in barrier_vertices:
    #     plt.plot(p.x, p.y, 'ok')

    sightLine = create_sight_line()
    plt.plot([sightLine.pointA.x, sightLine.pointB.x], [sightLine.pointA.y, sightLine.pointB.y], '--c')

    pivot_point = guardPoint
    while barrier_vertices:
        if sightLine.slope == 0:
            perpendicularLine = Line(pivot_point, slope='Infinity')
        elif sightLine.slope == 'Infinity':
            perpendicularLine = Line(pivot_point, slope=0)
        else:
            perpendicularLine = Line(pivot_point, slope=-1 / sightLine.slope)

        perpendicularPoint = perpendicularLine.solve(sightLine)
        # print(perpendicularPoint)
        # plt.plot(perpendicularPoint.x, perpendicularPoint.y, 'oy')
        # print('Pivot point:', pivot_point)
        new_barrier_edges = find_barrier_edges(pivot_point, perpendicularPoint)
        # print('Barrier to overcome from pivot point to sightline:', new_barrier_edges)
        if not perpendicularPoint.is_between(sightLine.pointA, sightLine.pointB) or new_barrier_edges:
            if can_see_sightLine(pivot_point)[0]:
                final_point = can_see_sightLine(pivot_point)[1]
                print('Found the sight line from the point', pivot_point, 'to the point', final_point)
                plt.plot([pivot_point.x, final_point.x], [pivot_point.y, final_point.y], '--g')
                distance_covered += pivot_point.distance(final_point)
                print('The required distance =', distance_covered)
                break

            new_barrier_vertices = find_barrier_vertices(new_barrier_edges)
            # barrier_vertices = new_barrier_vertices
            # print(new_barrier_vertices)
            probable_next_pivot = barrier_vertices.pop(0)
            barrier_between_pivots = find_barrier_edges(pivot_point, probable_next_pivot)
            if not barrier_between_pivots:
                plt.plot([pivot_point.x, probable_next_pivot.x], [pivot_point.y, probable_next_pivot.y], '--g')
                distance_covered += pivot_point.distance(probable_next_pivot)
                pivot_point = probable_next_pivot
            else:
                print('BUT! There is barrier for moving to next pivot point')
                print(barrier_between_pivots)
                probable_next_pivot = find_barrier_vertices(barrier_between_pivots)[0]
                plt.plot([pivot_point.x, probable_next_pivot.x], [pivot_point.y, probable_next_pivot.y], '--g')
                distance_covered += pivot_point.distance(probable_next_pivot)
                pivot_point = probable_next_pivot
                barrier_vertices.insert(0, pivot_point)
                # barrier_vertices = barrier_between_pivots
        else:
            print('VOILA')
            print('Found the sight line from the point', pivot_point, 'to the point', perpendicularPoint)
            plt.plot([pivot_point.x, perpendicularPoint.x], [pivot_point.y, perpendicularPoint.y], '--g')
            print('point to point distance', pivot_point.distance(perpendicularPoint))
            print('shortest distance', shortest_distance(pivot_point, sightLine))
            distance_covered += pivot_point.distance(perpendicularPoint)
            print('The required distance =', distance_covered)
            break

# --- Plotting Section --- #
plt.plot(guardPoint.x, guardPoint.y, 'ob')
plt.plot(statuePoint.x, statuePoint.y, 'og')
draw_boundary()
plt.axis('scaled')
plt.show()
