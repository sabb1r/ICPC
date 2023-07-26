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
        if len(crossings) == 2:
            return Line(point, statuePoint)


# --- Input Taking Section --- #
file_path = os.path.join(os.getcwd(), 'input.txt')  # Assuming the input file is put in the working directory as a name
# "input.txt"
with open(file_path, 'r') as file:
    no_vertex = int(file.readline().strip())

    vertices = []
    for i in range(no_vertex):
        vertex = Point(*[int(x) for x in file.readline().strip().split()])
        vertices.append(vertex)

    guardPoint = Point(*[int(x) for x in file.readline().strip().split()])
    statuePoint = Point(*[int(x) for x in file.readline().strip().split()])

boundary = create_boundary()
barrier_edges = find_barrier_edges(guardPoint, statuePoint)
if not barrier_edges:
    print('VOILA!!!')
else:
    barrier_vertices = find_barrier_vertices(barrier_edges)
    for p in barrier_vertices:
        plt.plot(p.x, p.y, 'ok')

    sightLine = create_sight_line()
    plt.plot([sightLine.pointA.x, sightLine.pointB.x], [sightLine.pointA.y, sightLine.pointB.y], '-c')

# --- Plotting Section --- #
plt.plot(guardPoint.x, guardPoint.y, 'ob')
plt.plot(statuePoint.x, statuePoint.y, 'og')
draw_boundary()
plt.show()
