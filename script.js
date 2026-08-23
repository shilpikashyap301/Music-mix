/**
 * MusicMix - Mood-Based Music Recommendation System
 * Client-Side JavaScript (Frontend Controller)
 * 
 * NOTE: As per project rules, all recommendation filtering, sorting, 
 * data parsing, and NumPy statistical calculations are performed on the
 * Python Flask backend. This script ONLY handles UI interactions, 
 * screen transitions, and API communication.
 */

// Helper to format text with proper capitalization
function capitalizeFirstLetter(string) {
    if (!string) return '';
    if (string.toLowerCase() === 'lofi' || string.toLowerCase() === 'lo-fi') return 'Lo-fi';
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Map dropdown genre values to user-friendly display string
function formatGenreName(genreVal) {
    if (!genreVal || genreVal === 'all') return 'All Genres';
    if (genreVal === 'lofi' || genreVal === 'lo-fi') return 'Lo-fi';
    return capitalizeFirstLetter(genreVal);
}

// Utility: XSS prevention
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

document.addEventListener('DOMContentLoaded', () => {
    // Screen Elements
    const homeScreen = document.getElementById('home-screen');
    const recommendationScreen = document.getElementById('recommendation-screen');

    // Form & Control Elements
    const moodSelect = document.getElementById('mood-select');
    const genreSelect = document.getElementById('genre-select');
    const getRecommendationsBtn = document.getElementById('get-recommendations-btn');
    const btnText = document.getElementById('btn-text');
    const backBtn = document.getElementById('back-btn');
    const tryAnotherMoodBtn = document.getElementById('try-another-mood-btn');
    const brandLogo = document.getElementById('brand-logo');

    // Display & Feedback Elements
    const moodChipDisplay = document.getElementById('mood-chip-display');
    const genreChipDisplay = document.getElementById('genre-chip-display');
    const songListContainer = document.getElementById('song-list');
    const emptyStateContainer = document.getElementById('empty-state');
    const errorStateContainer = document.getElementById('error-state');
    const errorText = document.getElementById('error-text');
    const loadingState = document.getElementById('loading-state');
    const quickMoodChips = document.querySelectorAll('.quick-mood-chip');

    // NumPy Statistics Elements
    const statsContainer = document.getElementById('stats-container');
    const statsCount = document.getElementById('stats-count');
    const statsAvg = document.getElementById('stats-avg');
    const statsTop = document.getElementById('stats-top');

    // =========================================================================
    // SCREEN NAVIGATION (Strictly 2 Screens: Home <-> Recommendations)
    // =========================================================================

    function showScreen(screenId) {
        if (screenId === 'recommendation-screen') {
            homeScreen.classList.add('hidden');
            recommendationScreen.classList.remove('hidden');
            if (backBtn) backBtn.classList.remove('hidden');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            recommendationScreen.classList.add('hidden');
            homeScreen.classList.remove('hidden');
            if (backBtn) backBtn.classList.add('hidden');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    // =========================================================================
    // FETCH RECOMMENDATIONS FROM PYTHON FLASK BACKEND
    // =========================================================================

    async function fetchRecommendations() {
        const selectedMood = (moodSelect.value || 'happy').trim();
        const selectedGenre = (genreSelect.value || 'all').trim();

        // 1. Setup UI for request
        if (btnText) btnText.textContent = "Recommending...";
        if (getRecommendationsBtn) getRecommendationsBtn.disabled = true;

        // Reset containers
        songListContainer.innerHTML = '';
        if (emptyStateContainer) emptyStateContainer.classList.add('hidden');
        if (errorStateContainer) errorStateContainer.classList.add('hidden');
        if (statsContainer) statsContainer.classList.add('hidden');
        if (loadingState) loadingState.classList.remove('hidden');

        // Navigate immediately to recommendation screen with loading feedback
        showScreen('recommendation-screen');
        moodChipDisplay.textContent = `Mood: ${capitalizeFirstLetter(selectedMood)}`;
        genreChipDisplay.textContent = `Genre: ${formatGenreName(selectedGenre)}`;

        try {
            // Send selections to Python Flask backend via POST /recommend
            const response = await fetch('/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    mood: selectedMood,
                    genre: selectedGenre
                })
            });

            const result = await response.json();

            if (!response.ok || !result.success) {
                throw new Error(result.error || 'Failed to fetch recommendations from Python backend.');
            }

            // Render matching songs returned by Python
            renderSongCards(result.songs || []);

            // Display NumPy calculations returned by Python
            if (result.stats && result.stats.count > 0) {
                statsCount.textContent = `${result.stats.count} track${result.stats.count === 1 ? '' : 's'}`;
                statsAvg.textContent = Number(result.stats.average_rating).toFixed(1);
                statsTop.textContent = Number(result.stats.highest_rating).toFixed(1);
                statsContainer.classList.remove('hidden');
            }

        } catch (error) {
            console.error('Error connecting to Python backend:', error);
            if (errorStateContainer && errorText) {
                errorText.textContent = error.message || 'Unable to connect to Python backend server.';
                errorStateContainer.classList.remove('hidden');
            }
        } finally {
            if (loadingState) loadingState.classList.add('hidden');
            if (btnText) btnText.textContent = "Get Recommendations";
            if (getRecommendationsBtn) getRecommendationsBtn.disabled = false;
        }
    }

    // =========================================================================
    // DYNAMIC SONG CARD RENDERING
    // =========================================================================

    function renderSongCards(songArray) {
        songListContainer.innerHTML = '';

        if (!songArray || songArray.length === 0) {
            if (emptyStateContainer) emptyStateContainer.classList.remove('hidden');
            return;
        }

        if (emptyStateContainer) emptyStateContainer.classList.add('hidden');

        songArray.forEach(song => {
            const card = document.createElement('div');
            card.className = 'glass-card flex items-center p-md group cursor-pointer';

            const formattedRating = Number(song.rating).toFixed(1);

            card.innerHTML = `
                <div class="w-16 h-16 rounded-lg overflow-hidden flex-shrink-0 mr-md relative">
                    <div class="absolute inset-0 bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center">
                        <span class="material-symbols-outlined text-primary text-3xl">music_note</span>
                    </div>
                </div>
                <div class="flex-grow flex flex-col justify-center overflow-hidden pr-2">
                    <h3 class="font-title-lg text-title-lg text-on-surface truncate group-hover:text-primary transition-colors">${escapeHtml(song.title)}</h3>
                    <p class="font-body-sm text-body-sm text-on-surface-variant truncate">${escapeHtml(song.artist)}</p>
                </div>
                <div class="flex flex-col items-end justify-center ml-sm flex-shrink-0">
                    <span class="glass-chip rounded-full px-sm py-1 font-label-md text-label-md text-primary mb-xs flex items-center h-auto text-[10px]">${escapeHtml(capitalizeFirstLetter(song.genre))}</span>
                    <div class="flex items-center gap-1 font-body-sm text-body-sm text-tertiary">
                        <span class="material-symbols-outlined text-[16px] text-[#FBBF24]">star</span> ${formattedRating}
                    </div>
                </div>
            `;

            songListContainer.appendChild(card);
        });
    }

    // =========================================================================
    // QUICK SELECT MOOD CHIPS
    // =========================================================================

    function updateActiveMoodChip(moodValue) {
        quickMoodChips.forEach(chip => {
            const chipMood = chip.getAttribute('data-mood');
            if (chipMood && chipMood.toLowerCase() === moodValue.toLowerCase()) {
                chip.classList.add('active');
            } else {
                chip.classList.remove('active');
            }
        });
    }

    quickMoodChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const mood = chip.getAttribute('data-mood');
            if (mood) {
                moodSelect.value = mood;
                updateActiveMoodChip(mood);
            }
        });
    });

    if (moodSelect) {
        moodSelect.addEventListener('change', () => {
            updateActiveMoodChip(moodSelect.value);
        });
        updateActiveMoodChip(moodSelect.value);
    }

    // =========================================================================
    // EVENT LISTENERS FOR BUTTONS & NAVIGATION
    // =========================================================================

    if (getRecommendationsBtn) {
        getRecommendationsBtn.addEventListener('click', (e) => {
            e.preventDefault();
            fetchRecommendations();
        });
    }

    if (backBtn) {
        backBtn.addEventListener('click', (e) => {
            e.preventDefault();
            showScreen('home-screen');
        });
    }

    if (tryAnotherMoodBtn) {
        tryAnotherMoodBtn.addEventListener('click', (e) => {
            e.preventDefault();
            showScreen('home-screen');
        });
    }

    if (brandLogo) {
        brandLogo.addEventListener('click', (e) => {
            e.preventDefault();
            showScreen('home-screen');
        });
    }

    // Initial Screen Setup
    showScreen('home-screen');
});
