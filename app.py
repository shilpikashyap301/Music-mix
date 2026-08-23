"""
MusicMix - Mood-Based Music Recommendation System
College Python Mini Project
=================================================
Demonstrates Core Python Concepts:
1. Python Fundamentals (Variables, Data Types: str, int, float, bool)
2. Lists (Music collection storage)
3. Tuples (Immutable predefined moods)
4. Sets (Unique music genres)
5. Dictionaries (Structured song records)
6. Conditional Statements (if, elif, else)
7. Loops (for loops for filtering, parsing, and sorting)
8. Modular Functions (load_data, save_data, recommend_songs, calculate_statistics)
9. File Handling (open() with 'r' and 'w' modes on music_data.txt)
10. NumPy (Statistical analysis of song ratings: mean, max, min)
11. Flask Web Framework (Routing and REST API endpoints)
"""

import os
from flask import Flask, render_template, request, jsonify
import numpy as np

# Initialize Flask Application
app = Flask(__name__)

# Path to the plain-text music data file
DATA_FILE = os.path.join(os.path.dirname(__file__), "music_data.txt")

# =============================================================================
# PYTHON DATA STRUCTURES: TUPLE & SET
# =============================================================================

# Tuple: Immutable collection of allowed moods (Python Concept: Tuple)
moods = (
    "happy",
    "sad",
    "relaxed",
    "energetic",
    "romantic",
    "focused"
)
VALID_MOODS = moods

# Set: Unique collection of genres (Python Concept: Set)
genres = {
    "all",
    "pop",
    "rock",
    "lo-fi",
    "instrumental",
    "romantic",
    "electronic"
}
VALID_GENRES = genres

# Default Songs List (Python Concept: List of Dictionaries)
songs = [
    {"title": "Weightless", "artist": "Marconi Union", "mood": "relaxed", "genre": "instrumental", "rating": 4.9},
    {"title": "Sunset Lover", "artist": "Petit Biscuit", "mood": "relaxed", "genre": "lo-fi", "rating": 4.8},
    {"title": "Ocean Drive", "artist": "Duke Dumont", "mood": "relaxed", "genre": "electronic", "rating": 4.7},
    {"title": "River Flows in You", "artist": "Yiruma", "mood": "relaxed", "genre": "instrumental", "rating": 4.9},
    {"title": "Banana Pancakes", "artist": "Jack Johnson", "mood": "relaxed", "genre": "pop", "rating": 4.7},
    {"title": "Wish You Were Here", "artist": "Pink Floyd", "mood": "relaxed", "genre": "rock", "rating": 4.9},
    {"title": "Happy", "artist": "Pharrell Williams", "mood": "happy", "genre": "pop", "rating": 4.9},
    {"title": "Don't Stop Me Now", "artist": "Queen", "mood": "happy", "genre": "rock", "rating": 4.9},
    {"title": "Can't Stop the Feeling!", "artist": "Justin Timberlake", "mood": "happy", "genre": "pop", "rating": 4.8},
    {"title": "Levels", "artist": "Avicii", "mood": "happy", "genre": "electronic", "rating": 4.9},
    {"title": "Sunday Morning", "artist": "Lofi Fruits Music", "mood": "happy", "genre": "lo-fi", "rating": 4.7},
    {"title": "Spring Waltz", "artist": "Frédéric Chopin", "mood": "happy", "genre": "instrumental", "rating": 4.8},
    {"title": "Someone Like You", "artist": "Adele", "mood": "sad", "genre": "pop", "rating": 4.9},
    {"title": "Fix You", "artist": "Coldplay", "mood": "sad", "genre": "rock", "rating": 4.9},
    {"title": "Comptine d'un autre été", "artist": "Yann Tiersen", "mood": "sad", "genre": "instrumental", "rating": 4.9},
    {"title": "death bed (coffee for your head)", "artist": "Powfu ft. beabadoobee", "mood": "sad", "genre": "lo-fi", "rating": 4.8},
    {"title": "Shelter (Piano Reprise)", "artist": "Porter Robinson & Madeon", "mood": "sad", "genre": "electronic", "rating": 4.7},
    {"title": "All I Want", "artist": "Kodaline", "mood": "sad", "genre": "romantic", "rating": 4.8},
    {"title": "Titanium", "artist": "David Guetta ft. Sia", "mood": "energetic", "genre": "electronic", "rating": 4.9},
    {"title": "Eye of the Tiger", "artist": "Survivor", "mood": "energetic", "genre": "rock", "rating": 4.9},
    {"title": "Blinding Lights", "artist": "The Weeknd", "mood": "energetic", "genre": "pop", "rating": 4.9},
    {"title": "Believer", "artist": "Imagine Dragons", "mood": "energetic", "genre": "rock", "rating": 4.8},
    {"title": "Flight of the Bumblebee", "artist": "David Garrett", "mood": "energetic", "genre": "instrumental", "rating": 4.7},
    {"title": "Tokyo Beats (Fast Flip)", "artist": "Chillhop Beats", "mood": "energetic", "genre": "lo-fi", "rating": 4.6},
    {"title": "Perfect", "artist": "Ed Sheeran", "mood": "romantic", "genre": "romantic", "rating": 4.9},
    {"title": "Until I Found You", "artist": "Stephen Sanchez", "mood": "romantic", "genre": "romantic", "rating": 4.9},
    {"title": "Just the Way You Are", "artist": "Bruno Mars", "mood": "romantic", "genre": "pop", "rating": 4.8},
    {"title": "I Don't Want to Miss a Thing", "artist": "Aerosmith", "mood": "romantic", "genre": "rock", "rating": 4.9},
    {"title": "Affection", "artist": "Jinsang", "mood": "romantic", "genre": "lo-fi", "rating": 4.7},
    {"title": "Can't Help Falling in Love", "artist": "Daniel Jang", "mood": "romantic", "genre": "instrumental", "rating": 4.9},
    {"title": "1 AM Study Session", "artist": "Lofi Girl", "mood": "focused", "genre": "lo-fi", "rating": 4.9},
    {"title": "Experience", "artist": "Ludovico Einaudi", "mood": "focused", "genre": "instrumental", "rating": 4.9},
    {"title": "Clair de Lune", "artist": "Claude Debussy", "mood": "focused", "genre": "instrumental", "rating": 4.9},
    {"title": "Strobe", "artist": "deadmau5", "mood": "focused", "genre": "electronic", "rating": 4.8},
    {"title": "Marooned", "artist": "Pink Floyd", "mood": "focused", "genre": "rock", "rating": 4.8},
    {"title": "Attention (Lofi Piano Study)", "artist": "Kuma Sounds", "mood": "focused", "genre": "pop", "rating": 4.7}
]
DEFAULT_SONGS = songs


