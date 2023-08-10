dim_x, dim_y, no_wind_flow = 0, 0, 0
crystal = {}
wind_direction = {}


def take_input():
    with open('crystal_crosswind_input.txt', 'r') as file:
        global dim_x, dim_y, no_wind_flow, crystal, wind_direction
        dim_x, dim_y, no_wind_flow = [int(val) for val in file.readline().strip().split(' ')]
        crystal = {k: '.' for k in ((i, j) for i in range(1, dim_x + 1) for j in range(1, dim_y + 1))}
        for i in range(no_wind_flow):
            text = file.readline().strip().split()
            wind = tuple([int(n) for n in text[:2]])
            no_boundary = int(text[2])
            boundary = []
            for j in range(3, 2 * no_boundary + 3, 2):
                coordinate = tuple([int(n) for n in text[j: j + 2]])
                boundary.append(coordinate)
                crystal[coordinate] = '#'
            wind_direction[wind] = boundary


def print_output():
    for x in range(1, dim_y + 1):
        for y in range(1, dim_x + 1):
            print(crystal[(y, x)], end='')
        print('\n')


def violate_boundary(point):
    for wind in wind_direction.keys():
        if any([(val[0] - wind[0], val[1] - wind[1]) == point for val in wind_direction[wind]]):
            return True
    return False


def can_place(point):
    for wind in wind_direction.keys():
        diff_point = (point[0] - wind[0], point[1] - wind[1])
        if any([diff_point[0] <= 0 or diff_point[0] > dim_x, diff_point[1] <= 0 or diff_point[1] > dim_y]):
            return False, 0
        elif diff_point not in boundary:
            if diff_point in confirm_dot:
                return False, 1
            else:
                return False, 2
    else:
        return True, 1


take_input()

boundary = set()
for b in crystal.keys():
    if crystal[b] == '#':
        boundary.add(b)

for key in wind_direction.keys():
    boundary_set = set(wind_direction[key])
    not_in_set = boundary.difference(boundary_set)

    for b in not_in_set:
        p = (b[0] - key[0], b[1] - key[1])
        if p in boundary:
            continue
        else:
            crystal[p] = '#'

print('Minimal')
print_output()

not_boundary = set()
for b in crystal.keys():
    if crystal[b] == '.':
        not_boundary.add(b)

boundary = list(set(crystal.keys()).difference(not_boundary))
boundary.sort()

not_boundary = list(not_boundary)
not_boundary.sort()
confirm_dot = []

for nb in not_boundary:
    if violate_boundary(nb):
        confirm_dot.append(nb)
    else:
        logic, val = can_place(nb)
        if logic:
            boundary.append(nb)
            # not_boundary.remove(nb)
        else:
            if val == 0:
                confirm_dot.append(nb)
                # not_boundary.remove(nb)
            elif val == 1:
                confirm_dot.append(nb)
                # not_boundary.remove(nb)
            elif val == 2:
                not_boundary.append(nb)
            else:
                continue

for elem in boundary:
    crystal[elem] = '#'

print('Maximal')
print_output()
