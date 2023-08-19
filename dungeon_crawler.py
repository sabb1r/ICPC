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

    def add_link(self, room, time):
        self.edge.add(room)
        room.edge.add(self)
        # room.time = time
        self.time[(self.room_number, room.room_number)] = time
        room.time[room.room_number, self.room_number] = time

    def __repr__(self):
        return 'Room {}'.format(self.room_number)


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
        room.parent = None
        room.child.clear()
        room.cost = 0

    def order_tree(room):
        for ch in room.edge:
            if ch == room.parent:
                continue
            room.child.add(ch)
            ch.parent = room
            ch.cost = ch.parent.cost + ch.time[(ch.room_number, ch.parent.room_number)]
            order_tree(ch)

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


G = nx.Graph()
dungeon, scenario = take_input()

for ind, scene in enumerate(scenario):
    starting_room = dungeon[scene[0]]
    key_room = dungeon[scene[1]]
    trap_room = dungeon[scene[2]]

    if ind == 0 or starting_room.room_number != dungeon[scenario[ind - 1][0]]:
        set_root(starting_room)

    if is_antecedent(trap_room, key_room):
        print('Impossible')
    else:
        print('Possible')
    # elif is_antecedent(key_room, trap_room):
    #     times = [(room, time_counter(room)) for room in starting_room.child]
    #     times.sort(key=lambda x: x[1][0])
    #     if len(times) == 1:
    #         least_time = times[0][1][0]
    #     else:
    #         least_time = sum([t[1] for t in times[:-1]]) + times[-1][1]
    #     # times.sort(key=lambda x:x[1])
    #     # if len(times) == 1:
    #     #     least_time = times[-1][1]
    #     # else:
    #     #     least_time = [x * 2 for x in times[:-1][1]] + times[-1][1]
    #     print(least_time)
    # else:
    #     print('have to think how to solve')

    # print(starting_room)
    # for room in dungeon[1:]:
    #     print(room, room.cost)

    # plot_tree(starting_room)
    # pos = nx.spring_layout(G, k=10)
    # nx.draw(G, pos, with_labels=True)
    # labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    # plt.show()
