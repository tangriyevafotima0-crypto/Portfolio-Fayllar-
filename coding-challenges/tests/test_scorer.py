"""Tests for the Scorer service."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.scorer import Scorer


class TestScorer:
    """Test suite for the Scorer class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.scorer = Scorer()

    def test_full_points_easy(self) -> None:
        """Test full points awarded for passing all easy tests (with speed bonus)."""
        points = self.scorer.calculate_points("easy", 5, 5, execution_time=2.0)
        assert points == 10

    def test_full_points_medium(self) -> None:
        """Test full points awarded for passing all medium tests (with speed bonus)."""
        points = self.scorer.calculate_points("medium", 5, 5, execution_time=2.0)
        assert points == 25

    def test_full_points_hard(self) -> None:
        """Test full points awarded for passing all hard tests (with speed bonus)."""
        points = self.scorer.calculate_points("hard", 5, 5, execution_time=2.0)
        assert points == 50

    def test_partial_credit_above_half(self) -> None:
        """Test partial credit when more than half tests pass."""
        points = self.scorer.calculate_points("easy", 4, 5)
        expected = int(10 * (4 / 5) * 0.5)
        assert points == expected

    def test_no_points_below_half(self) -> None:
        """Test no points when fewer than half tests pass."""
        points = self.scorer.calculate_points("easy", 2, 5)
        assert points == 0

    def test_zero_tests(self) -> None:
        """Test handling of zero total tests."""
        points = self.scorer.calculate_points("easy", 0, 0)
        assert points == 0

    def test_time_bonus(self) -> None:
        """Test time bonus for fast execution."""
        points_fast = self.scorer.calculate_points("easy", 5, 5, execution_time=0.5)
        points_slow = self.scorer.calculate_points("easy", 5, 5, execution_time=2.0)
        assert points_fast > points_slow

    def test_streak_bonus_no_streak(self) -> None:
        """Test no bonus for short streaks."""
        bonus = self.scorer.calculate_streak_bonus(2)
        assert bonus == 0

    def test_streak_bonus_small(self) -> None:
        """Test small bonus for 3-4 streak."""
        bonus = self.scorer.calculate_streak_bonus(3)
        assert bonus == 5

    def test_streak_bonus_medium(self) -> None:
        """Test medium bonus for 5-9 streak."""
        bonus = self.scorer.calculate_streak_bonus(7)
        assert bonus == 15

    def test_streak_bonus_large(self) -> None:
        """Test large bonus for 10+ streak."""
        bonus = self.scorer.calculate_streak_bonus(12)
        assert bonus == 30

    def test_difficulty_multiplier(self) -> None:
        """Test difficulty multiplier values."""
        assert self.scorer.get_difficulty_multiplier("easy") == 1.0
        assert self.scorer.get_difficulty_multiplier("medium") == 2.5
        assert self.scorer.get_difficulty_multiplier("hard") == 5.0
        assert self.scorer.get_difficulty_multiplier("unknown") == 1.0
