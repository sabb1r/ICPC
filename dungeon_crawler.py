import networkx as nx
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(10000)


class Room:
    def __init__(self, room_number):
        self.room_number = room_number
        self.time = {}
        self.parent = None
        self.child = []
        self.link = set()
        self.cost = 0
        self.max_time = 0
        self.min_time = 0

    def add_link(self, room, time):
        self.link.add(room)
        room.link.add(self)
        self.time[(self.room_number, room.room_number)] = time
        room.time[room.room_number, self.room_number] = time

    def add_child(self, room):
        self.child.append(room)
        room.parent = self

    def __repr__(self):
        return 'Room {}'.format(self.room_number)


def make_root(root, parent):
    if not root:
        return
    temp = root.parent
    root.parent = parent
    if temp:
        root.child.append(temp)
    if parent:
        root.child.remove(parent)

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


def set_root(root):
    def order_tree(room):
        time_list = []

        if len(room.child) == 0:
            room.cost = 0

        for child in room.child:
            order_tree(child)
            time_list.append((child, child.cost))

        max_time_list = [(x[0], 2 * room.time[(room.room_number, x[0].room_number)] + x[0].max_time) for x in time_list]

        room.max_time = sum([x[1] for x in max_time_list])

        if len(time_list) == 1:
            room.min_time = room.time[(room.room_number, time_list[0][0].room_number)] + time_list[0][0].min_time

        elif time_list:
            min_time_list = []
            for k in range(len(max_time_list)):
                max_time_list_copied = max_time_list[:]
                r, t = max_time_list_copied.pop(k)
                sum_max_time = sum([x[1] for x in max_time_list_copied])
                min_time = room.time[(room.room_number, r.room_number)] + r.min_time + sum_max_time
                min_time_list.append((r, min_time))
            min_time_list.sort(key=lambda x: x[1])

            # if key_hole_different_branch and is_antecedent(min_time_list[0][0], key_room) and not is_antecedent(
            #         min_time_list[0][0], trap_room):
            #     #have to find out

            room.min_time = min_time_list[0][1]

        else:
            room.min_time = room.max_time

    order_tree(root)


def plot_tree(room):
    global G
    G.add_node(room.room_number)
    for ch in room.child:
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
        for ch in room1.child:
            if is_antecedent(ch, room2):
                return True
        return False


def time_to_key_room(room):
    def find_the_room(parent):
        if parent.room_number == room.room_number:
            return 0
        return parent.time[(parent.room_number, parent.parent.room_number)] + find_the_room(parent.parent)

    time = find_the_room(key_room)

    return time


def swap(prev_room_info, key_holding_room_info):
    # Have to edit
    prev_room = prev_room_info[1]
    key_holding_room = key_holding_room_info[1]

    dk = key_holding_room.time[(key_holding_room.room_number, key_holding_room.parent.room_number)]
    di = prev_room.time[(prev_room.room_number, prev_room.parent.room_number)]

    swapping_cost = key_holding_room_info[0] + di + prev_room.min_cost
    not_swapping_cost = prev_room_info[0] + 3 * dk + key_holding_room.min_cost

    if swapping_cost < not_swapping_cost:
        return True
    else:
        return False


def relative_position():
    global key_hole_same_branch, key_hole_different_branch, trap_precedes_key

    if is_antecedent(trap_room, key_room):
        trap_precedes_key = True
    elif is_antecedent(key_room, trap_room):
        key_hole_same_branch = True
    else:
        key_hole_different_branch = True


G = nx.Graph()
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
        if not starting_room.parent and not starting_room.child:
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

    set_root(starting_room)
    result.append(str(starting_room.min_time))



for val in result:
    print(val)
# write_output(result)

plot_tree(starting_room)
pos = nx.spring_layout(G, k=10)
nx.draw(G, pos, with_labels=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()
print('Distance to get to the key room from room {} is = {}'.format(dungeon[4], time_to_key_room(dungeon[4])))