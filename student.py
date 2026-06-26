"""
student.py — Student class for UniDept Management System.

Represents a student enrolled in a university department, tracking
their personal details and the courses they are registered for.
"""

from utils import DuplicateEnrollmentError


class Student:
    """A university student with enrollment capabilities.

    Attributes:
        student_id (int): Unique identifier for the student.
        name (str): Full name of the student.
        email (str): Email address of the student.
        enrolled_courses (list[str]): Course codes the student is
            currently enrolled in.
    """

    def __init__(self, student_id, name, email, enrolled_courses=None):
        """Initialise a Student instance.

        Args:
            student_id (int): Unique student identifier.
            name (str): Full name.
            email (str): Email address.
            enrolled_courses (list[str], optional): Pre-existing
                course enrolments. Defaults to an empty list.
        """
        self.student_id = int(student_id)
        self.name = name
        self.email = email
        self.enrolled_courses = enrolled_courses if enrolled_courses else []

    # ------------------------------------------------------------------
    # Core Methods
    # ------------------------------------------------------------------

    def enroll(self, course_code):
        """Enrol the student in a course.

        Args:
            course_code (str): The code of the course to enrol in.

        Returns:
            bool: True if enrolment succeeded.

        Raises:
            DuplicateEnrollmentError: If the student is already
                enrolled in this course.
        """
        if course_code in self.enrolled_courses:
            raise DuplicateEnrollmentError(
                f"Student {self.student_id} is already enrolled "
                f"in {course_code}."
            )

        self.enrolled_courses.append(course_code)

        return True

    def drop_course(self, course_code):
        """Remove the student from a course.

        Args:
            course_code (str): The code of the course to drop.

        Returns:
            bool: True if the course was dropped, False if the
                student was not enrolled in it.
        """
        if course_code in self.enrolled_courses:
            self.enrolled_courses.remove(course_code)
            return True
        return False

    def get_courses(self):
        """Return the list of courses the student is enrolled in.

        Returns:
            list[str]: A copy of the enrolled course codes.
        """
        return list(self.enrolled_courses)

    def to_dict(self):
        """Serialise the student to a dictionary for CSV output.

        Returns:
            dict: Keys match the CSV column headers.
        """
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "enrolled_courses": ";".join(self.enrolled_courses),
        }

    def __str__(self):
        """Return a human-readable representation of the student.

        Returns:
            str: Formatted student summary.
        """
        courses = (
            ", ".join(self.enrolled_courses)
            if self.enrolled_courses else "None"
        )

        return (
            f"[ID: {self.student_id}] {self.name} ({self.email}) "
            f"— Courses: {courses}"
        )

    def __repr__(self):
        """Return an unambiguous string representation.

        Returns:
            str: Constructor-style representation.
        """
        return (
            f"Student({self.student_id}, '{self.name}', "
            f"'{self.email}', {self.enrolled_courses})"
        )
