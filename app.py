import random
import streamlit as st

from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_points_for_win,
    get_range_for_difficulty,
    load_high_score,
    parse_guess,
    save_high_score,
    update_score,
)

# --- UI SETUP ---
st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")

# --- SIDEBAR & DIFFICULTY ---
st.sidebar.header("Settings")

# FIX 4: Reset game when difficulty changes
def handle_difficulty_change():
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.status = "playing"
    if "guess_input" in st.session_state:
        del st.session_state["guess_input"]
    # Note: st.session_state.secret will be updated by the range logic below
    if "last_diff" in st.session_state and st.session_state.last_diff != st.session_state.diff_selector:
         st.session_state.secret = random.randint(*get_range_for_difficulty(st.session_state.diff_selector))
    st.session_state.last_diff = st.session_state.diff_selector

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
    key="diff_selector",
    on_change=handle_difficulty_change
)

attempt_limit = get_attempt_limit(difficulty)
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# --- High score (from file) ---
high_score_data = load_high_score()
st.sidebar.metric("🏆 Best score", high_score_data["score"])
if high_score_data.get("difficulty"):
    st.sidebar.caption(f"Best: {high_score_data['attempts']} attempts on {high_score_data['difficulty']}")

# --- SESSION STATE INITIALIZATION ---
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []

# --- GAME UI ---
st.subheader("Make a guess")

# FIX 2: Blue info card now reflects correct range/attempts 
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

raw_guess = st.text_input("Enter your guess:", value="", key="guess_input")

col1, col2 = st.columns(2)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    # FIX 3: New Game now clears history, status, and guess input
    if st.button("New Game 🔁"):
        st.session_state.attempts = 0
        st.session_state.history = []
        st.session_state.status = "playing"
        st.session_state.secret = random.randint(low, high)
        if "guess_input" in st.session_state:
            del st.session_state["guess_input"]
        st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success(f"You won! The secret was {st.session_state.secret}.")
    else:
        st.error(f"Game over! The secret was {st.session_state.secret}.")
    st.stop()

if submit and raw_guess:
    st.session_state.attempts += 1
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    else:
        # Logic fix: Ensure secret is always int for comparison
        outcome, message = check_guess(guess_int, int(st.session_state.secret))
        st.session_state.history.append({
            "attempt": st.session_state.attempts,
            "guess": guess_int,
            "outcome": outcome,
        })

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.session_state.score = update_score(st.session_state.score, "Win", st.session_state.attempts)
            # Persist high score if this game beats it
            points_this_game = get_points_for_win(st.session_state.attempts)
            if points_this_game > high_score_data["score"]:
                save_high_score(points_this_game, difficulty, st.session_state.attempts)
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
        else:
            st.warning(message)

# --- Guess history sidebar (visual: where each guess fell on the range) ---
if st.session_state.history:
    st.sidebar.divider()
    st.sidebar.subheader("📊 Guess history")
    for i, h in enumerate(st.session_state.history):
        attempt, guess, outcome = h["attempt"], h["guess"], h["outcome"]
        st.sidebar.caption(f"Guess {attempt}: **{guess}** → {outcome}")
        st.sidebar.slider(
            "Position",
            min_value=low,
            max_value=high,
            value=guess,
            key=f"hist_slider_{i}",
            disabled=True,
            label_visibility="collapsed",
        )

# --- HISTORY DISPLAY (main area) ---
if st.session_state.history:
    st.write("### Guess History")
    for h in st.session_state.history:
        st.text(f"Guess {h['attempt']}: {h['guess']} → {h['outcome']}")

with st.expander("Developer Debug Info"):
    st.write(f"Secret: {st.session_state.secret}")
    st.write(f"Score: {st.session_state.score}")