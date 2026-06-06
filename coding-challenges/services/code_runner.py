"""Code execution service for safely running user-submitted code."""

import time
import traceback
from typing import Any
from io import StringIO
import sys


class CodeRunner:
    """Safely executes user-submitted code against test cases.

    Provides sandboxed execution with timeout protection and
    output capturing for grading code submissions.

    Attributes:
        timeout: Maximum execution time in seconds.
        max_output_length: Maximum length of captured output.
    """

    def __init__(self, timeout: int = 5, max_output_length: int = 5000) -> None:
        """Initialize the CodeRunner.

        Args:
            timeout: Maximum execution time in seconds.
            max_output_length: Maximum allowed output length.
        """
        self.timeout = timeout
        self.max_output_length = max_output_length

    def execute_code(self, code: str, test_input: Any) -> dict:
        """Execute submitted code with a given test input.

        Creates an isolated namespace and runs the user's code,
        capturing the return value from a 'solution' function.

        Args:
            code: The user's submitted Python code.
            test_input: Input to pass to the solution function.

        Returns:
            Dictionary with 'output', 'error', and 'execution_time' keys.
        """
        result = {"output": None, "error": None, "execution_time": 0.0}

        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        namespace = {"__builtins__": __builtins__}

        start_time = time.time()

        try:
            exec(code, namespace)

            if "solution" not in namespace:
                result["error"] = "No 'solution' function found in your code."
                return result

            if isinstance(test_input, list):
                output = namespace["solution"](*test_input)
            else:
                output = namespace["solution"](test_input)

            result["output"] = output
            result["execution_time"] = time.time() - start_time

        except TimeoutError:
            result["error"] = f"Execution timed out after {self.timeout} seconds."
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {str(e)}"
            result["execution_time"] = time.time() - start_time
        finally:
            sys.stdout = old_stdout

        return result

    def run_tests(self, code: str, test_cases: list[dict]) -> dict:
        """Run code against all provided test cases.

        Args:
            code: The user's submitted Python code.
            test_cases: List of test case dicts with 'input' and 'expected' keys.

        Returns:
            Dictionary with overall results including pass/fail counts
            and individual test results.
        """
        results = {
            "all_passed": False,
            "tests_passed": 0,
            "tests_total": len(test_cases),
            "test_results": [],
            "execution_time": 0.0,
            "error": None,
        }

        if not test_cases:
            results["error"] = "No test cases available for this challenge."
            return results

        total_time = 0.0

        for i, test_case in enumerate(test_cases):
            test_input = test_case.get("input")
            expected = test_case.get("expected")

            execution = self.execute_code(code, test_input)
            total_time += execution.get("execution_time", 0.0)

            passed = execution["output"] == expected and execution["error"] is None

            test_result = {
                "test_number": i + 1,
                "input": test_input,
                "expected": expected,
                "actual": execution["output"],
                "passed": passed,
                "error": execution["error"],
            }

            results["test_results"].append(test_result)

            if passed:
                results["tests_passed"] += 1

            if execution["error"] and not results["error"]:
                results["error"] = execution["error"]

        results["execution_time"] = total_time
        results["all_passed"] = results["tests_passed"] == results["tests_total"]

        return results

    def validate_code(self, code: str) -> dict:
        """Validate code syntax without executing it.

        Args:
            code: The code string to validate.

        Returns:
            Dictionary with 'valid' boolean and optional 'error' message.
        """
        try:
            compile(code, "<submission>", "exec")
            return {"valid": True, "error": None}
        except SyntaxError as e:
            return {"valid": False, "error": f"Syntax Error on line {e.lineno}: {e.msg}"}
