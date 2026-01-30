"""
Game logic utilities for the number-guessing game.

Provides difficulty ranges, attempt limits, guess parsing, guess validation,
score updates, and high-score persistence. All functions are pure where possible;
I/O is limited to high-score load/save.
"""
from __future__ import annotations

import json
import os
from typing import Optional

HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.json"
)


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """
    Return the inclusive (low, high) number range for a given difficulty.

    The secret number is chosen from this range. Easy uses a small range,
    Hard uses the full range.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard". Case-sensitive.

    Returns:
        A 2-tuple (low, high) inclusive. Easy=(1, 20), Normal=(1, 50),
        Hard=(1, 100). Unknown difficulties default to (1, 100).
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def get_attempt_limit(difficulty: str) -> int:
    """
    Return the maximum number of guesses allowed for a given difficulty.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard". Case-sensitive.

    Returns:
        Maximum attempts allowed. Easy=6, Normal=8, Hard=5.
        Unknown difficulties default to 5.
    """
    limits = {"Easy": 6, "Normal": 8, "Hard": 5}
    return limits.get(difficulty, 5)


def parse_guess(raw: str) -> tuple[bool, Optional[int], Optional[str]]:
    """
    Parse user input string into an integer guess.

    Accepts integers and float-like strings (e.g. "52.0"); decimals are
    truncated. Rejects empty input, non-numeric strings, and overflow
    (e.g. "1e400").

    Args:
        raw: The user's raw input string. May be empty or contain
             whitespace, digits, decimals, or invalid content.

    Returns:
        A 3-tuple (ok, value, error_message):
        - ok: True if parsing succeeded, False otherwise.
        - value: The parsed integer, or None if parsing failed.
        - error_message: None on success; otherwise a short message
          such as "Enter a guess." or "That is not a number."
    """
    if not raw or raw.strip() == "":
        return False, None, "Enter a guess."
    try:
        value = int(float(raw))
        return True, value, None
    except (ValueError, OverflowError):
        return False, None, "That is not a number."


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """
    Compare the player's guess to the secret number and return outcome and hint.

    Args:
        guess: The player's guess (integer).
        secret: The secret number to guess.

    Returns:
        A 2-tuple (outcome, message):
        - outcome: "Win", "Too High", or "Too Low".
        - message: User-facing hint, e.g. "🎉 Correct!" or "📈 Go HIGHER!".
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(
    current_score: int, outcome: str, attempt_number: int
) -> int:
    """
    Update the player's score based on game outcome and attempt count.

    Only a "Win" outcome adds points; the number of points decreases
    as attempt_number increases, with a minimum of 10 per win.

    Args:
        current_score: The score before this update.
        outcome: "Win", "Too High", or "Too Low". Only "Win" adds points.
        attempt_number: Number of attempts used (1-based). Used to
            compute points for a win: max(10, 100 - 10 * attempt_number).

    Returns:
        The new score. Unchanged if outcome is not "Win".
    """
    if outcome == "Win":
        points = max(10, 100 - 10 * attempt_number)
        return current_score + points
    return current_score


def get_points_for_win(attempt_number: int) -> int:
    """
    Return the points earned for a win with the given attempt count.

    Used for high-score comparison (e.g. same score, fewer attempts
    ranks higher).

    Args:
        attempt_number: Number of attempts used to win (1-based).

    Returns:
        Points for this win: max(10, 100 - 10 * attempt_number).
    """
    return max(10, 100 - 10 * attempt_number)


def load_high_score() -> dict:
    """
    Load the high-score record from the persistent JSON file.

    If the file is missing, unreadable, or invalid JSON, returns a
    default zero record. Does not raise.

    Returns:
        A dict with keys:
        - "score": int (0 if missing/invalid).
        - "difficulty": str or None.
        - "attempts": int or None.
    """
    default = {"score": 0, "difficulty": None, "attempts": None}
    if not os.path.isfile(HIGH_SCORE_FILE):
        return default
    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "score": int(data.get("score", 0)),
            "difficulty": data.get("difficulty"),
            "attempts": data.get("attempts"),
        }
    except (json.JSONDecodeError, OSError):
        return default


def save_high_score(
    score: int,
    difficulty: Optional[str] = None,
    attempts: Optional[int] = None,
) -> None:
    """
    Save the high-score record to the persistent JSON file.

    Overwrites the existing file. Creates the file if it does not exist.
    Directory must already exist.

    Args:
        score: The high score to save.
        difficulty: Optional difficulty label (e.g. "Normal") for display.
        attempts: Optional attempt count for this score, for tie-breaking.

    Returns:
        None.
    """
    with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"score": score, "difficulty": difficulty, "attempts": attempts},
            f,
            indent=2,
        )
