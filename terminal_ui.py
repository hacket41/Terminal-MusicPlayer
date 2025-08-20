import curses

from wcwidth import wcswidth

from queue_stack import play_song
from song_library import load_songs, song_library


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


def run_ui(stdscr):
    load_songs()
    curses.curs_set(0)
    cursor = 0
    offset = 0  # for scrolling

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        max_visible = height - 3  # leave space for header/footer

        stdscr.addstr(
            0,
            0,
            "🎵 Terminal Music Player - cmus-like (Enter=Play, q=Quit)",
            curses.A_BOLD,
        )

        if not song_library:
            stdscr.addstr(2, 0, "No songs loaded")
        else:
            # adjust offset for scrolling
            if cursor < offset:
                offset = cursor
            elif cursor >= offset + max_visible:
                offset = cursor - max_visible + 1

            for idx, song in enumerate(song_library[offset : offset + max_visible]):
                display_str = f"{song['title']} - {song['artist']}"
                display_str = truncate_to_width(display_str, width - 3)
                if idx + offset == cursor:
                    stdscr.addstr(idx + 2, 0, f"> {display_str}", curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 2, 0, f"  {display_str}")

        stdscr.refresh()
        k = stdscr.getch()

        if k == ord("q"):
            break
        elif k == curses.KEY_UP and cursor > 0:
            cursor -= 1
        elif k == curses.KEY_DOWN and cursor < len(song_library) - 1:
            cursor += 1
        elif k == ord("\n"):
            play_song(song_library[cursor])
