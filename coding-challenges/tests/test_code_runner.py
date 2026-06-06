"""Tests for the CodeRunner service."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.code_runner import CodeRunner


class TestCodeRunner:
    """Test suite for the CodeRunner class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.runner = CodeRunner(timeout=5)

    def test_execute_simple_function(self) -> None:
        """Test executing a simple function that returns a value."""
        code = "def solution(x):\n    return x * 2"
        result = self.runner.execute_code(code, 5)

        assert result["output"] == 10
        assert result["error"] is None

    def test_execute_with_list_input(self) -> None:
        """Test executing with multiple arguments via list."""
        code = "def solution(a, b):\n    return a + b"
        result = self.runner.execute_code(code, [3, 7])

        assert result["output"] == 10
        assert result["error"] is None

    def test_missing_solution_function(self) -> None:
        """Test error when no solution function is defined."""
        code = "def my_func(x):\n    return x"
        result = self.runner.execute_code(code, 5)

        assert result["output"] is None
        assert "No 'solution' function found" in result["error"]

    def test_syntax_error_in_code(self) -> None:
        """Test handling of syntax errors."""
        code = "def solution(x)\n    return x"
        result = self.runner.execute_code(code, 5)

        assert result["error"] is not None
        assert "SyntaxError" in result["error"]

    def test_runtime_error(self) -> None:
        """Test handling of runtime exceptions."""
        code = "def solution(x):\n    return 1 / 0"
        result = self.runner.execute_code(code, 5)

        assert result["error"] is not None
        assert "ZeroDivisionError" in result["error"]

    def test_run_tests_all_pass(self) -> None:
        """Test running multiple test cases that all pass."""
        code = "def solution(x):\n    return x * 2"
        test_cases = [
            {"input": 1, "expected": 2},
            {"input": 5, "expected": 10},
            {"input": 0, "expected": 0},
        ]

        result = self.runner.run_tests(code, test_cases)

        assert result["all_passed"] is True
        assert result["tests_passed"] == 3
        assert result["tests_total"] == 3

    def test_run_tests_partial_pass(self) -> None:
        """Test running tests where some fail."""
        code = "def solution(x):\n    return x + 1"
        test_cases = [
            {"input": 1, "expected": 2},
            {"input": 5, "expected": 10},
        ]

        result = self.runner.run_tests(code, test_cases)

        assert result["all_passed"] is False
        assert result["tests_passed"] == 1
        assert result["tests_total"] == 2

    def test_run_tests_empty(self) -> None:
        """Test handling of empty test cases list."""
        code = "def solution(x):\n    return x"
        result = self.runner.run_tests(code, [])

        assert result["all_passed"] is False
        assert result["error"] is not None

    def test_validate_code_valid(self) -> None:
        """Test validating syntactically correct code."""
        code = "def solution(x):\n    return x * 2"
        result = self.runner.validate_code(code)

        assert result["valid"] is True
        assert result["error"] is None

    def test_validate_code_invalid(self) -> None:
        """Test validating code with syntax errors."""
        code = "def solution(x)\n    return x"
        result = self.runner.validate_code(code)

        assert result["valid"] is False
        assert "Syntax Error" in result["error"]
