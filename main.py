from playlist_manager import add_song, create_playlist
from queue_stack import (
    party_mode_upvote,
    play_from_party_mode,
    play_from_queue,
    play_next_feature,
    show_history,
)
from shuffle import recursive_shuffle

from song_library import filter_by_artist, list_songs, load_songs, song_library


def main():
    load_songs()  # 👈 load songs from ~/Downloads/Songs at start

    while True:
        print("\n--- Music Playlist Manager ---")
        print("1. View Library")
        print("2. Filter by Artist")
        print("3. Add Song (manual)")
        print("4. Create Playlist")
        print("5. Shuffle Library (Recursive)")
        print("6. Play Next (Queue)")
        print("7. Party Mode Upvote (Priority Queue)")
        print("8. Play From Party Mode")
        print("9. Play From Queue")
        print("10. Show History (Stack)")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            list_songs()
        elif choice == "2":
            artist = input("Enter artist name: ")
            songs = filter_by_artist(artist)
            for s in songs:
                print(f"{s['title']} - {s['artist']}")
        elif choice == "3":
            add_song()
        elif choice == "4":
            create_playlist()
        elif choice == "5":
            shuffled = recursive_shuffle(song_library[:])
            print("🔀 Shuffled Songs:")
            for s in shuffled:
                print(f"{s['title']} - {s['artist']}")
        elif choice == "6":
            list_songs()
            idx = int(input("Pick song number: ")) - 1
            play_next_feature(song_library[idx])
        elif choice == "7":
            list_songs()
            idx = int(input("Pick song number: ")) - 1
            priority = int(input("Enter priority (1-10): "))
            party_mode_upvote(song_library[idx], priority)
        elif choice == "8":
            play_from_party_mode()
        elif choice == "9":
            play_from_queue()
        elif choice == "10":
            show_history()
        elif choice == "0":
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