# =============================================================================
# FILE HANDLING FUNCTIONS (Python Concept: open() 'r' and 'w')
# =============================================================================

def save_data(song_list, filepath=DATA_FILE):
    """
    Saves the list of song dictionaries to a text file.
    Demonstrates file handling with open(..., 'w').
    """
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            for song in song_list:
                line = f"{song['title']}|{song['artist']}|{song['mood']}|{song['genre']}|{song['rating']}\n"
                file.write(line)
        return True
    except IOError as e:
        print(f"[Error] Failed to save music data: {e}")
        return False


def load_songs(filepath=DATA_FILE):
    """
    Reads and parses the song records from a text file.
    Demonstrates file handling with open(..., 'r'), strip(), split(), and type conversion.
    """
    songs_loaded = []
    
    # If the file does not exist, create it with default data
    if not os.path.exists(filepath):
        print(f"[Info] File {filepath} not found. Creating with default song catalog.")
        save_data(DEFAULT_SONGS, filepath)
        return DEFAULT_SONGS.copy()
    
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                cleaned_line = line.strip()
                if cleaned_line and not cleaned_line.startswith("#"):
                    parts = cleaned_line.split("|")
                    if len(parts) >= 5:
                        song_dict = {
                            "title": parts[0].strip(),
                            "artist": parts[1].strip(),
                            "mood": parts[2].strip().lower(),
                            "genre": parts[3].strip().lower(),
                            "rating": float(parts[4].strip())  # Float conversion
                        }
                        songs_loaded.append(song_dict)
        return songs_loaded if songs_loaded else DEFAULT_SONGS.copy()
    except Exception as e:
        print(f"[Error] Failed to load data from file: {e}")
        return DEFAULT_SONGS.copy()

# Alias for backwards compatibility
load_data = load_songs



# =============================================================================
# DATA VALIDATION & HELPER FUNCTIONS
# =============================================================================

def validate_selection(mood, genre):
    """
    Validates user input using Tuples, Sets, and Conditional Statements.
    Returns: (is_valid: bool, cleaned_mood: str, cleaned_genre: str, error_message: str)
    """
    if not mood or not isinstance(mood, str):
        return False, "", "", "Please provide a valid mood."

    cleaned_mood = mood.strip().lower()
    cleaned_genre = (genre or "all").strip().lower().replace(" ", "")

    # Normalize lo-fi formatting
    if cleaned_genre in ("lofi", "lo-fi"):
        cleaned_genre = "lo-fi"

    # Validate mood against the VALID_MOODS tuple
    if cleaned_mood not in VALID_MOODS:
        return False, cleaned_mood, cleaned_genre, f"'{mood}' is not a recognized mood. Valid moods: {', '.join(VALID_MOODS)}."

    # Validate genre against the VALID_GENRES set
    if cleaned_genre not in VALID_GENRES and cleaned_genre != "allgenres":
        return False, cleaned_mood, cleaned_genre, f"'{genre}' is not a recognized genre."

    if cleaned_genre == "allgenres":
        cleaned_genre = "all"

    return True, cleaned_mood, cleaned_genre, ""


