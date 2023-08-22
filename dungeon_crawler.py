# import networkx as nx
import matplotlib.pyplot as plt
import sys


class Room:
    def __init__(self, room_number):
        self.room_number = room_number
        self.edge = []
        self.time = {}
        self.parent = None
        self.child = []
        self.cost = 0
        self.max_cost = 0
        self.min_cost = 0

    def add_link(self, room, time):
        self.child.append(room)
        room.parent = self
        # room.time = time
        self.time[(self.room_number, room.room_number)] = time
        room.time[room.room_number, self.room_number] = time

    def __repr__(self):
        return 'Room {}'.format(self.room_number)

    def clear(self):
        self.parent = None
        self.child.clear()
        self.cost = 0
        self.max_cost = 0
        self.min_cost = 0


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


def set_root(root):
    # for room in dungeon[1:]:
    #     room.clear()

    def order_tree(room):
        global faced_key_room, faced_trap_room, relative_position_detected
        t = []

        # if not relative_position_detected:
        #     if room.room_number == key_room.room_number:
        #         faced_key_room = True
        #     if room.room_number == trap_room.room_number:
        #         faced_trap_room = True
        #
        #     if faced_key_room and faced_trap_room:
        #         relative_position()

        if len(room.child) == 0:
            room.cost = 0

        for ch in room.child:
            # if ch == room.parent:
            #     continue
            # room.child.append(ch)
            # ch.parent = room

            order_tree(ch)
            t.append((ch.cost, ch))

        test = [((2 * room.time[(room.room_number, x[1].room_number)] + x[1].max_cost), x[1]) for x in t]
        test = sorted(test, key=lambda x: x[0])

        room.max_cost = sum([x[0] for x in test])

        if len(t) == 1:
            room.min_cost = room.time[(room.room_number, t[0][1].room_number)] + t[0][1].min_cost
        elif t:
            test_smaller = test[:-1]
            test_largest = test[-1]

            multiplier = 1

            if key_hole_different_branch and is_antecedent(test_largest[1], key_room) and not is_antecedent(
                    test_largest[1], trap_room):
                if not swap(test_smaller[-1], test_largest):
                    multiplier = 3
                else:
                    temp = test_largest
                    test_largest = test_smaller.pop()
                    test_smaller.append(temp)
            cost_min = sum([x[0] for x in test_smaller]) + test_largest[1].min_cost + multiplier * room.time[
                (room.room_number, test_largest[1].room_number)]
            room.min_cost = cost_min
        else:
            room.min_cost = room.max_cost

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


def swap(prev_room_info, key_holding_room_info):
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
    global key_hole_same_branch, key_hole_different_branch, relative_position_detected, trap_precedes_key

    relative_position_detected = True

    if is_antecedent(trap_room, key_room):
        trap_precedes_key = True
        # raise Exception
    elif is_antecedent(key_room, trap_room):
        key_hole_same_branch = True
    else:
        key_hole_different_branch = True


# G = nx.Graph()
dungeon, scenario = take_input()
result = []

for ind, scene in enumerate(scenario):
    relative_position_detected = False
    key_hole_different_branch = False
    key_hole_same_branch = False
    trap_precedes_key = False
    # faced_key_room = False
    # faced_trap_room = False

    starting_room = dungeon[scene[0]]
    key_room = dungeon[scene[1]]
    trap_room = dungeon[scene[2]]

    if starting_room.room_number != dungeon[1].room_number or (ind > 1 and starting_room.room_number != dungeon[scenario[ind - 1][0]]):
        make_root(starting_room, None)

    relative_position()

    if trap_precedes_key:
        result.append('impossible')
        continue

    set_root(starting_room)
    result.append(str(starting_room.min_cost))
    # print(result, scene)

    # except Exception:
    #     result.append('impossible')
print(result)
# write_output(result)

# plot_tree(starting_room)
# pos = nx.spring_layout(G, k=10)
# nx.draw(G, pos, with_labels=True)
# labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
# plt.show()
