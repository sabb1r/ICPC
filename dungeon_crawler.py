import networkx as nx
import matplotlib.pyplot as plt


class Room:
    def __init__(self, room_number):
        self.room_number = room_number
        self.edge = set()
        self.time = {}
        self.parent = None
        self.child = set()
        self.cost = 0
        self.max_cost = 0
        self.min_cost = 0

    def add_link(self, room, time):
        self.edge.add(room)
        room.edge.add(self)
        # room.time = time
        self.time[(self.room_number, room.room_number)] = time
        room.time[room.room_number, self.room_number] = time

    def __repr__(self):
        return 'Room {}'.format(self.room_number)

    def clear(self):
        self.parent = None
        self.child = set()
        self.cost = 0
        self.max_cost = 0
        self.min_cost = 0


def time_counter(room):
    if len(room.child) == 0:
        tmin = room.time[(room.room_number, room.parent.room_number)]
        tmax = 2 * tmin
        return tmin, tmax
    else:
        time = []
        for ch in room.child:
            time.append(time_counter(ch))
        time.sort()
        tmax = sum([x[1] for x in time])
        tmin = sum(x[1] for x in time[:-1]) + time[-1][0]
    return tmin, tmax


def set_root(root):
    for room in dungeon[1:]:
        room.clear()

    def order_tree(room):
        t = []
        if len(room.edge) == 1:
            room.cost = 0

        for ch in room.edge:
            if ch == room.parent:
                continue
            room.child.add(ch)
            ch.parent = room
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
            if key_hole_different_branch:
                if is_antecedent(test_largest[1], key_room):
                    temp = test_largest
                    test_largest = test_smaller.pop()
                    test_smaller.append(temp)
            cost_min = sum([x[0] for x in test_smaller]) + test_largest[1].min_cost + room.time[(room.room_number, test_largest[1].room_number)]
            room.min_cost = cost_min
        else:
            room.min_cost = room.max_cost

    order_tree(root)


def show_path(room_from, room_to, room_throgh=None):
    """
    :param room_from: A room object
    :param room_to: A room object
    :param room_through: A room object
    :return: True - if I have to face "room_through" while going from "room_from" to "room_to"
    """

    if len(room_from.edge) == 1:
        return []
    else:
        path = []
        for e in room_from.edge.difference(room_from.parent):
            path.append(e)
            if e.room_number == room_to.room_number:
                return path
            else:
                e.parent.add(room_from)
                room = show_path(e, room_to, room_throgh=None)
                if len(room) != 0 and room[-1].room_number == room_to.room_number:
                    path.append(room)
                    return path

            path.clear()


def plot_tree(room):
    global G
    G.add_node(room.room_number)
    for ch in room.child:
        G.add_edge(room.room_number, ch.room_number, weight=room.time[(room.room_number, ch.room_number)])
        plot_tree(ch)


def take_input():
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


def is_antecedent(room1, room2):
    if room1.room_number == room2.room_number:
        return True
    else:
        for ch in room1.child:
            if is_antecedent(ch, room2):
                return True
        return False


def location():
    pass


G = nx.Graph()
dungeon, scenario = take_input()

for ind, scene in enumerate(scenario):
    key_hole_different_branch = False
    starting_room = dungeon[scene[0]]
    key_room = dungeon[scene[1]]
    trap_room = dungeon[scene[2]]

    if ind == 0 or starting_room.room_number != dungeon[scenario[ind - 1][0]]:
        set_root(starting_room)

    if is_antecedent(trap_room, key_room):
        print('Impossible')

    elif is_antecedent(key_room, trap_room):
        least_time = starting_room.min_cost
        print(least_time)

    else:
        key_hole_different_branch = True
        set_root(starting_room)
        least_time = starting_room.min_cost
        print(least_time)

    # print(starting_room)
    # print(starting_room.max_cost, starting_room.min_cost)

    # plot_tree(starting_room)
    # pos = nx.spring_layout(G, k=10)
    # nx.draw(G, pos, with_labels=True)
    # labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    # plt.show()
