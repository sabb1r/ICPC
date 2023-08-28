# import networkx as nx
# import matplotlib.pyplot as plt
import sys

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

    # def __eq__(self, other):
    #     if self.room_number == other.room_number:
    #         return True
    #     else:
    #         return False

    def add_link(self, room, time):
        self.link.add(room)
        room.link.add(self)
        self.time[(self.room_number, room.room_number)] = time
        room.time[room.room_number, self.room_number] = time

    def add_child(self, room):
        self.children.append(room)
        room.parent = self

    def __repr__(self):
        return 'Room {}'.format(self.room_number)


def make_root(root, parent):
    if not root:
        return
    temp = root.parent
    root.parent = parent
    if temp:
        root.children.append(temp)
    if parent:
        root.children.remove(parent)

    make_root(temp, root)


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
    time_list = []

    if len(room.children) == 0:
        room.cost = 0

    for child in room.children:
        calculate_time(child)
        time_list.append((child, child.cost))

    max_time_list = [(x[0], 2 * room.time[(room.room_number, x[0].room_number)] + x[0].max_time) for x in time_list]

    room.max_time = sum([x[1] for x in max_time_list])

    if len(time_list) == 1:
        room.min_time = room.time[(room.room_number, time_list[0][0].room_number)] + time_list[0][0].min_time
        room.end_room = time_list[0][0]

    elif time_list:
        min_time_list = []
        for rm in max_time_list:
            # max_time_list_copied = max_time_list[:]
            # r, t = max_time_list_copied.pop(k)
            # sum_max_time = sum([x[1] for x in max_time_list_copied])
            # min_time = room.time[(room.room_number, r.room_number)] + r.min_time + sum_max_time
            # min_time_list.append((r, min_time))
            val = room.time[(room.room_number, rm[0].room_number)] + rm[0].max_time - rm[0].min_time
            min_time_list.append((rm[0], val))
        min_time_list.sort(key=lambda x: x[1])

        if key_hole_different_branch:
            if is_antecedent(min_time_list[0][0], key_room) and is_antecedent(room, trap_room) and not is_antecedent(
                    min_time_list[0][0], trap_room):
                swappable(min_time_list, room)

        room.min_time = room.max_time - min_time_list[-1][1]
        room.end_room = min_time_list[-1][0]

    else:
        room.min_time = room.max_time
        room.end_room = room


def plot_tree(room):
    global G
    G.add_node(room.room_number)
    for ch in room.children:
        G.add_edge(room.room_number, ch.room_number, weight=room.time[(room.room_number, ch.room_number)])
        plot_tree(ch)


def take_input():
    # with open(sys.argv[1], 'r') as file:
    with open('dungeon_crawler_input.txt', 'r') as file:
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
        return parent.time[(parent.room_number, parent.parent.room_number)] + find_the_room(parent.parent)

    time = find_the_room(to_room)

    return time, nodes


def relative_position():
    global key_hole_same_branch, key_hole_different_branch, trap_precedes_key, key_room, trap_room

    if is_antecedent(trap_room, key_room):
        trap_precedes_key = True
    elif is_antecedent(key_room, trap_room):
        key_hole_same_branch = True
    else:
        key_hole_different_branch = True


def swappable(min_time_list, room):
    time_if_swap = min_time_list[-1][1]

    key_time, nodes = time_to_reach_room(room, key_room)
    branches = []

    tmax = 0
    for node in nodes:
        time_to_node = time_to_reach_room(room, node)
        branch = []
        for child in node.children:
            if child in nodes:
                continue
            t = 2 * node.time[(node.room_number, child.room_number)] + child.max_time
            tmax += t
            branch.append(child)
        branches.append([node, branch])



    for i in range(len(branches)):
        for ind, sub_branch in enumerate(branches[i][1]):
            maximum_time = 2 * branch[0].time[(branch[0].room_number, sub_branch.room_number)] + sub_branch.max_time
            branches[i][1][ind] = maximum_time

    mod_branches = [[x[0], sum(x[1])] for x in branches]
    mod_branches.sort(key=lambda x: x[1])

    # def get_key(room):
    #     # nonlocal time_to_get_key
    #     if not is_antecedent(room.end_room, key_room) or room.room_number == key_room.room_number:
    #         return room.min_time
    #         # return room.max_time
    #     return 2 * room.time[(room.room_number, room.end_room.room_number)] + get_key(room.end_room)
    #
    # time_to_get_key = 2 * room.time[(room.room_number, min_time_list[0][0].room_number)] + get_key(min_time_list[0][0])
    # # time_to_get_key = 2 * room.time[(room.room_number, min_time_list[0][0].room_number)] + get_key(min_time_list[0][0])
    #
    # # time_if_not_swap = time_to_get_key + min_time_list[0][1] - (room.time[(room.room_number, min_time_list[0][0].room_number)] + min_time_list[0][0].min_time)
    # time_if_not_swap = room.min_time + time_to_get_key + min_time_list[0][1]

    # if time_if_swap < time_if_not_swap:
    #     temp = min_time_list[0]
    #     min_time_list[0] = min_time_list[1]
    #     min_time_list[1] = temp
    # else:
    #     min_time_list[0] = (min_time_list[0][0], time_if_not_swap)


# G = nx.Graph()
dungeon, scenario = take_input()
result = []

for ind, scene in enumerate(scenario):
    relative_position_detected = False
    key_hole_different_branch = False
    key_hole_same_branch = False
    trap_precedes_key = False

    starting_room = dungeon[scene[0]]
    key_room = dungeon[scene[1]]
    trap_room = dungeon[scene[2]]

    if starting_room.room_number != dungeon[scenario[ind - 1][0]]:
        if not starting_room.parent and not starting_room.children:
            initial_root_setup(starting_room)
        else:
            make_root(starting_room, None)

    relative_position()

    if trap_precedes_key:
        result.append('impossible')
        continue

    if key_hole_different_branch:
        result.append('have to improvised')
        continue

    calculate_time(starting_room)
    result.append(str(starting_room.min_time))

for val in result:
    print(val)
# write_output(result)

# plot_tree(starting_room)
# pos = nx.spring_layout(G, k=10)
# nx.draw(G, pos, with_labels=True)
# labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
# plt.show()
# print('Distance to get to the key room from room {} is = {}'.format(dungeon[5], time_to_key_room(dungeon[5])))
