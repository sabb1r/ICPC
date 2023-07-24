import os
from geometry import *
from matplotlib import pyplot as plt


def draw_boundary():
    pass


# --- Input Taking Section --- #
file_path = os.getcwd() + '\\input.txt'  # Assuming the input file is put in the working directory as a name
# "input.txt"

with open(file_path, 'r') as file:
    no_edges = int(file.readline().strip())

    edges = []
    for i in range(no_edges):
        edge = Point(*[int(x) for x in file.readline().strip().split()])
        edges.append(edge)

    guardPoint = Point(*[int(x) for x in file.readline().strip().split()])
    statuePoint = Point(*[int(x) for x in file.readline().strip().split()])