def get_genres(song_list):
    """
    Extracts all unique genres from a list of songs using Python Set comprehension.
    """
    unique_genres = {song["genre"] for song in song_list}
    return sorted(list(unique_genres))


# =============================================================================
# RECOMMENDATION & NUMPY ANALYSIS LOGIC
# =============================================================================

def recommend_songs(mood, genre, all_songs=None):
    """
    Filters and sorts songs matching the user's selected mood and genre.
    Demonstrates Conditional Statements, Loops, and Sorting.
    """
    if all_songs is None:
        all_songs = load_songs()

    matching_songs = []
    
    # Iterate through all songs using a for loop
    for song in all_songs:
        # Check if song matches the requested mood
        if song["mood"].lower() == mood.lower():
            # If genre is 'all', accept any genre; otherwise match exact genre
            if genre == "all" or song["genre"].lower().replace("-", "") == genre.lower().replace("-", ""):
                matching_songs.append(song)
    
    # Sort recommendations by rating in descending order (highest rating first)
    sorted_songs = sorted(matching_songs, key=lambda s: s["rating"], reverse=True)
    return sorted_songs


def analyze_ratings(song_list=None):
    """
    Uses NumPy to perform statistical calculations on song ratings.
    Demonstrates: np.array, np.mean, np.max, np.min, np.round.
    """
    if song_list is None:
        song_list = load_songs()

    if not song_list:
        return {
            "count": 0,
            "average_rating": 0.0,
            "highest_rating": 0.0,
            "lowest_rating": 0.0
        }

    # Extract ratings into a NumPy array
    ratings = np.array([song["rating"] for song in song_list], dtype=float)

    # Compute statistics using NumPy methods
    avg_rating = float(np.round(np.mean(ratings), 2))
    max_rating = float(np.max(ratings))
    min_rating = float(np.min(ratings))

    return {
        "count": int(len(ratings)),
        "average_rating": avg_rating,
        "highest_rating": max_rating,
        "lowest_rating": min_rating
    }

# Alias for backwards compatibility
calculate_statistics = analyze_ratings



# =============================================================================
# FLASK WEB ROUTES
# =============================================================================

@app.route("/")
def home():
    """
    Renders the main Home Screen (Screen 1 & 2 UI).
    """
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def get_recommendations_api():
    """
    POST API Endpoint for Recommendations:
    1. Reads user selections from JSON payload.
    2. Validates mood and genre.
    3. Loads song records from text file.
    4. Executes recommendation algorithm in Python.
    5. Calculates NumPy statistics.
    6. Returns structured JSON to the frontend.
    """
    try:
        # Parse incoming JSON payload
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"success": False, "error": "Invalid request. JSON payload required."}), 400

        user_mood = data.get("mood", "")
        user_genre = data.get("genre", "all")

        # Validate input (Python Concept: Functions, Tuples, Sets, Conditions)
        is_valid, cleaned_mood, cleaned_genre, error_msg = validate_selection(user_mood, user_genre)
        if not is_valid:
            return jsonify({"success": False, "error": error_msg}), 400

        # Load data from file (Python Concept: File Handling)
        all_songs = load_songs(DATA_FILE)

        # Generate recommendations (Python Concept: Loops, Conditions, Sorting)
        recommended_songs = recommend_songs(cleaned_mood, cleaned_genre, all_songs)

        # Calculate statistics using NumPy (Python Concept: NumPy analysis)
        stats = analyze_ratings(recommended_songs)

        # Return successful response
        return jsonify({
            "success": True,
            "mood": cleaned_mood,
            "genre": cleaned_genre,
            "total_matches": len(recommended_songs),
            "stats": stats,
            "songs": recommended_songs
        }), 200

    except Exception as err:
        print(f"[Error] Exception in /recommend endpoint: {err}")
        return jsonify({
            "success": False,
            "error": "An unexpected server error occurred. Please try again."
        }), 500


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Ensure dataset file is ready upon startup
    print("=" * 60)
    print("🎧 MusicMix - Mood-Based Music Recommendation System")
    print("=" * 60)
    
    songs_catalog = load_songs(DATA_FILE)
    print(f"✓ Loaded {len(songs_catalog)} songs from {DATA_FILE}")
    print(f"✓ Supported Moods ({len(VALID_MOODS)}): {', '.join(VALID_MOODS)}")
    print(f"✓ Supported Genres ({len(VALID_GENRES)}): {', '.join(sorted(VALID_GENRES))}")
    print("✓ Flask Server Starting on http://127.0.0.1:5000")
    print("=" * 60)
    
    app.run(host="127.0.0.1", port=5000, debug=True)
