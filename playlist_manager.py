from song_library import list_songs, song_library

playlists = {}


def add_song():
    title = input("Enter song title: ")
    artist = input("Enter artist: ")
    duration = int(input("Enter duration (sec): "))
    song_library.append(
        {"title": title, "artist": artist, "duration": duration, "file": None}
    )
    print(f"✅ Added '{title}' - {artist} to library")


def create_playlist():
    name = input("Enter playlist name: ")
    playlists[name] = []
    while True:
        list_songs()
        choice = input("Pick song number to add (or 'done'): ")
        if choice.lower() == "done":
            break
        try:
            playlists[name].append(song_library[int(choice) - 1])
            print(f"✅ Added {song_library[int(choice) - 1]['title']}")
        except:
            print("Invalid choice")
    print(f"🎶 Playlist '{name}' created with {len(playlists[name])} songs")

