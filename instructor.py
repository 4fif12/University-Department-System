"""
instructor.py — Instructor class for UniDept Management System.

Represents a faculty member in the department who may be assigned
to teach one or more courses.
"""


class Instructor:
    """A department instructor with course assignment capabilities.

    Attributes:
        instructor_id (int): Unique identifier for the instructor.
        name (str): Full name of the instructor.
        department (str): Department the instructor belongs to.
        assigned_courses (list[str]): Course codes assigned to teach.
    """

    def __init__(self, instructor_id, name, department, assigned_courses=None):
        """Initialise an Instructor instance.

        Args:
            instructor_id (int): Unique instructor identifier.
            name (str): Full name.
            department (str): Department name.
            assigned_courses (list[str], optional): Pre-existing
                course assignments. Defaults to an empty list.
        """
        self.instructor_id = int(instructor_id)
        self.name = name
        self.department = department
        self.assigned_courses = (
            assigned_courses if assigned_courses else []
        )

    # ------------------------------------------------------------------
    # Core Methods
    # ------------------------------------------------------------------

    def assign_course(self, course_code):
        """Assign a course to this instructor.

        Args:
            course_code (str): The code of the course to assign.

        Returns:
            bool: True if the course was assigned, False if already
                assigned.
        """
        course_code = course_code.upper()

        if course_code in self.assigned_courses:
            return False

        self.assigned_courses.append(course_code)

        return True

    def unassign_course(self, course_code):
        """Remove a course assignment from this instructor.

        Args:
            course_code (str): The code of the course to remove.

        Returns:
            bool: True if the course was removed, False if it was
                not assigned.
        """
        course_code = course_code.upper()

        if course_code in self.assigned_courses:
            self.assigned_courses.remove(course_code)
            return True

        return False

    def get_courses(self):
        """Return the list of courses this instructor is teaching.

        Returns:
            list[str]: A copy of the assigned course codes.
        """
        return list(self.assigned_courses)

    def to_dict(self):
        """Serialise the instructor to a dictionary for CSV output.

        Returns:
            dict: Keys match the CSV column headers.
        """
        return {
            "instructor_id": self.instructor_id,
            "name": self.name,
            "department": self.department,
            "assigned_courses": ";".join(self.assigned_courses),
        }

    def __str__(self):
        """Return a human-readable representation of the instructor.

        Returns:
            str: Formatted instructor summary.
        """
        courses = (
            ", ".join(self.assigned_courses)
            if self.assigned_courses else "None"
        )

        return (
            f"[ID: {self.instructor_id}] {self.name} "
            f"({self.department}) — Courses: {courses}"
        )

    def __repr__(self):
        """Return an unambiguous string representation.

        Returns:
            str: Constructor-style representation.
        """
        return (
            f"Instructor({self.instructor_id}, '{self.name}', "
            f"'{self.department}', {self.assigned_courses})"
        )
