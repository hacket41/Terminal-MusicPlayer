import curses

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


def build_artist_index():
    """Return a list of tuples: (display_str, song) where headers have None for song"""
    items = []
    grouped = {}
    for song in song_library:
        grouped.setdefault(song["artist"], []).append(song)
    for artist, songs in grouped.items():
        items.append((f"== {artist} ==", None))  # header
        for s in songs:
            items.append((f"{s['title']}", s))
    return items


def run_ui(stdscr):
    load_songs()
    curses.curs_set(0)
    cursor = 0
    offset = 0
    search_mode = False
    search_term = ""

    items = build_artist_index()

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        max_visible = height - 3

        stdscr.addstr(
            0,
            0,
            "🎵 Terminal Music Player - cmus-like (Enter=Play, Space=Pause, q=Quit)",
            curses.A_BOLD,
        )
        if search_mode:
            stdscr.addstr(1, 0, f"/{search_term}")
        else:
            stdscr.addstr(1, 0, f"{len(song_library)} songs loaded")

        # scrolling
        if cursor < offset:
            offset = cursor
        elif cursor >= offset + max_visible:
            offset = cursor - max_visible + 1

        for idx, (display_str, song) in enumerate(items[offset : offset + max_visible]):
            display_str = truncate_to_width(display_str, width - 3)
            if idx + offset == cursor:
                stdscr.addstr(idx + 2, 0, f"> {display_str}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 2, 0, f"  {display_str}")

        stdscr.refresh()
        k = stdscr.getch()

        if search_mode:
            if k in (curses.KEY_ENTER, 10, 13):
                search_mode = False
                # rebuild items based on search
                items = [
                    (f"{s['title']} - {s['artist']}", s)
                    for s in song_library
                    if search_term.lower() in s["title"].lower()
                    or search_term.lower() in s["artist"].lower()
                ]
                cursor = 0
                offset = 0
                search_term = ""
            elif k in (27,):  # Esc to cancel
                search_mode = False
                items = build_artist_index()
                cursor = 0
                offset = 0
                search_term = ""
            elif k in (curses.KEY_BACKSPACE, 127):
                search_term = search_term[:-1]
            else:
                search_term += chr(k)
            continue

        if k == ord("q"):
            break
        elif k == curses.KEY_UP and cursor > 0:
            cursor -= 1
        elif k == curses.KEY_DOWN and cursor < len(items) - 1:
            cursor += 1
        elif k == ord("\n"):
            _, song = items[cursor]
            if song:
                play_song(song)
        elif k == ord(" "):  # pause / resume
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
        elif k == curses.KEY_LEFT:  # rewind
            pos = pygame.mixer.music.get_pos() / 1000
            pygame.mixer.music.play(start=max(pos - REWIND_FORWARD_STEP, 0))
        elif k == curses.KEY_RIGHT:  # forward
            pos = pygame.mixer.music.get_pos() / 1000
            pygame.mixer.music.play(start=pos + REWIND_FORWARD_STEP)
        elif k == ord("/"):
            search_mode = True
            search_term = ""
