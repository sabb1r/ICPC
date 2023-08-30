import sys
import time

start_time = time.time()
sys.setrecursionlimit(10000)


class Room:
    def __init__(self, room_number):
        self.room_number = room_number
        self.time = {}
        self.parent = None
        self.children = []
        self.link = set()
        self.cost = 0
        self.max_time = 0
        self.min_time = 0

    def add_link(self, room, time):
        self.link.add(room)
        room.link.add(self)
        self.time[(self, room)] = time
        room.time[(room, self)] = time

    def add_child(self, room):
        self.children.append(room)
        room.parent = self

    def __repr__(self):
        return 'Room {}'.format(self.room_number)


def make_root(root, parent):
    previous_parent = []

    def root_setup(root, parent):

        if not root:
            return
        else:
            temp = root.parent
            root.parent = parent
            if temp:
                root.children.append(temp)
                previous_parent.append(temp)
            if parent:
                root.children.remove(parent)

        root_setup(temp, root)

    root_setup(root, parent)
    return previous_parent


def initial_root_setup(root):
    if not root.parent:
        root.parent = None

    if not root.parent:
        children = root.link
    else:
        children = root.link.difference({root.parent})

    if not children:
        return

    for child in children:
        root.add_child(child)
        initial_root_setup(child)


def calculate_time(room):
    global previous_parent, same_as_before
    time_list = []

    if len(room.children) == 0:
        room.cost = 0

    # for child in room.children:
    #     calculate_time(child)
    #     time_list.append((child, child.cost))

    for child in room.children:
        if not same_as_before:
            if child in previous_parent:
                time_list.append((child, child.max_time))
                continue
            else:
                calculate_time(child)
                time_list.append((child, child.cost))
        else:
            calculate_time(child)
            time_list.append((child, child.cost))

    max_time_list = [(x[0], 2 * room.time[(room, x[0])] + x[0].max_time) for x in time_list]

    room.max_time = sum([x[1] for x in max_time_list])

    if len(time_list) == 1:
        room.min_time = room.time[(room, time_list[0][0])] + time_list[0][0].min_time
        room.end_room = time_list[0][0]

    elif time_list:
        min_time_list = []
        for rm in max_time_list:
            val = room.time[(room, rm[0])] + rm[0].max_time - rm[0].min_time
            min_time_list.append([rm[0], val])
        min_time_list.sort(key=lambda x: x[1])

        if key_hole_different_branch:
            if is_antecedent(min_time_list[-1][0], key_room) and is_antecedent(room, trap_room) and not is_antecedent(
                    min_time_list[-1][0], trap_room):
                swappable(min_time_list, room)

        room.min_time = room.max_time - min_time_list[-1][1]
        room.end_room = min_time_list[-1][0]

    else:
        room.min_time = room.max_time
        room.end_room = room


def take_input():
    with open(sys.argv[1], 'r') as file:
    # with open('dungeon_crawler_input.txt', 'r') as file:
        total_room, total_scenario = list(map(int, file.readline().strip().split(' ')))
        dungeon = [None] + [Room(i) for i in range(1, total_room + 1)]
        for i in range(total_room - 1):
            room1, room2, time = list(map(int, file.readline().strip().split(' ')))
            dungeon[room1].add_link(dungeon[room2], time)

        scenario = []
        for i in range(total_scenario):
            scenario.append(list(map(int, file.readline().strip().split(' '))))

    return dungeon, scenario


def write_output(result):
    with open(sys.argv[2] + sys.argv[1].split('/')[-1].split('.')[0] + '.ans', 'w') as file:
        file.writelines([val + '\n' for val in result])


def is_antecedent(room1, room2):
    if room1.room_number == room2.room_number:
        return True
    else:
        for ch in room1.children:
            if is_antecedent(ch, room2):
                return True
        return False


def time_to_reach_room(from_room, to_room):
    nodes = []

    def find_the_room(parent):
        nodes.append(parent)
        if parent.room_number == from_room.room_number:
            return 0
        return parent.time[(parent, parent.parent)] + find_the_room(parent.parent)

    time = find_the_room(to_room)
    nodes = nodes[::-1]

    return time, nodes


def relative_position():
    global key_hole_same_branch, key_hole_different_branch, trap_precedes_key, key_room, trap_room

    if is_antecedent(trap_room, key_room):
        trap_precedes_key = True
    elif is_antecedent(key_room, trap_room):
        key_hole_same_branch = True
    else:
        key_hole_different_branch = True


def min_time_node(key_time, nodes, first_room):
    branches = []
    costs = []
    for node in nodes[:-1]:
        for child in node.children:
            if child in nodes:
                continue
            branches.append([node, child])
            costs.append([node, 2 * node.time[(node, child)] + child.max_time])

    if not branches:
        return 3 * key_time + key_room.min_time

    tmax = sum([x[1] for x in costs]) + 2 * key_time + key_room.max_time

    flag = 100000000000000000

    for ind, branch in enumerate(branches):
        t = tmax - costs[ind][1] + time_to_reach_room(first_room, branch[1])[0] + branch[1].min_time
        if t < flag:
            flag = t

    return flag


def swappable(min_time_list, room):
    time_if_swap = room.max_time - min_time_list[-2][1]

    key_time, nodes = time_to_reach_room(min_time_list[-1][0], key_room)

    key_time += nodes[0].time[(nodes[0], nodes[0].parent)]

    time_if_not_swap = min_time_node(key_time, nodes, room)

    final_list = [2 * room.time[(room, child)] + child.max_time for child in room.children if
                  child.room_number != min_time_list[-1][0].room_number]

    time_if_not_swap += sum(final_list)

    if time_if_swap < time_if_not_swap:
        temp = min_time_list[-1]
        min_time_list[-1] = min_time_list[-2]
        min_time_list[-2] = temp

    else:
        val = room.max_time - time_if_not_swap
        min_time_list[-1][1] = val


dungeon, scenario = take_input()
result = []

for ind, scene in enumerate(scenario):
    key_hole_different_branch = False
    key_hole_same_branch = False
    trap_precedes_key = False
    same_as_before = True

    starting_room = dungeon[scene[0]]
    key_room = dungeon[scene[1]]
    trap_room = dungeon[scene[2]]

    if starting_room.room_number != dungeon[scenario[ind - 1][0]]:
        if not starting_room.parent and not starting_room.children:
            initial_root_setup(starting_room)
        else:
            if result[-1] != 'impossible':
                same_as_before = True
            previous_parent = make_root(starting_room, None)

    relative_position()

    if trap_precedes_key:
        result.append('impossible')
        continue

    calculate_time(starting_room)
    result.append(str(starting_room.min_time))

# for val in result:
#     print(val)
print('Time Required: ', time.time() - start_time)
write_output(result)
