import networkx as nx
import matplotlib.pyplot as plt


class Room:
    def __init__(self, room_number):
        self.room_number = room_number
        self.edge = set()
        self.time = {}

    def add_link(self, room, time):
        self.edge.add(room)
        room.edge.add(self)
        self.time[(self.room_number, room.room_number)] = time
        room.time[room.room_number, self.room_number] = time


def time_counter(room):
    if len(room.edge) == 0:
        return 0
    else:
        time = 0
        for e in room.edge:
            time += room.time[(room.room_number, e.room_number)] + time_counter(e)
    return time


def show_path(room_from, room_to, room_throgh=None):
    """
    :param room_from: A room object
    :param room_to: A room object
    :param room_throgh: A room object
    :return: True - if I have to face "room_through" while going from "room_from" to "room_to"
    """

    if len(room_from.edge) == 0:
        return []
    else:
        path = []
        for e in room_from.edge:
            path.append(e)
            if e.room_number == room_to.room_number:
                return path
            else:
                path.append(show_path(e, room_to, room_throgh=None))


def plot_tree(room):
    global G
    G.add_node(room.room_number)
    for e in room.edge:
        G.add_edge(room.room_number, e.room_number)
        plot_tree(e)


room1 = Room(1)
room2 = Room(2)
room3 = Room(3)
room4 = Room(4)
room5 = Room(5)
G = nx.Graph()

room1.add_link(room2, 5)
room1.add_link(room3, 1)
room3.add_link(room4, 3)
room3.add_link(room5, 2)


plot_tree(room1)
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
