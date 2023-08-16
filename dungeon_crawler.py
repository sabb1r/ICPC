import networkx as nx
import matplotlib.pyplot as plt


class Room:
    def __init__(self, room_number):
        self.room_number = room_number
        self.parent = set()
        self.child = set()
        self.time = {}

    def add_child(self, room, time):
        self.child.add(room)
        room.parent.add(self)
        self.time[(self.room_number, room.room_number)] = time


def time_counter(room):
    if len(room.child) == 0:
        return 0
    else:
        time = 0
        for ch in room.child:
            time += room.time[(room.room_number, ch.room_number)] + time_counter(ch)
    return time


def plot_tree(room):
    global G
    G.add_node(room.room_number)
    for ch in room.child:
        G.add_edge(room.room_number, ch.room_number)
        plot_tree(ch)


room1 = Room(1)
room2 = Room(2)
room3 = Room(3)
room4 = Room(4)
room5 = Room(5)
G = nx.Graph()

room1.add_child(room2, 5)
room1.add_child(room3, 1)
room3.add_child(room4, 3)
room3.add_child(room5, 2)

print(time_counter(room3))
plot_tree(room1)
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
