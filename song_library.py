import os

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

MUSIC_DIR = os.path.expanduser("~/Downloads/Songs")
song_library = []


def load_songs():
    global song_library
    song_library.clear()

    for filename in os.listdir(MUSIC_DIR):
        if filename.endswith(".mp3"):
            filepath = os.path.join(MUSIC_DIR, filename)
            try:
                audio = MP3(filepath, ID3=EasyID3)
                song_library.append(
                    {
                        "title": audio.get("title", [os.path.splitext(filename)[0]])[0],
                        "artist": audio.get("artist", ["Unknown"])[0],
                        "duration": int(audio.info.length),
                        "file": filepath,
                    }
                )
            except Exception as e:
                print(f"Could not load {filename}: {e}")


def list_songs():
    if not song_library:
        print("No songs loaded")
        return []
    for i, song in enumerate(song_library, start=1):
        mins, secs = divmod(song["duration"], 60)
        print(f"{i}. {song['title']} - {song['artist']} ({mins}:{secs:02d})")
    return song_library


def filter_by_artist(artist):
    results = [s for s in song_library if artist.lower() in s["artist"].lower()]
    if not results:
        print("No songs found for that artist.")
        return []
    for i, song in enumerate(results, start=1):
        print(f"{i}. {song['title']} - {song['artist']}")
    return results
