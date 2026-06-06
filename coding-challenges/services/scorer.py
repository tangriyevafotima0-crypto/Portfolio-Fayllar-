"""Scoring service for calculating points from challenge submissions."""


class Scorer:
    """Calculates points awarded for challenge submissions.

    Points are based on difficulty level and the proportion
    of test cases passed. Bonus points for fast execution.

    Attributes:
        base_points: Mapping of difficulty to base point values.
        time_bonus_threshold: Seconds under which a time bonus applies.
    """

    def __init__(self) -> None:
        """Initialize the Scorer with default point values."""
        self.base_points: dict[str, int] = {
            "easy": 10,
            "medium": 25,
            "hard": 50,
        }
        self.time_bonus_threshold: float = 1.0

    def calculate_points(
        self,
        difficulty: str,
        tests_passed: int,
        tests_total: int,
        execution_time: float = 0.0,
    ) -> int:
        """Calculate points for a submission.

        Full points are awarded only when all tests pass.
        Partial credit is given proportionally.

        Args:
            difficulty: Challenge difficulty (easy, medium, hard).
            tests_passed: Number of test cases passed.
            tests_total: Total number of test cases.
            execution_time: Time taken to execute in seconds.

        Returns:
            Points earned as an integer.
        """
        if tests_total == 0:
            return 0

        base = self.base_points.get(difficulty, 10)
        pass_ratio = tests_passed / tests_total

        if pass_ratio == 1.0:
            points = base
        elif pass_ratio >= 0.5:
            points = int(base * pass_ratio * 0.5)
        else:
            points = 0

        if pass_ratio == 1.0 and execution_time < self.time_bonus_threshold:
            bonus = int(base * 0.1)
            points += bonus

        return points

    def get_difficulty_multiplier(self, difficulty: str) -> float:
        """Get the scoring multiplier for a difficulty level.

        Args:
            difficulty: Challenge difficulty level.

        Returns:
            Multiplier as a float.
        """
        multipliers = {
            "easy": 1.0,
            "medium": 2.5,
            "hard": 5.0,
        }
        return multipliers.get(difficulty, 1.0)

    def calculate_streak_bonus(self, consecutive_solves: int) -> int:
        """Calculate bonus points for solving consecutive challenges.

        Args:
            consecutive_solves: Number of challenges solved in a row.

        Returns:
            Bonus points to award.
        """
        if consecutive_solves < 3:
            return 0
        elif consecutive_solves < 5:
            return 5
        elif consecutive_solves < 10:
            return 15
        else:
            return 30
