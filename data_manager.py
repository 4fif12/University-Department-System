"""
data_manager.py — Data persistence module for UniDept Management System.

Handles all CSV file I/O operations and provides transactional
enrolment to keep Student and Course objects in sync.  Uses a
write-to-temp-then-rename strategy for basic crash safety.
"""

import csv
import os
import tempfile

from student import Student
from course import Course
from instructor import Instructor
from gradebook import GradeBook

# ---------------------------------------------------------------------------
# Path Constants
# ---------------------------------------------------------------------------

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

STUDENTS_FILE = os.path.join(DATA_DIR, "students.csv")
COURSES_FILE = os.path.join(DATA_DIR, "courses.csv")
INSTRUCTORS_FILE = os.path.join(DATA_DIR, "instructors.csv")
GRADES_FILE = os.path.join(DATA_DIR, "grades.csv")

# ---------------------------------------------------------------------------
# Helper — Atomic Write
# ---------------------------------------------------------------------------


def _atomic_write_csv(filepath, fieldnames, rows):
    """Write rows to a CSV file using a temp-file-then-rename strategy.

    Args:
        filepath (str): Destination file path.
        fieldnames (list[str]): Column headers.
        rows (list[dict]): Row data as dictionaries.

    Raises:
        IOError: If writing or renaming fails.
    """
    directory = os.path.dirname(filepath)
    os.makedirs(directory, exist_ok=True)

    # Write to a temporary file in the same directory
    fd, tmp_path = tempfile.mkstemp(
        dir=directory, suffix=".tmp", prefix="unidept_"
    )

    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as tmp_file:
            writer = csv.DictWriter(tmp_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        # On Windows, remove destination first if it exists

        if os.path.exists(filepath):
            os.remove(filepath)
        os.rename(tmp_path, filepath)

    except Exception:
        # Clean up temp file on failure
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise

# ---------------------------------------------------------------------------
# Load Functions
# ---------------------------------------------------------------------------


def load_students(filepath=STUDENTS_FILE):
    """Load student records from a CSV file.

    Args:
        filepath (str): Path to the students CSV file.

    Returns:
        list[Student]: A list of Student objects.
    """
    students = []

    try:
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                enrolled = (
                    row["enrolled_courses"].split(";")

                    if row["enrolled_courses"]

                    else []
                )

                students.append(Student(
                    student_id=int(row["student_id"]),
                    name=row["name"],
                    email=row["email"],
                    enrolled_courses=enrolled,
                ))

    except FileNotFoundError:
        # No existing data check so that we can start fresh
        pass

    except Exception as exc:
        print(f"Warning: Could not load students — {exc}")

    return students


def load_courses(filepath=COURSES_FILE):
    """Load course records from a CSV file.

    Args:
        filepath (str): Path to the courses CSV file.

    Returns:
        list[Course]: A list of Course objects.
    """
    courses = []

    try:
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                enrolled = (
                    [int(sid) for sid in row["enrolled_students"].split(";")]

                    if row["enrolled_students"]

                    else []
                )

                instructor_id = (
                    row["instructor_id"]

                    if row["instructor_id"]

                    else None
                )

                courses.append(Course(
                    course_code=row["course_code"],
                    title=row["title"],
                    credits=int(row["credits"]),
                    max_enrollment=int(row["max_enrollment"]),
                    enrolled_students=enrolled,
                    instructor_id=instructor_id,
                ))

    except FileNotFoundError:
        pass

    except Exception as exc:
        print(f"Warning: Could not load courses — {exc}")

    return courses


def load_instructors(filepath=INSTRUCTORS_FILE):
    """Load instructor records from a CSV file.

    Args:
        filepath (str): Path to the instructors CSV file.

    Returns:
        list[Instructor]: A list of Instructor objects.
    """
    instructors = []

    try:
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                assigned = (
                    row["assigned_courses"].split(";")

                    if row["assigned_courses"]

                    else []
                )

                instructors.append(Instructor(
                    instructor_id=int(row["instructor_id"]),
                    name=row["name"],
                    department=row["department"],
                    assigned_courses=assigned,
                ))

    except FileNotFoundError:
        pass

    except Exception as exc:
        print(f"Warning: Could not load instructors — {exc}")

    return instructors


def load_grades(filepath=GRADES_FILE):
    """Load grade records from a CSV file into a GradeBook.

    Args:
        filepath (str): Path to the grades CSV file.

    Returns:
        GradeBook: A GradeBook populated with loaded entries.
    """
    entries = []

    try:
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                entries.append({
                    "student_id": int(row["student_id"]),
                    "course_code": row["course_code"].upper(),
                    "grade": row["grade"].upper(),
                })

    except FileNotFoundError:
        pass

    except Exception as exc:
        print(f"Warning: Could not load grades — {exc}")

    return GradeBook(entries)


# ---------------------------------------------------------------------------
# Save Functions
# ---------------------------------------------------------------------------

def save_students(students, filepath=STUDENTS_FILE):
    """Persist student records to a CSV file.

    Args:
        students (list[Student]): Student objects to save.
        filepath (str): Destination file path.
    """
    fieldnames = ["student_id", "name", "email", "enrolled_courses"]
    rows = [s.to_dict() for s in students]
    _atomic_write_csv(filepath, fieldnames, rows)


def save_courses(courses, filepath=COURSES_FILE):
    """Persist course records to a CSV file.

    Args:
        courses (list[Course]): Course objects to save.
        filepath (str): Destination file path.
    """

    fieldnames = [
        "course_code", "title", "credits", "max_enrollment",
        "enrolled_students", "instructor_id",
    ]

    rows = [c.to_dict() for c in courses]
    _atomic_write_csv(filepath, fieldnames, rows)


def save_instructors(instructors, filepath=INSTRUCTORS_FILE):
    """Persist instructor records to a CSV file.

    Args:
        instructors (list[Instructor]): Instructor objects to save.
        filepath (str): Destination file path.
    """
    fieldnames = ["instructor_id", "name", "department", "assigned_courses"]
    rows = [i.to_dict() for i in instructors]
    _atomic_write_csv(filepath, fieldnames, rows)


def save_grades(gradebook, filepath=GRADES_FILE):
    """Persist grade records to a CSV file.

    Args:
        gradebook (GradeBook): The GradeBook to save.
        filepath (str): Destination file path.
    """
    fieldnames = ["student_id", "course_code", "grade"]
    rows = gradebook.to_list()
    _atomic_write_csv(filepath, fieldnames, rows)


def save_all(students, courses, instructors, gradebook):
    """Save all data collections to their respective CSV files.

    Args:
        students (list[Student]): Student objects.
        courses (list[Course]): Course objects.
        instructors (list[Instructor]): Instructor objects.
        gradebook (GradeBook): Grade records.
    """
    save_students(students)
    save_courses(courses)
    save_instructors(instructors)
    save_grades(gradebook)


# ---------------------------------------------------------------------------
# ID Generation
# ---------------------------------------------------------------------------

def generate_student_id(students):
    """Generate the next available student ID.

    Args:
        students (list[Student]): Existing student objects.

    Returns:
        int: The next available ID (max + 1, or 1 if empty).
    """
    if not students:
        return 1
    return max(s.student_id for s in students) + 1


def generate_instructor_id(instructors):
    """Generate the next available instructor ID.

    Args:
        instructors (list[Instructor]): Existing instructor objects.

    Returns:
        int: The next available ID (max + 1, or 1 if empty).
    """
    if not instructors:
        return 1
    return max(i.instructor_id for i in instructors) + 1


# ---------------------------------------------------------------------------
# Uniqueness Checks
# ---------------------------------------------------------------------------

def find_student(students, student_id):
    """Find a student by ID.

    Args:
        students (list[Student]): The student collection.
        student_id (int): The ID to search for.

    Returns:
        Student or None: The matching student, or None.
    """
    student_id = int(student_id)
    for student in students:
        if student.student_id == student_id:
            return student
    return None


def find_course(courses, course_code):
    """Find a course by code.

    Args:
        courses (list[Course]): The course collection.
        course_code (str): The code to search for.

    Returns:
        Course or None: The matching course, or None.
    """
    course_code = course_code.upper()
    for course in courses:
        if course.course_code == course_code:
            return course
    return None


def find_instructor(instructors, instructor_id):
    """Find an instructor by ID.

    Args:
        instructors (list[Instructor]): The instructor collection.
        instructor_id (int): The ID to search for.

    Returns:
        Instructor or None: The matching instructor, or None.
    """
    instructor_id = int(instructor_id)
    for instructor in instructors:
        if instructor.instructor_id == instructor_id:
            return instructor
    return None


def course_code_exists(courses, course_code):
    """Check whether a course code already exists.

    Args:
        courses (list[Course]): The course collection.
        course_code (str): The code to check.

    Returns:
        bool: True if the code is already in use.
    """
    return find_course(courses, course_code) is not None


# ---------------------------------------------------------------------------
# Transactional Enrolment
# ---------------------------------------------------------------------------

def enroll_student_in_course(student, course):
    """Enrol a student in a course transactionally.

    Both the Student and Course objects are updated together.
    If either update fails, the operation is rolled back.

    Args:
        student (Student): The student to enrol.
        course (Course): The course to enrol in.

    Returns:
        bool: True if enrolment succeeded.

    Raises:
        CourseFullError: If the course is at capacity.
        DuplicateEnrollmentError: If already enrolled.
    """
    # Attempt course side first
    course.add_student(student.student_id)
    try:
        student.enroll(course.course_code)
    except Exception:
        # Roll back the course side change if any error occurs
        course.remove_student(student.student_id)
        raise
    return True


def drop_student_from_course(student, course):
    """Drop a student from a course transactionally.

    Both the Student and Course objects are updated together.

    Args:
        student (Student): The student to drop.
        course (Course): The course to drop from.

    Returns:
        bool: True if drop succeeded, False if the student was
            not enrolled.
    """
    removed_from_course = course.remove_student(student.student_id)
    removed_from_student = student.drop_course(course.course_code)
    return removed_from_course or removed_from_student
