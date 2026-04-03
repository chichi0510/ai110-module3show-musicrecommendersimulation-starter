"""
Command line runner for the Music Recommender Simulation.

Stress-tests three distinct user profiles, then runs a weight-shift experiment.
"""

from typing import Any, Dict, List

from src.recommender import load_songs, recommend_songs

# --- Stress-test profiles (clearly different tastes) ---
PROFILES: List[Dict[str, Any]] = [
    {
        "name": "High-Energy Pop",
        "description": "Upbeat pop, happy mood, high target energy",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
    },
    {
        "name": "Chill Lofi",
        "description": "Lofi + chill mood, low target energy",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.36,
    },
    {
        "name": "Deep Intense Rock",
        "description": "Rock + intense mood, high target energy",
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
    },
]


def _print_banner(title: str, subtitle: str = "") -> None:
    print()
    print("=" * 64)
    print(title)
    if subtitle:
        print(subtitle)
    print("=" * 64)


def print_top_k(
    title: str,
    user_prefs: Dict[str, Any],
    songs: List[Dict[str, Any]],
    k: int = 5,
    **score_kwargs: Any,
) -> None:
    _print_banner(title)
    recommendations = recommend_songs(user_prefs, songs, k=k, **score_kwargs)
    print("\nTop recommendations:\n")
    for i, rec in enumerate(recommendations, start=1):
        song, score, reasons = rec
        print(f"{i}. {song['title']}")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        for line in reasons:
            print(f"   - {line}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for p in PROFILES:
        user_prefs = {"genre": p["genre"], "mood": p["mood"], "energy": p["energy"]}
        print_top_k(
            f"Profile: {p['name']}\n{p['description']}",
            user_prefs,
            songs,
            k=5,
        )

    # --- Sensitivity experiment: shift weight toward energy (Option A) ---
    lofi_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.36}
    print_top_k(
        "Experiment — Chill Lofi user, DEFAULT weights\n"
        "(genre +2.0, mood +1.0, energy similarity 0–1)",
        lofi_prefs,
        songs,
        k=5,
    )
    print_top_k(
        "Experiment — Chill Lofi user, ENERGY emphasis\n"
        "(genre +1.0, mood +1.0, energy similarity 0–2)",
        lofi_prefs,
        songs,
        k=5,
        genre_points=1.0,
        mood_points=1.0,
        energy_scale=2.0,
    )


if __name__ == "__main__":
    main()
