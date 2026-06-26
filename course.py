"""
course.py — Course class for UniDept Management System.

Represents an academic course offered by the department, tracking
its details, enrolled students, and assigned instructor.
"""

from utils import CourseFullError, DuplicateEnrollmentError


class Course:
    """An academic course with enrolment management.

    Attributes:
        course_code (str): Unique code identifying the course (e.g. "CS101").
        title (str): Descriptive title of the course.
        credits (int): Number of credit hours.
        max_enrollment (int): Maximum number of students allowed.
        enrolled_students (list[int]): Student IDs currently enrolled.
        instructor_id (int or None): ID of the assigned instructor.
    """

    def __init__(self, course_code, title, credits, max_enrollment,
                 enrolled_students=None, instructor_id=None):
        """Initialise a Course instance.

        Args:
            course_code (str): Unique course code.
            title (str): Course title.
            credits (int): Credit hours.
            max_enrollment (int): Capacity limit.
            enrolled_students (list[int], optional): Pre-enrolled
                student IDs. Defaults to an empty list.
            instructor_id (int or None, optional): Assigned instructor.
        """
        self.course_code = course_code.upper()
        self.title = title
        self.credits = int(credits)
        self.max_enrollment = int(max_enrollment)
        self.enrolled_students = enrolled_students if enrolled_students else []
        self.instructor_id = (
            int(instructor_id) if instructor_id is not None
            and str(instructor_id).strip() != "" else None
        )

    # ------------------------------------------------------------------
    # Core Methods
    # ------------------------------------------------------------------

    def add_student(self, student_id):
        """Add a student to the course roster.

        Args:
            student_id (int): The student's ID.

        Returns:
            bool: True if the student was added successfully.

        Raises:
            CourseFullError: If the course is at maximum capacity.
            DuplicateEnrollmentError: If the student is already
                enrolled.
        """
        student_id = int(student_id)

        if self.is_full():
            raise CourseFullError(
                f"Course {self.course_code} is full "
                f"({self.max_enrollment}/{self.max_enrollment})."
            )

        if student_id in self.enrolled_students:
            raise DuplicateEnrollmentError(
                f"Student {student_id} is already enrolled "
                f"in {self.course_code}."
            )

        self.enrolled_students.append(student_id)

        return True

    def remove_student(self, student_id):
        """Remove a student from the course roster.

        Args:
            student_id (int): The student's ID.

        Returns:
            bool: True if the student was removed, False if not found.
        """
        student_id = int(student_id)

        if student_id in self.enrolled_students:
            self.enrolled_students.remove(student_id)
            return True
        return False

    def is_full(self):
        """Check whether the course has reached its capacity.

        Returns:
            bool: True if enrolled students >= max_enrollment.
        """
        return len(self.enrolled_students) >= self.max_enrollment

    def get_roster(self):
        """Return a copy of the enrolled student ID list.

        Returns:
            list[int]: Enrolled student IDs.
        """
        return list(self.enrolled_students)

    def assign_instructor(self, instructor_id):
        """Assign an instructor to this course.

        Args:
            instructor_id (int): The instructor's ID.
        """
        self.instructor_id = int(instructor_id)

    def to_dict(self):
        """Serialise the course to a dictionary for CSV output.

        Returns:
            dict: Keys match the CSV column headers.
        """
        return {
            "course_code": self.course_code,
            "title": self.title,
            "credits": self.credits,
            "max_enrollment": self.max_enrollment,
            "enrolled_students": ";".join(
                str(sid) for sid in self.enrolled_students
            ),
            "instructor_id": (
                self.instructor_id if self.instructor_id is not None else ""
            ),
        }

    def __str__(self):
        """Return a human-readable representation of the course.

        Returns:
            str: Formatted course summary.
        """
        enrolled = len(self.enrolled_students)
        instructor = self.instructor_id if self.instructor_id else "Unassigned"

        return (
            f"[{self.course_code}] {self.title} "
            f"({self.credits} credits) — "
            f"Enrolled: {enrolled}/{self.max_enrollment}, "
            f"Instructor: {instructor}"
        )

    def __repr__(self):
        """Return an unambiguous string representation.

        Returns:
            str: Constructor-style representation.
        """
        return (
            f"Course('{self.course_code}', '{self.title}', "
            f"{self.credits}, {self.max_enrollment}, "
            f"{self.enrolled_students}, {self.instructor_id})"
        )
