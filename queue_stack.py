import heapq
from collections import deque

import pygame

pygame.init()
pygame.mixer.init()

play_next_queue = deque()  # Queue
party_mode_heap = []  # Priority Queue
history_stack = []  # Stack


def play_song(song):
    if song:
        pygame.mixer.music.load(song["file"])
        pygame.mixer.music.play()
        print(f"▶️ Now Playing: {song['title']} - {song['artist']}")
        history_stack.append(song)


def play_next_feature(song):
    play_next_queue.append(song)
    print(f"📌 Queued to play next: {song['title']}")


def party_mode_upvote(song, priority):
    heapq.heappush(party_mode_heap, (-priority, song))
    print(f"🎉 '{song['title']}' upvoted with priority {priority}!")


def play_from_party_mode():
    if party_mode_heap:
        _, song = heapq.heappop(party_mode_heap)
        play_song(song)


def play_from_queue():
    if play_next_queue:
        song = play_next_queue.popleft()
        play_song(song)


def show_history():
    print("\n⏪ Listening History:")
    for song in reversed(history_stack):
        print(f"{song['title']} - {song['artist']}")
