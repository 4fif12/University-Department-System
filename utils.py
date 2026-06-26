"""
utils.py — Utility module for UniDept Management System.

Contains custom exceptions, input validation helpers, grade
mapping constants, and table formatting utilities used across
all other modules.
"""

import re

# ---------------------------------------------------------------------------
# Grade Constants
# ---------------------------------------------------------------------------

VALID_GRADES = {"A", "B", "C", "D", "F"}

GRADE_MAP = {
    "A": 4.0,
    "B": 3.0,
    "C": 2.0,
    "D": 1.0,
    "F": 0.0,
}

# ---------------------------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------------------------


class StudentNotFoundError(Exception):
    """Raised when a student ID does not exist in the system."""


class CourseNotFoundError(Exception):
    """Raised when a course code does not exist in the system."""


class InstructorNotFoundError(Exception):
    """Raised when an instructor ID does not exist in the system."""


class CourseFullError(Exception):
    """Raised when attempting to enroll in a course that is at capacity."""


class DuplicateEnrollmentError(Exception):
    """Raised when a student is already enrolled in the specified course."""


class InvalidGradeError(Exception):
    """Raised when a grade value is not one of the valid letter grades."""


class DuplicateIDError(Exception):
    """Raised when attempting to create a record with an ID that exists."""

# ---------------------------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------------------------


def validate_email(email):
    """Validate an email address using a basic regex pattern.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email matches the pattern, False otherwise.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    return bool(re.match(pattern, email))


def sanitize_input(text):
    """Sanitize user input by stripping leading/trailing whitespace.

    The Python csv module handles quoting of commas and special
    characters automatically, so we only need to strip whitespace.

    Args:
        text (str): The raw user input.

    Returns:
        str: The sanitized string.
    """
    return text.strip()


def validate_grade(grade):
    """Check whether a grade string is a valid letter grade.

    Args:
        grade (str): The grade to validate (case-insensitive).

    Returns:
        str: The uppercase valid grade.

    Raises:
        InvalidGradeError: If the grade is not in VALID_GRADES.
    """
    grade_upper = grade.strip().upper()

    if grade_upper not in VALID_GRADES:
        raise InvalidGradeError(
            f"'{grade}' is not a valid grade. Valid grades are: "
            f"{', '.join(sorted(VALID_GRADES))}"
        )
    return grade_upper


# ---------------------------------------------------------------------------
# Display / Formatting Helpers
# ---------------------------------------------------------------------------

def format_table(headers, rows):
    """Format data as an aligned text table.

    Args:
        headers (list[str]): Column header labels.
        rows (list[list[str]]): Row data; each inner list is one row.

    Returns:
        str: The formatted table as a multi-line string.
    """
    if not rows:
        return "(No data to display)"

    # Convert every cell to a string
    str_rows = [[str(cell) for cell in row] for row in rows]
    str_headers = [str(h) for h in headers]

    # Determine the maximum width of each column
    col_widths = [len(h) for h in str_headers]

    for row in str_rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(cell))

    # Build the separator and format strings
    separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    row_fmt = "| " + " | ".join(f"{{:<{w}}}" for w in col_widths) + " |"

    lines = [separator, row_fmt.format(*str_headers), separator]

    for row in str_rows:
        lines.append(row_fmt.format(*row))

    lines.append(separator)

    return "\n".join(lines)


def confirm_action(prompt="Are you sure? (y/n): "):
    """Ask the user for a yes/no confirmation.

    Args:
        prompt (str): The confirmation prompt to display.

    Returns:
        bool: True if the user entered 'y' or 'yes', False otherwise.
    """
    response = input(prompt).strip().lower()

    return response in ("y", "yes")
