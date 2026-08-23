import app
import json

def run_all_e2e_tests():
    print("=" * 60)
    print("🚀 RUNNING END-TO-END VERIFICATION OF ALL 6 USER TEST SCENARIOS")
    print("=" * 60)
    
    client = app.app.test_client()

    # Flow 1: Home Screen renders properly
    res_home = client.get('/')
    assert res_home.status_code == 200
    html = res_home.data.decode('utf-8')
    assert "MusicMix" in html
    assert "Find the music that matches your mood." in html
    assert "id=\"mood-select\"" in html
    assert "id=\"genre-select\"" in html
    assert "id=\"get-recommendations-btn\"" in html
    assert "id=\"recommendation-screen\"" in html
    assert "id=\"back-btn\"" in html
    assert "id=\"try-another-mood-btn\"" in html
    assert "id=\"empty-state\"" in html
    assert "No matching songs found." in html
    assert "Try another mood or genre." in html
    print("✅ Flow 1 Verified: Home & Recommendation screens, selectors, buttons, and state containers present in template.")

    # Flow 2: Test 1 (Relaxed, All Genres) -> Displays matching relaxed songs sorted by rating descending
    res_t1 = client.post('/recommend', data=json.dumps({'mood': 'relaxed', 'genre': 'all'}), content_type='application/json')
    assert res_t1.status_code == 200
    data_t1 = res_t1.get_json()
    assert data_t1['success'] is True
    assert len(data_t1['songs']) >= 5
    # Check all are relaxed
    for s in data_t1['songs']:
        assert s['mood'] == 'relaxed', f"Expected relaxed, got {s['mood']}"
    # Check sorting descending
    ratings = [s['rating'] for s in data_t1['songs']]
    assert ratings == sorted(ratings, reverse=True), "Not sorted by rating descending"
    # Check NumPy stats
    assert data_t1['stats']['count'] == len(data_t1['songs'])
    assert data_t1['stats']['average_rating'] > 0
    assert data_t1['stats']['highest_rating'] == ratings[0]
    print(f"✅ Flow 2 (Test 1) Verified: Relaxed + All Genres returned {len(data_t1['songs'])} songs sorted by rating (Top: {data_t1['stats']['highest_rating']}, Avg: {data_t1['stats']['average_rating']}).")

    # Flow 3: Test 2 (Happy, Pop) -> Only Happy + Pop songs
    res_t2 = client.post('/recommend', data=json.dumps({'mood': 'happy', 'genre': 'pop'}), content_type='application/json')
    assert res_t2.status_code == 200
    data_t2 = res_t2.get_json()
    assert data_t2['success'] is True
    assert len(data_t2['songs']) > 0
    for s in data_t2['songs']:
        assert s['mood'] == 'happy' and s['genre'] == 'pop'
    print(f"✅ Flow 3 (Test 2) Verified: Happy + Pop returned {len(data_t2['songs'])} tracks strictly matching Happy & Pop.")

    # Flow 4: Test 3 (Energetic, Rock) -> Only Energetic + Rock songs
    res_t3 = client.post('/recommend', data=json.dumps({'mood': 'energetic', 'genre': 'rock'}), content_type='application/json')
    assert res_t3.status_code == 200
    data_t3 = res_t3.get_json()
    assert data_t3['success'] is True
    assert len(data_t3['songs']) > 0
    for s in data_t3['songs']:
        assert s['mood'] == 'energetic' and s['genre'] == 'rock'
    print(f"✅ Flow 4 (Test 3) Verified: Energetic + Rock returned {len(data_t3['songs'])} tracks strictly matching Energetic & Rock.")

    # Flow 5: Test 4 (Empty result combination, e.g. Happy + Romantic)
    res_t4 = client.post('/recommend', data=json.dumps({'mood': 'happy', 'genre': 'romantic'}), content_type='application/json')
    assert res_t4.status_code == 200
    data_t4 = res_t4.get_json()
    assert data_t4['success'] is True
    assert len(data_t4['songs']) == 0
    assert data_t4['stats']['count'] == 0
    print("✅ Flow 5 (Test 4) Verified: Unmatched combination returns 0 songs with count 0.")

    # Flow 6: Error Handling (Invalid Mood / Genre)
    res_t5 = client.post('/recommend', data=json.dumps({'mood': 'mysterious', 'genre': 'jazz'}), content_type='application/json')
    assert res_t5.status_code == 400
    data_t5 = res_t5.get_json()
    assert data_t5['success'] is False
    assert "not a recognized mood" in data_t5['error']
    print("✅ Flow 6 (Error Handling) Verified: Invalid mood returned 400 with friendly message.")

    # Flow 7: Verify Python Evaluation Concepts
    print("\n----------------------------------------")
    print("📚 PYTHON EVALUATION CHECKLIST VALIDATION:")
    print("----------------------------------------")
    print(f"✓ Tuple (VALID_MOODS): {app.VALID_MOODS} (type: {type(app.VALID_MOODS).__name__})")
    print(f"✓ Set (VALID_GENRES): {app.VALID_GENRES} (type: {type(app.VALID_GENRES).__name__})")
    all_songs = app.load_songs()
    print(f"✓ List of Dictionaries (songs): {len(all_songs)} songs loaded from music_data.txt")
    print(f"✓ Dictionary sample: {all_songs[0]}")
    
    # Test direct calls without extra arguments
    direct_recs = app.recommend_songs("happy", "pop")
    assert len(direct_recs) > 0, "Direct recommend_songs('happy', 'pop') failed"
    print(f"✓ Direct function call: recommend_songs('happy', 'pop') returned {len(direct_recs)} songs")
    
    stats_all = app.analyze_ratings()
    assert stats_all["average_rating"] > 0
    print(f"✓ Direct function call: analyze_ratings() computed Avg={stats_all['average_rating']}, Max={stats_all['highest_rating']}, Min={stats_all['lowest_rating']}")
    print("----------------------------------------")
    print("🎉 ALL TESTS & EVALUATION CHECKS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == '__main__':
    run_all_e2e_tests()
