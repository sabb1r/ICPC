import os
from geometry import *
from matplotlib import pyplot as plt


def create_boundary():
    for i in range(len(vertices) - 1):
        edge = Line(vertices[i], vertices[i + 1])
        boundary.append(edge)

    boundary.append(Line(vertices[i], vertices[0]))


def draw_boundary():
    abscissa = [p.x for p in vertices]
    abscissa.append(vertices[0].x)

    ordinate = [p.y for p in vertices]
    ordinate.append(vertices[0].y)

    plt.plot(abscissa, ordinate, 'r')


def find_barrier_edges(pointA, pointB):
    lineAB = Line(pointA, pointB)


# --- Input Taking Section --- #
file_path = os.getcwd() + '\\input.txt'  # Assuming the input file is put in the working directory as a name
# "input.txt"
with open(os.path.abspath(file_path), 'r') as file:
    no_vertex = int(file.readline().strip())

    vertices = []
    for i in range(no_vertex):
        vertex = Point(*[int(x) for x in file.readline().strip().split()])
        vertices.append(vertex)

    guardPoint = Point(*[int(x) for x in file.readline().strip().split()])
    statuePoint = Point(*[int(x) for x in file.readline().strip().split()])

boundary = []

# --- Plotting Section --- #
plt.plot(guardPoint.x, guardPoint.y, 'ob')
plt.plot(statuePoint.x, statuePoint.y, 'og')
draw_boundary()
plt.show()
