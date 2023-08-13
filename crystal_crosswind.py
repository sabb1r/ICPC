import sys

dim_x, dim_y, no_wind_flow = 0, 0, 0
crystal_points = set()
boundary_points = set()
wind_direction = dict()
confirmed_empty_points = set()
probable_boundary_points = set()
recursion_stop = set()


def take_input():
    with open(sys.argv[1], 'r') as file:
        global dim_x, dim_y, no_wind_flow, crystal_points, boundary_points, wind_direction
        dim_x, dim_y, no_wind_flow = [int(val) for val in file.readline().strip().split(' ')]
        crystal_points = {(i, j) for i in range(1, dim_x + 1) for j in range(1, dim_y + 1)}
        for i in range(no_wind_flow):
            text = file.readline().strip().split(' ')
            wind = tuple(map(int, text[:2]))
            no_boundary = int(text[2])
            boundary = set()
            for j in range(3, 2 * no_boundary + 3, 2):
                coordinate = tuple(map(int, text[j: j + 2]))
                boundary_points.add(coordinate)
                boundary.add(coordinate)
            wind_direction[wind] = boundary


def create_output(structure):
    matrix = []
    for x in range(1, dim_y + 1):
        line = []
        for y in range(1, dim_x + 1):
            if (y, x) in structure:
                line.append('#')
            else:
                line.append('.')

        line.append('\n')
        matrix.append(''.join(line))

    return matrix


def write_output():
    with open(sys.argv[2] + sys.argv[1].split('/')[-1].split('.')[0] + '.ans', 'w') as file:
        file.writelines(minimal_structure)
        file.write('\n')
        file.writelines(maximal_structure)


def is_outside(point):
    if any([point[0] <= 0 or point[0] > dim_x, point[1] <= 0 or point[1] > dim_y]):
        return True
    else:
        return False


def is_boundary(point, wind):
    p = (point[0] - wind[0], point[1] - wind[1])
    if is_outside(p) or p not in boundary_points:
        return True
    else:
        return False


def insert_boundary(point):
    global recursion_stop
    recursion_stop.add(point)
    diff_points = [(point[0] - wind[0], point[1] - wind[1]) for wind in wind_direction]

    if any([is_outside(x) or x in confirmed_empty_points for x in diff_points]):
        raise Exception

    else:
        stats = []
        for x in diff_points:
            if x in boundary_points or x in recursion_stop:
                stats.append(True)
            else:
                try:
                    insert_boundary(x)
                except Exception:
                    confirmed_empty_points.add(x)
                    stats.append(False)
                    break
        if not all(stats):
            raise Exception
        else:
            boundary_points.add(point)


take_input()

# Create confirmed_empty_points set
for key, val in wind_direction.items():
    for point in val:
        p = (point[0] - key[0], point[1] - key[1])
        if not is_outside(p):
            confirmed_empty_points.add(p)

# Create probable_boundary_points set
probable_boundary_points = crystal_points.difference(confirmed_empty_points).difference(boundary_points)

# Minimal structure generation
for wind, boundaries in wind_direction.items():
    other_boundary_points = boundary_points.difference(boundaries)
    for boundary in other_boundary_points:
        if not is_boundary(boundary, wind):
            continue
        else:
            insert_boundary((boundary[0] - wind[0], boundary[1] - wind[1]))

minimal_structure = create_output(boundary_points)

# Maximal structure generation
while len(probable_boundary_points) != 0:
    prob_point = probable_boundary_points.pop()
    try:
        insert_boundary(prob_point)
    except Exception:
        confirmed_empty_points.add(prob_point)

maximal_structure = create_output(boundary_points)
write_output()
