import curses

from terminal_ui import run_ui

if __name__ == "__main__":
    curses.wrapper(run_ui)
