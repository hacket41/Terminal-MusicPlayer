# Terminal Music Player 🎵

A **terminal-based music player** written in Python, supporting playlists, shuffle, queues, and party mode. Play your local MP3 library directly from the terminal.

---

## Features

- Browse your music library with song title, artist, and duration
- Filter songs by artist
- Add songs manually to the library
- Create custom playlists
- Recursive shuffle of library
- Queue songs to play next
- Party mode with priority-based upvotes
- View listening history
- Terminal UI with scrolling and Unicode support

---

## Requirements

- Python 3.10+
- [pygame](https://www.pygame.org/) (for audio playback)
- [mutagen](https://mutagen.readthedocs.io/) (for MP3 metadata)
- [wcwidth](https://pypi.org/project/wcwidth/) (for Unicode width handling)
- Linux/Arch tested (should work on Windows/Mac with minor path changes)
