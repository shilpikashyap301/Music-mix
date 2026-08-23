import app

def test_musicmix_backend():
    client = app.app.test_client()

    print("========================================")
    print(" 🧪 RUNNING MUSICMIX COMPREHENSIVE TESTS ")
    print("========================================")

    # 1. Data Structure Verification (Tuple, Set, List, Dict)
    assert isinstance(app.VALID_MOODS, tuple), "VALID_MOODS must be a Tuple"
    assert isinstance(app.VALID_GENRES, set), "VALID_GENRES must be a Set"
    assert len(app.VALID_MOODS) == 6, "Must contain exactly 6 moods"
    print("✓ Concept Check 1 Passed: Tuple (VALID_MOODS) and Set (VALID_GENRES) correctly implemented.")

    # 2. File Handling Verification
    songs_loaded = app.load_songs()
    assert isinstance(songs_loaded, list), "Loaded songs must be a List"
    assert len(songs_loaded) >= 15, "Music catalog must contain at least 15 songs"
    for s in songs_loaded:
        assert isinstance(s, dict), "Each song must be a Dictionary"
        assert all(k in s for k in ("title", "artist", "mood", "genre", "rating")), "Missing dictionary keys"
        assert isinstance(s["rating"], (int, float)), "Rating must be numeric (float/int)"
    print(f"✓ Concept Check 2 Passed: File handling (open 'r') loaded {len(songs_loaded)} song dictionaries.")

    # 3. NumPy Ratings Analysis Verification
    stats = app.analyze_ratings(songs_loaded)
    assert "average_rating" in stats and "highest_rating" in stats and "lowest_rating" in stats
    assert stats["highest_rating"] >= stats["average_rating"] >= stats["lowest_rating"]
    print(f"✓ Concept Check 3 Passed: NumPy statistics computed -> Avg: {stats['average_rating']}, Max: {stats['highest_rating']}, Min: {stats['lowest_rating']}.")

    # 4. HTTP GET / -> Home Screen
    res_home = client.get('/')
    assert res_home.status_code == 200, f"GET / failed with status {res_home.status_code}"
    assert b"MusicMix" in res_home.data, "MusicMix brand missing from HTML"
    print("✓ Test 1 Passed: GET / successfully serves Home Screen HTML with 200 OK.")

    # 5. POST /recommend -> Test 1: Mood=Relaxed, Genre=All Genres
    res_rel_all = client.post('/recommend', json={'mood': 'relaxed', 'genre': 'all'})
    assert res_rel_all.status_code == 200
    data_rel_all = res_rel_all.get_json()
    assert data_rel_all['success'] is True
    assert len(data_rel_all['songs']) > 0
    # Verify sorted by rating descending
    ratings_rel = [s['rating'] for s in data_rel_all['songs']]
    assert ratings_rel == sorted(ratings_rel, reverse=True), "Songs not sorted by rating descending"
    for s in data_rel_all['songs']:
        assert s['mood'] == 'relaxed'
    print(f"✓ Test 2 Passed: POST /recommend (Relaxed, All) -> {len(data_rel_all['songs'])} songs sorted by rating.")

    # 6. POST /recommend -> Test 2: Mood=Happy, Genre=Pop
    res_hap_pop = client.post('/recommend', json={'mood': 'happy', 'genre': 'pop'})
    assert res_hap_pop.status_code == 200
    data_hap_pop = res_hap_pop.get_json()
    assert data_hap_pop['success'] is True
    for s in data_hap_pop['songs']:
        assert s['mood'] == 'happy' and s['genre'] == 'pop'
    print(f"✓ Test 3 Passed: POST /recommend (Happy, Pop) -> {len(data_hap_pop['songs'])} tracks strictly matching Happy & Pop.")

    # 7. POST /recommend -> Test 3: Mood=Energetic, Genre=Rock
    res_ene_rock = client.post('/recommend', json={'mood': 'energetic', 'genre': 'rock'})
    assert res_ene_rock.status_code == 200
    data_ene_rock = res_ene_rock.get_json()
    assert data_ene_rock['success'] is True
    for s in data_ene_rock['songs']:
        assert s['mood'] == 'energetic' and s['genre'] == 'rock'
    print(f"✓ Test 4 Passed: POST /recommend (Energetic, Rock) -> {len(data_ene_rock['songs'])} tracks strictly matching Energetic & Rock.")

    # 8. POST /recommend -> Test 4: No matching songs combination
    res_no_match = client.post('/recommend', json={'mood': 'happy', 'genre': 'romantic'})
    assert res_no_match.status_code == 200
    data_no_match = res_no_match.get_json()
    assert data_no_match['success'] is True
    assert len(data_no_match['songs']) == 0
    print("✓ Test 5 Passed: POST /recommend with no matching songs returns empty song list (triggers empty state UI).")

    # 9. POST /recommend -> Error Handling (Invalid Mood)
    res_inv = client.post('/recommend', json={'mood': 'excited', 'genre': 'all'})
    assert res_inv.status_code == 400
    data_inv = res_inv.get_json()
    assert data_inv['success'] is False
    assert "not a recognized mood" in data_inv['error']
    print("✓ Test 6 Passed: Invalid mood returns 400 Bad Request with user-friendly error message.")

    print("\n========================================")
    print(" 🎉 ALL PYTHON BACKEND TESTS PASSED! 🎧 ")
    print("========================================")

if __name__ == '__main__':
    test_musicmix_backend()

