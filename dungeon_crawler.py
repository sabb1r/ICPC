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
