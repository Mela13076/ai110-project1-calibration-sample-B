def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50  # Fixed: Scaled logically
    if difficulty == "Hard":
        return 1, 100  # Fixed: Hard should be the largest range
    return 1, 100


def get_attempt_limit(difficulty: str):
    """Return max attempts allowed for a given difficulty."""
    limits = {"Easy": 6, "Normal": 8, "Hard": 5}
    return limits.get(difficulty, 5)


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if not raw or raw.strip() == "":
        return False, None, "Enter a guess."
    try:
        # Handling floats/decimals gracefully
        value = int(float(raw))
        return True, value, None
    except ValueError:
        return False, None, "That is not a number."


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    FIX 1: Inverted Hint Logic - Corrected the conditional operators so higher guesses return 'Too High'.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"  # Fixed: Was saying Higher
    else:
        return "Too Low", "📈 Go HIGHER!"  # Fixed: Was saying Lower


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = max(10, 100 - 10 * attempt_number)
        return current_score + points
    return current_score  # Simplified for stability
