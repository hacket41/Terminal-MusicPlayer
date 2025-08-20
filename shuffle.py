# Recursive shuffle (Week 2)
import random


def recursive_shuffle(songs):
    if len(songs) <= 1:
        return songs
    mid = random.randint(0, len(songs) - 1)
    return [songs[mid]] + recursive_shuffle(songs[:mid] + songs[mid + 1 :])
