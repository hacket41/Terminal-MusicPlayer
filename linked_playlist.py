class Node:
    def __init__(self, song):
        self.song = song
        self.next = None
        self.prev = None


class PlaylistLinkedList:
    def __init__(self):
        self.head = None
        self.current = None

    def add_song(self, song):
        new_node = Node(song)
        if not self.head:
            self.head = new_node
            self.current = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node
            new_node.prev = temp

    def play_next(self):
        if self.current and self.current.next:
            self.current = self.current.next
        return self.current.song if self.current else None

    def play_prev(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        return self.current.song if self.current else None

