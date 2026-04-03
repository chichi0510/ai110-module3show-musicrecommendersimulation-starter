import csv
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass

# Algorithm recipe (additive points): genre > mood > energy fine-tune.
POINTS_GENRE_MATCH = 2.0
POINTS_MOOD_MATCH = 1.0


def _genre_mood_match(user_value: str, song_value: str) -> float:
    """1.0 if labels match, else 0.0."""
    return 1.0 if user_value and song_value and user_value == song_value else 0.0


def _energy_similarity(target: float, song_energy: float) -> float:
    """0.0–1.0: closer target energy is better (both in [0, 1])."""
    return max(0.0, 1.0 - abs(float(song_energy) - float(target)))


def _total_score(
    genre_m: float,
    mood_m: float,
    energy_sim: float,
    *,
    genre_points: float = POINTS_GENRE_MATCH,
    mood_points: float = POINTS_MOOD_MATCH,
    energy_scale: float = 1.0,
    use_mood: bool = True,
) -> float:
    m = mood_m if use_mood else 0.0
    return genre_points * genre_m + mood_points * m + energy_scale * energy_sim


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored: List[Tuple[float, Song]] = []
        for song in self.songs:
            g = _genre_mood_match(user.favorite_genre, song.genre)
            m = _genre_mood_match(user.favorite_mood, song.mood)
            e = _energy_similarity(user.target_energy, song.energy)
            scored.append((_total_score(g, m, e, use_mood=True), song))
        scored = sorted(scored, key=lambda t: t[0], reverse=True)
        return [s for _, s in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        parts: List[str] = []
        if song.genre == user.favorite_genre:
            parts.append(f"genre matches your favorite ({song.genre})")
        else:
            parts.append(f"genre is {song.genre}, not your favorite ({user.favorite_genre})")
        if song.mood == user.favorite_mood:
            parts.append(f"mood matches ({song.mood})")
        else:
            parts.append(f"mood is {song.mood} vs preferred {user.favorite_mood}")
        parts.append(
            f"energy {song.energy:.2f} vs target {user.target_energy:.2f}"
        )
        return "; ".join(parts) + "."

def load_songs(csv_path: str) -> List[Dict[str, Any]]:
    """Read songs CSV into a list of dicts with numeric fields coerced for scoring."""
    print(f"Loading songs from {csv_path}...")
    rows: List[Dict[str, Any]] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = int(round(float(row["tempo_bpm"])))
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            rows.append(row)
    print(f"Loaded songs: {len(rows)}")
    return rows

def score_song(
    user_prefs: Dict,
    song: Dict,
    *,
    genre_points: float = POINTS_GENRE_MATCH,
    mood_points: float = POINTS_MOOD_MATCH,
    energy_scale: float = 1.0,
    use_mood: bool = True,
) -> Tuple[float, List[str]]:
    """Return total match score and human-readable reason strings for one song."""
    genre_key = user_prefs.get("genre") or user_prefs.get("favorite_genre", "")
    mood_key = user_prefs.get("mood") or user_prefs.get("favorite_mood", "")
    target_energy = float(user_prefs.get("energy", user_prefs.get("target_energy", 0.5)))

    g = _genre_mood_match(str(genre_key), str(song.get("genre", "")))
    m_raw = _genre_mood_match(str(mood_key), str(song.get("mood", "")))
    m = m_raw if use_mood else 0.0
    e = _energy_similarity(target_energy, float(song.get("energy", 0.0)))
    score = _total_score(
        g,
        m_raw,
        e,
        genre_points=genre_points,
        mood_points=mood_points,
        energy_scale=energy_scale,
        use_mood=use_mood,
    )

    reasons: List[str] = []
    if g >= 1.0:
        reasons.append(f"genre match (+{genre_points:.1f})")
    if use_mood and m_raw >= 1.0:
        reasons.append(f"mood match (+{mood_points:.1f})")
    reasons.append(f"energy close to target (+{energy_scale * e:.2f})")
    return score, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    **score_kwargs: Any,
) -> List[Tuple[Dict, float, List[str]]]:
    """Score every song via score_song (optional genre_points, mood_points, energy_scale, use_mood), sort, top k."""
    ranked: List[Tuple[Dict, float, List[str]]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, **score_kwargs)
        ranked.append((song, score, reasons))
    ranked = sorted(ranked, key=lambda t: t[1], reverse=True)
    return ranked[:k]
