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


take_input()
print_output()
# print(wind_direction)

# for key in wind_direction.keys():
#     for val in wind_direction[key]:
#         if val not in wind_direction

