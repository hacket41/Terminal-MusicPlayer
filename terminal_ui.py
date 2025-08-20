import curses
from collections import defaultdict

from wcwidth import wcswidth

from queue_stack import play_song, pygame
from song_library import load_songs, song_library

REWIND_FORWARD_STEP = 5  # seconds


def truncate_to_width(text, width):
    result = ""
    total_width = 0
    for c in text:
        w = wcswidth(c)
        if total_width + w > width:
            return result + "..."
        result += c
        total_width += w
    return result


def build_artist_group():
    grouped = defaultdict(list)
    for song in song_library:
        grouped[song["artist"]].append(song)
    return dict(sorted(grouped.items()))  # sorted by artist


def run_ui(stdscr):
    load_songs()
    curses.curs_set(0)
    stdscr.nodelay(False)

    grouped = build_artist_group()
    artists = list(grouped.keys())
    current_artist_idx = 0
    current_song_idx = 0
    in_songs_pane = False
    search_mode = False
    search_term = ""
    songs_filtered = []

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        artist_width = min(25, width // 3)
        right_start = artist_width + 2
        songs_of_artist = (
            grouped[artists[current_artist_idx]] if not search_mode else songs_filtered
        )

        # Header
        stdscr.addstr(0, 0, "🎵 Terminal Music Player - cmus-like", curses.A_BOLD)
        stdscr.addstr(
            1,
            0,
            f"Artists: {len(artists)} | Songs: {len(song_library)} | Press '/' to search | 'q' to quit",
        )

        if search_mode:
            stdscr.addstr(2, 0, f"/{search_term}")

        # Draw artists pane
        for idx, artist in enumerate(artists[: height - 3]):
            display = truncate_to_width(artist, artist_width)
            if idx == current_artist_idx and not in_songs_pane and not search_mode:
                stdscr.addstr(idx + 3, 0, display.ljust(artist_width), curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 3, 0, display.ljust(artist_width))

        # Draw songs pane
        for idx, song in enumerate(songs_of_artist[: height - 3]):
            display = truncate_to_width(song["title"], width - right_start - 1)
            if idx == current_song_idx and in_songs_pane:
                stdscr.addstr(idx + 3, right_start, display, curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 3, right_start, display)

        stdscr.refresh()
        k = stdscr.getch()

        if search_mode:
            if k in (curses.KEY_ENTER, 10, 13):
                # finish search
                songs_filtered = [
                    s
                    for s in song_library
                    if search_term.lower() in s["title"].lower()
                    or search_term.lower() in s["artist"].lower()
                ]
                in_songs_pane = True
                current_song_idx = 0
                search_mode = False
            elif k in (27,):  # Esc to cancel
                search_mode = False
            elif k in (curses.KEY_BACKSPACE, 127):
                search_term = search_term[:-1]
            else:
                try:
                    search_term += chr(k)
                except:
                    pass
            continue

        # Global controls
        if k == ord("q"):
            break
        elif k == ord("/"):
            search_mode = True
            search_term = ""
        elif not in_songs_pane:
            if k == curses.KEY_UP and current_artist_idx > 0:
                current_artist_idx -= 1
                current_song_idx = 0
            elif k == curses.KEY_DOWN and current_artist_idx < len(artists) - 1:
                current_artist_idx += 1
                current_song_idx = 0
            elif k == curses.KEY_RIGHT:
                in_songs_pane = True
        else:
            songs_of_artist = (
                grouped[artists[current_artist_idx]]
                if not search_mode
                else songs_filtered
            )
            if k == curses.KEY_UP and current_song_idx > 0:
                current_song_idx -= 1
            elif k == curses.KEY_DOWN and current_song_idx < len(songs_of_artist) - 1:
                current_song_idx += 1
            elif k == curses.KEY_LEFT:
                in_songs_pane = False
            elif k == ord("\n"):
                play_song(songs_of_artist[current_song_idx])
            elif k == ord(" "):
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif k == curses.KEY_LEFT:
                pos = pygame.mixer.music.get_pos() / 1000
                pygame.mixer.music.play(start=max(pos - REWIND_FORWARD_STEP, 0))
            elif k == curses.KEY_RIGHT:
                pos = pygame.mixer.music.get_pos() / 1000
                pygame.mixer.music.play(start=pos + REWIND_FORWARD_STEP)
