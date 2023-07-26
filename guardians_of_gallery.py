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


def find_barrier_vertices(pointA, pointB):
    barrier_vertices = []
    line_ab = Line(pointA, pointB)
    for edge in boundary:
        intersecting_point = line_ab.solve(edge)
        if intersecting_point is None:
            continue
        else:
            if intersecting_point.is_between(edge.pointA, edge.pointB) and intersecting_point.is_between(line_ab.pointA, line_ab.pointB):
                barrier_vertices.append(intersecting_point)

    return barrier_vertices


# --- Input Taking Section --- #
file_path = os.path.join(os.getcwd(), 'input.txt') # Assuming the input file is put in the working directory as a name
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
barrier_points = find_barrier_vertices(guardPoint, statuePoint)
if not barrier_points:
    print('VOILA!!!')
else:
    for dot in barrier_points:
        plt.plot(dot.x, dot.y, 'ok')

# --- Plotting Section --- #
plt.plot(guardPoint.x, guardPoint.y, 'ob')
plt.plot(statuePoint.x, statuePoint.y, 'og')
draw_boundary()
plt.show()
