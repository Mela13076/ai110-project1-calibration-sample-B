"""
Tests for game logic (logic_utils).

Covers the bugs described in reflection.md:
1. check_guess hint direction (Too Low → "Higher", Too High → "Lower")
2. Difficulty ranges and attempt limits (Easy: 1–20, 6 attempts; etc.)
3. (New Game / difficulty reset are UI/session state; logic is get_range + get_attempt_limit)
4. Difficulty change uses correct range (get_range_for_difficulty)
"""
import pytest

from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


# --- check_guess (reflection #1: hint direction) ---


def test_check_guess_win():
    """Guess equals secret → Win."""
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message or "🎉" in message


def test_check_guess_too_low_returns_higher_hint():
    """Reflection #1: Guess below secret → 'Too Low' and hint to go HIGHER.
    (Secret 52, guess 50 → should say Higher, not Lower.)
    """
    outcome, message = check_guess(50, 52)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper() or "higher" in message


def test_check_guess_too_high_returns_lower_hint():
    """Reflection #1: Guess above secret → 'Too High' and hint to go LOWER.
    (Secret 52, guess 54 → should say Lower, not Higher.)
    """
    outcome, message = check_guess(54, 52)
    assert outcome == "Too High"
    assert "LOWER" in message.upper() or "lower" in message


def test_check_guess_too_low_generic():
    """Secret 50, guess 40 → Too Low, Higher."""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


def test_check_guess_too_high_generic():
    """Secret 50, guess 60 → Too High, Lower."""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()


# --- get_range_for_difficulty (reflection #2, #4: difficulty → range) ---


def test_easy_range_1_to_20():
    """Reflection #2: Easy mode should use range 1–20."""
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20


def test_normal_range_1_to_50():
    """Normal mode → 1–50."""
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 50


def test_hard_range_1_to_100():
    """Reflection #4: Hard should be largest range (1–100)."""
    low, high = get_range_for_difficulty("Hard")
    assert low == 1 and high == 100


def test_unknown_difficulty_defaults_to_1_100():
    """Unknown difficulty → default 1–100."""
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1 and high == 100


# --- get_attempt_limit (reflection #2: Easy = 6 attempts) ---


def test_easy_6_attempts():
    """Reflection #2: Easy mode should allow 6 attempts."""
    assert get_attempt_limit("Easy") == 6


def test_normal_8_attempts():
    """Normal → 8 attempts."""
    assert get_attempt_limit("Normal") == 8


def test_hard_5_attempts():
    """Hard → 5 attempts."""
    assert get_attempt_limit("Hard") == 5


def test_unknown_difficulty_attempt_limit():
    """Unknown difficulty → sensible default."""
    assert get_attempt_limit("Unknown") == 5


# --- parse_guess ---


def test_parse_guess_empty():
    """Empty input → error, no value."""
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert "Enter a guess" in err


def test_parse_guess_whitespace():
    """Whitespace-only → error."""
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert "Enter a guess" in err


def test_parse_guess_non_number():
    """Non-numeric input → error."""
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert "not a number" in err


def test_parse_guess_valid_int():
    """Valid integer string → ok, int value, no error."""
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_float_coerced_to_int():
    """Float-like input (e.g. 52.0) is coerced to int."""
    ok, value, err = parse_guess("52.0")
    assert ok is True
    assert value == 52
    assert err is None


# --- update_score ---


def test_update_score_on_win():
    """Win adds points; first attempt gives more."""
    score = update_score(0, "Win", 1)
    assert score == 90  # max(10, 100 - 10*1) = 90


def test_update_score_on_win_later_attempt():
    """Later attempt win gives fewer points."""
    score = update_score(0, "Win", 5)
    assert score == 50  # max(10, 100 - 50) = 50


def test_update_score_min_points_on_win():
    """Win always gives at least 10 points."""
    score = update_score(100, "Win", 15)  # 100 - 150 would be negative
    assert score == 110  # 100 + max(10, 100 - 150) = 100 + 10


def test_update_score_no_change_on_loss():
    """Non-win outcome does not change score."""
    score = update_score(50, "Too High", 3)
    assert score == 50


def test_update_score_no_change_on_too_low():
    """Too Low does not change score."""
    score = update_score(50, "Too Low", 2)
    assert score == 50
