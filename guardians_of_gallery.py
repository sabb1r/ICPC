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
    barrier_line1 = find_barrier_edges(pointX, sightLine.pointA)
    barrier_line2 = find_barrier_edges(pointX, sightLine.pointB)

    if not barrier_line1:
        return True, sightLine.pointA
    elif not barrier_line2:
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
    if len(find_barrier_edges(current_pivot, probable_point, crossing=False)) == 0:
        return probable_point


def can_reach_sighLine(pointX):
    perpendicularLine = Line(pointX, slope=perpendicularLine_slope)
    perpendicularPoint = perpendicularLine.solve(sightLine)
    if not perpendicularPoint.is_between(sightLine.pointA, sightLine.pointB):
        return False
    else:
        if len(find_barrier_edges(pointX, perpendicularPoint, crossing=False)) == 0:
            return True
        else:
            return False


vertices = []
guardPoint = None
statuePoint = None
distance_covered = 0


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


take_input()
boundary = create_boundary()
# print(boundary)
barrier_edges = find_barrier_edges(guardPoint, statuePoint, crossing=False)
# print(barrier_edges)

if len(barrier_edges) == 0:
    print('VOILA!!!')
    print('The required distance =', distance_covered)
else:
    barrier_vertices = find_barrier_vertices(barrier_edges)
    # print(barrier_vertices)
    # print('Barrier vertices for pointGuard and pointStatue:', barrier_vertices)
    # for p in barrier_vertices:
    #     plt.plot(p.x, p.y, 'ok')

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
            distance = distance1 if distance1 < distance2 else distance2
            distance_covered += distance
            break
        plt.plot([pivot_point.x, next_pivot.x], [pivot_point.y, next_pivot.y], '--g')

        distance_covered += pivot_point.distance(next_pivot)
        pivot_point = next_pivot

        # perpendicularPoint = perpendicularLine.solve(sightLine)
        # # print(perpendicularPoint)
        # # plt.plot(perpendicularPoint.x, perpendicularPoint.y, 'oy')
        # # print('Pivot point:', pivot_point)
        # new_barrier_edges = find_barrier_edges(pivot_point, perpendicularPoint, crossing=False)
        # # print('Barrier to overcome from pivot point to sightline:', new_barrier_edges)
        # if not perpendicularPoint.is_between(sightLine.pointA, sightLine.pointB) or new_barrier_edges:
        #     if can_see_sightLine(pivot_point)[0]:
        #         final_point = can_see_sightLine(pivot_point)[1]
        #         print('Found the sight line from the point', pivot_point, 'to the point', final_point)
        #         plt.plot([pivot_point.x, final_point.x], [pivot_point.y, final_point.y], '--g')
        #         distance_covered += pivot_point.distance(final_point)
        #         print('The required distance =', distance_covered)
        #         break
        #
        #     new_barrier_vertices = find_barrier_vertices(new_barrier_edges)
        #     # barrier_vertices = new_barrier_vertices
        #     # print(new_barrier_vertices)
        #     probable_next_pivot = barrier_vertices.pop(0)
        #     barrier_between_pivots = find_barrier_edges(pivot_point, probable_next_pivot)
        #     if not barrier_between_pivots:
        #         plt.plot([pivot_point.x, probable_next_pivot.x], [pivot_point.y, probable_next_pivot.y], '--g')
        #         distance_covered += pivot_point.distance(probable_next_pivot)
        #         pivot_point = probable_next_pivot
        #     else:
        #         print('BUT! There is barrier for moving to next pivot point')
        #         print(barrier_between_pivots)
        #         probable_next_pivot = find_barrier_vertices(barrier_between_pivots)[0]
        #         plt.plot([pivot_point.x, probable_next_pivot.x], [pivot_point.y, probable_next_pivot.y], '--g')
        #         distance_covered += pivot_point.distance(probable_next_pivot)
        #         pivot_point = probable_next_pivot
        #         barrier_vertices.insert(0, pivot_point)
        #         # barrier_vertices = barrier_between_pivots
        # else:
        #     print('VOILA')
        #     print('Found the sight line from the point', pivot_point, 'to the point', perpendicularPoint)
        #     plt.plot([pivot_point.x, perpendicularPoint.x], [pivot_point.y, perpendicularPoint.y], '--g')
        #     print('point to point distance', pivot_point.distance(perpendicularPoint))
        #     print('shortest distance', shortest_distance(pivot_point, sightLine))
        #     distance_covered += pivot_point.distance(perpendicularPoint)
        #     print('The required distance =', distance_covered)
        #     break
    else:
        finalLine = Line(pivot_point, slope=perpendicularLine_slope)
        finalPoint = finalLine.solve(sightLine)
        distance_covered += pivot_point.distance(finalPoint)
        plt.plot([pivot_point.x, finalPoint.x], [pivot_point.y, finalPoint.y], '--g')

    print('Final pivot point:', pivot_point)
    print('Total distance covered=', distance_covered)
# --- Plotting Section --- #
plt.plot(guardPoint.x, guardPoint.y, 'ob')
plt.plot(statuePoint.x, statuePoint.y, 'og')
draw_boundary()
plt.axis('scaled')
plt.show()
