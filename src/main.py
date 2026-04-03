"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Explicit user profile (the "ground truth" preferences we compare songs against).
    user_profile = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }
    user_prefs = {
        "genre": user_profile["favorite_genre"],
        "mood": user_profile["favorite_mood"],
        "energy": user_profile["target_energy"],
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for i, rec in enumerate(recommendations, start=1):
        song, score, reasons = rec
        print(f"{i}. {song['title']}")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        for line in reasons:
            print(f"   - {line}")
        print()


if __name__ == "__main__":
    main()
