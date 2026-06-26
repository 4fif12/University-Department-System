"""
gradebook.py — GradeBook class for UniDept Management System.

Manages grade entries that link students, courses, and letter grades,
and provides GPA calculation capabilities.
"""

from utils import validate_grade, GRADE_MAP


class GradeBook:
    """A grade registry tracking student performance across courses.

    Each entry is a dictionary with keys:
        - student_id (int)
        - course_code (str)
        - grade (str)  — one of A, B, C, D, F

    Attributes:
        entries (list[dict]): The collection of grade records.
    """

    def __init__(self, entries=None):
        """Initialise a GradeBook instance.

        Args:
            entries (list[dict], optional): Pre-existing grade
                entries. Defaults to an empty list.
        """
        self.entries = entries if entries else []

    # ------------------------------------------------------------------
    # Core Methods
    # ------------------------------------------------------------------

    def add_grade(self, student_id, course_code, grade):
        """Record a new grade for a student in a course.

        Args:
            student_id (int): The student's ID.
            course_code (str): The course code.
            grade (str): The letter grade (A–F).

        Returns:
            bool: True if the grade was recorded.

        Raises:
            InvalidGradeError: If the grade is not valid.
            ValueError: If a grade already exists for this
                student/course combination.
        """
        grade = validate_grade(grade)
        student_id = int(student_id)
        course_code = course_code.upper()

        # Check for existing entry
        for entry in self.entries:
            if (entry["student_id"] == student_id
                    and entry["course_code"] == course_code):
                raise ValueError(
                    f"A grade already exists for student "
                    f"{student_id} in {course_code}. "
                    f"Use update_grade() instead."
                )

        self.entries.append({
            "student_id": student_id,
            "course_code": course_code,
            "grade": grade,
        })

        return True

    def update_grade(self, student_id, course_code, new_grade):
        """Update an existing grade for a student in a course.

        Args:
            student_id (int): The student's ID.
            course_code (str): The course code.
            new_grade (str): The new letter grade (A–F).

        Returns:
            bool: True if the grade was updated.

        Raises:
            InvalidGradeError: If the new grade is not valid.
            ValueError: If no existing grade record is found.
        """
        new_grade = validate_grade(new_grade)
        student_id = int(student_id)
        course_code = course_code.upper()

        for entry in self.entries:
            if (entry["student_id"] == student_id
                    and entry["course_code"] == course_code):
                entry["grade"] = new_grade
                return True

        raise ValueError(
            f"No grade record found for student "
            f"{student_id} in {course_code}."
        )

    def get_student_grades(self, student_id):
        """Retrieve all grade entries for a specific student.

        Args:
            student_id (int): The student's ID.

        Returns:
            list[dict]: Grade entries for the student.
        """
        student_id = int(student_id)

        return [
            entry for entry in self.entries
            if entry["student_id"] == student_id
        ]

    def get_course_grades(self, course_code):
        """Retrieve all grade entries for a specific course.

        Args:
            course_code (str): The course code.

        Returns:
            list[dict]: Grade entries for the course.
        """
        course_code = course_code.upper()
        return [
            entry for entry in self.entries
            if entry["course_code"] == course_code
        ]

    def calculate_gpa(self, student_id):
        """Calculate the GPA for a student across all graded courses.

        Uses the GRADE_MAP to convert letter grades to numeric
        values and computes the unweighted average.

        Args:
            student_id (int): The student's ID.

        Returns:
            float: The computed GPA, or 0.0 if no grades exist.
        """
        grades = self.get_student_grades(student_id)

        if not grades:
            return 0.0

        total_points = sum(GRADE_MAP[g["grade"]] for g in grades)

        return round(total_points / len(grades), 2)

    def to_list(self):
        """Serialise all entries to a list of dicts for CSV output.

        Returns:
            list[dict]: Each dict has keys: student_id,
                course_code, grade.
        """
        return [dict(entry) for entry in self.entries]

    def __str__(self):
        """Return a human-readable summary of all grade entries.

        Returns:
            str: Formatted grade listing.
        """
        if not self.entries:
            return "GradeBook: (empty)"

        lines = ["GradeBook:"]

        for entry in self.entries:
            lines.append(
                f"  Student {entry['student_id']} — "
                f"{entry['course_code']}: {entry['grade']}"
            )

        return "\n".join(lines)

    def __repr__(self):
        """Return an unambiguous string representation.

        Returns:
            str: Constructor-style representation.
        """
        return f"GradeBook({self.entries})"
