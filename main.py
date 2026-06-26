"""
main.py — Entry point for UniDept Management System.

Provides an interactive, menu-driven command-line interface for
managing students, courses, instructors, and grades in a university
department.
"""


from student import Student
from course import Course
from instructor import Instructor
from utils import (
    sanitize_input,
    validate_email,
    format_table,
    confirm_action,
    GRADE_MAP,
    CourseFullError,
    DuplicateEnrollmentError,
    InvalidGradeError,
)
import data_manager as dm

# ======================================================================
# Display Helpers
# ======================================================================


def print_header(title):
    """Print a formatted section header.

    Args:
        title (str): The section title to display.
    """
    width = 44

    print()
    print("+" + "=" * width + "+")
    print("|" + title.center(width) + "|")
    print("+" + "=" * width + "+")


def print_menu(options):
    """Print a numbered menu from a list of option strings.

    Args:
        options (list[str]): Menu option labels.
    """
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    print("  0. Back to Main Menu")
    print()


def get_choice(prompt="Enter your choice: "):
    """Read and return a menu choice from the user.

    Args:
        prompt (str): The input prompt.

    Returns:
        str: The stripped user input.
    """
    return input(prompt).strip()


# ======================================================================
# Student Management
# ======================================================================

def student_menu(students, courses):
    """Handle the Student Management submenu.

    Args:
        students (list[Student]): Current student list.
        courses (list[Course]): Current course list.
    """
    while True:
        print_header("Student Management")

        print_menu([
            "Add New Student",
            "View All Students",
            "Search Student by ID",
            "Enrol Student in Course",
            "Drop Student from Course",
            "Remove Student",
        ])

        choice = get_choice()

        if choice == "0":
            break

        elif choice == "1":
            _add_student(students)

        elif choice == "2":
            _view_all_students(students)

        elif choice == "3":
            _search_student(students)

        elif choice == "4":
            _enroll_student(students, courses)

        elif choice == "5":
            _drop_student(students, courses)

        elif choice == "6":
            _remove_student(students, courses)

        else:
            print("Invalid choice. Please try again.")


def _add_student(students):
    """Add a new student to the system."""
    print("\n--- Add New Student ---")

    name = sanitize_input(input("Enter student name: "))

    if not name:
        print("Error: Name cannot be empty.")
        return

    email = sanitize_input(input("Enter student email: "))

    if not validate_email(email):
        print("Error: Invalid email format.")
        return

    student_id = dm.generate_student_id(students)
    new_student = Student(student_id, name, email)
    students.append(new_student)
    print(f"Student added successfully: {new_student}")


def _view_all_students(students):
    """Display all students in a formatted table."""
    if not students:
        print("\nNo students in the system.")
        return

    headers = ["ID", "Name", "Email", "Courses"]

    rows = []

    for s in students:
        courses_str = (
            ", ".join(s.enrolled_courses)
            if s.enrolled_courses else "None"
        )
        rows.append([s.student_id, s.name, s.email, courses_str])

    print()
    print(format_table(headers, rows))


def _search_student(students):
    """Search for a student by ID and display their details."""
    try:
        student_id = int(input("\nEnter student ID: "))

    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    student = dm.find_student(students, student_id)

    if student:
        print(f"\n{student}")

    else:
        print(f"Error: Student with ID {student_id} not found.")


def _enroll_student(students, courses):
    """Enrol a student in a course."""
    try:
        student_id = int(input("\nEnter student ID: "))

    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    student = dm.find_student(students, student_id)

    if not student:
        print(f"Error: Student with ID {student_id} not found.")
        return

    course_code = sanitize_input(input("Enter course code: ")).upper()
    course = dm.find_course(courses, course_code)

    if not course:
        print(f"Error: Course '{course_code}' not found.")
        return

    try:
        dm.enroll_student_in_course(student, course)
        print(f"Student {student.name} enrolled in {course.title}.")

    except (CourseFullError, DuplicateEnrollmentError) as exc:
        print(f"Error: {exc}")


def _drop_student(students, courses):
    """Drop a student from a course."""
    try:
        student_id = int(input("\nEnter student ID: "))

    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    student = dm.find_student(students, student_id)

    if not student:
        print(f"Error: Student with ID {student_id} not found.")
        return

    course_code = sanitize_input(input("Enter course code: ")).upper()
    course = dm.find_course(courses, course_code)

    if not course:
        print(f"Error: Course '{course_code}' not found.")
        return

    if not confirm_action(
        f"Drop {student.name} from {course.title}? (y/n): "
    ):
        print("Operation cancelled.")
        return

    if dm.drop_student_from_course(student, course):
        print(f"Student {student.name} dropped from {course.title}.")

    else:
        print(f"Student {student.name} was not enrolled in {course.title}.")


def _remove_student(students, courses):
    """Remove a student from the system entirely."""
    try:
        student_id = int(input("\nEnter student ID to remove: "))

    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    student = dm.find_student(students, student_id)
    if not student:
        print(f"Error: Student with ID {student_id} not found.")
        return

    if not confirm_action(
        f"Remove {student.name} permanently? (y/n): "
    ):
        print("Operation cancelled.")
        return

    # Remove from all enrolled courses
    for code in list(student.enrolled_courses):
        course = dm.find_course(courses, code)

        if course:
            course.remove_student(student.student_id)

    students.remove(student)
    print(f"Student {student.name} (ID: {student_id}) has been removed.")


# ======================================================================
# Course Management
# ======================================================================

def course_menu(courses, instructors):
    """Handle the Course Management submenu.

    Args:
        courses (list[Course]): Current course list.
        instructors (list[Instructor]): Current instructor list.
    """
    while True:
        print_header("Course Management")

        print_menu([
            "Add New Course",
            "View All Courses",
            "Search Course by Code",
            "Assign Instructor to Course",
            "View Course Roster",
            "Remove Course",
        ])

        choice = get_choice()

        if choice == "0":
            break

        elif choice == "1":
            _add_course(courses)

        elif choice == "2":
            _view_all_courses(courses)

        elif choice == "3":
            _search_course(courses)

        elif choice == "4":
            _assign_instructor(courses, instructors)

        elif choice == "5":
            _view_roster(courses)

        elif choice == "6":
            _remove_course(courses, instructors)

        else:
            print("Invalid choice. Please try again.")


def _add_course(courses):
    """Add a new course to the system."""
    print("\n--- Add New Course ---")

    code = sanitize_input(input("Enter course code (e.g. CS101): ")).upper()

    if not code:
        print("Error: Course code cannot be empty.")
        return

    if dm.course_code_exists(courses, code):
        print(f"Error: Course code '{code}' already exists.")
        return

    title = sanitize_input(input("Enter course title: "))

    if not title:
        print("Error: Title cannot be empty.")
        return

    try:
        credits = int(input("Enter credits: "))
        max_enroll = int(input("Enter maximum enrolment: "))

    except ValueError:
        print("Error: Credits and max enrolment must be numbers.")
        return

    if credits <= 0 or max_enroll <= 0:
        print("Error: Credits and max enrolment must be positive.")
        return

    new_course = Course(code, title, credits, max_enroll)
    courses.append(new_course)

    print(f"Course added successfully: {new_course}")


def _view_all_courses(courses):
    """Display all courses in a formatted table."""
    if not courses:
        print("\nNo courses in the system.")
        return

    headers = ["Code", "Title", "Credits", "Enrolled", "Max", "Instructor"]

    rows = []

    for c in courses:
        inst = c.instructor_id if c.instructor_id else "N/A"
        rows.append([
            c.course_code, c.title, c.credits,
            len(c.enrolled_students), c.max_enrollment, inst,
        ])

    print()
    print(format_table(headers, rows))


def _search_course(courses):
    """Search for a course by code and display its details."""
    code = sanitize_input(input("\nEnter course code: ")).upper()
    course = dm.find_course(courses, code)

    if course:
        print(f"\n{course}")

    else:
        print(f"Error: Course '{code}' not found.")


def _assign_instructor(courses, instructors):
    """Assign an instructor to a course."""
    code = sanitize_input(input("\nEnter course code: ")).upper()
    course = dm.find_course(courses, code)

    if not course:
        print(f"Error: Course '{code}' not found.")
        return

    try:
        inst_id = int(input("Enter instructor ID: "))

    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    instructor = dm.find_instructor(instructors, inst_id)

    if not instructor:
        print(f"Error: Instructor with ID {inst_id} not found.")
        return

    course.assign_instructor(instructor.instructor_id)
    instructor.assign_course(course.course_code)

    print(
        f"Instructor {instructor.name} assigned to "
        f"{course.course_code} ({course.title})."
    )


def _view_roster(courses):
    """Display the enrolment roster for a course."""
    code = sanitize_input(input("\nEnter course code: ")).upper()
    course = dm.find_course(courses, code)

    if not course:
        print(f"Error: Course '{code}' not found.")
        return

    roster = course.get_roster()

    if not roster:
        print(f"\nCourse {course.course_code} has no enrolled students.")

    else:
        print(f"\nRoster for {course.course_code} — {course.title}:")
        for sid in roster:
            print(f"  - Student ID: {sid}")


def _remove_course(courses, instructors):
    """Remove a course from the system."""
    code = sanitize_input(input("\nEnter course code to remove: ")).upper()
    course = dm.find_course(courses, code)

    if not course:
        print(f"Error: Course '{code}' not found.")
        return

    if not confirm_action(
        f"Remove course {course.course_code} ({course.title})? (y/n): "
    ):
        print("Operation cancelled.")
        return

    # Unassign instructor
    if course.instructor_id:
        inst = dm.find_instructor(instructors, course.instructor_id)

        if inst:
            inst.unassign_course(course.course_code)

    courses.remove(course)

    print(f"Course {code} has been removed.")


# ======================================================================
# Instructor Management
# ======================================================================

def instructor_menu(instructors, courses):
    """Handle the Instructor Management submenu.

    Args:
        instructors (list[Instructor]): Current instructor list.
        courses (list[Course]): Current course list.
    """
    while True:
        print_header("Instructor Management")

        print_menu([
            "Add New Instructor",
            "View All Instructors",
            "Search Instructor by ID",
            "Remove Instructor",
        ])

        choice = get_choice()

        if choice == "0":
            break

        elif choice == "1":
            _add_instructor(instructors)

        elif choice == "2":
            _view_all_instructors(instructors)

        elif choice == "3":
            _search_instructor(instructors)

        elif choice == "4":
            _remove_instructor(instructors, courses)

        else:
            print("Invalid choice. Please try again.")


def _add_instructor(instructors):
    """Add a new instructor to the system."""
    print("\n--- Add New Instructor ---")

    name = sanitize_input(input("Enter instructor name: "))

    if not name:
        print("Error: Name cannot be empty.")
        return

    department = sanitize_input(input("Enter department: "))

    if not department:
        print("Error: Department cannot be empty.")
        return

    inst_id = dm.generate_instructor_id(instructors)
    new_instructor = Instructor(inst_id, name, department)
    instructors.append(new_instructor)

    print(f"Instructor added successfully: {new_instructor}")


def _view_all_instructors(instructors):
    """Display all instructors in a formatted table."""
    if not instructors:
        print("\nNo instructors in the system.")
        return

    headers = ["ID", "Name", "Department", "Courses"]

    rows = []

    for i in instructors:
        courses_str = (
            ", ".join(i.assigned_courses) if i.assigned_courses else "None"
        )
        rows.append([i.instructor_id, i.name, i.department, courses_str])

    print()
    print(format_table(headers, rows))


def _search_instructor(instructors):
    """Search for an instructor by ID and display their details."""
    try:
        inst_id = int(input("\nEnter instructor ID: "))

    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    instructor = dm.find_instructor(instructors, inst_id)

    if instructor:
        print(f"\n{instructor}")

    else:
        print(f"Error: Instructor with ID {inst_id} not found.")


def _remove_instructor(instructors, courses):
    """Remove an instructor from the system."""
    try:
        inst_id = int(input("\nEnter instructor ID to remove: "))

    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    instructor = dm.find_instructor(instructors, inst_id)

    if not instructor:
        print(f"Error: Instructor with ID {inst_id} not found.")
        return

    if not confirm_action(
        f"Remove {instructor.name} permanently? (y/n): "
    ):
        print("Operation cancelled.")
        return

    # Unassign from all courses
    for code in list(instructor.assigned_courses):
        course = dm.find_course(courses, code)

        if course and course.instructor_id == instructor.instructor_id:
            course.instructor_id = None

    instructors.remove(instructor)

    print(
        f"Instructor {instructor.name} (ID: {inst_id}) has been removed."
    )


# ======================================================================
# Grade Management
# ======================================================================

def grade_menu(students, courses, gradebook):
    """Handle the Grade Management submenu.

    Args:
        students (list[Student]): Current student list.
        courses (list[Course]): Current course list.
        gradebook (GradeBook): The grade registry.
    """
    while True:
        print_header("Grade Management")

        print_menu([
            "Add Grade",
            "Update Grade",
            "View Student Grades",
            "View Course Grades",
        ])

        choice = get_choice()

        if choice == "0":
            break

        elif choice == "1":
            _add_grade(students, courses, gradebook)

        elif choice == "2":
            _update_grade(students, courses, gradebook)

        elif choice == "3":
            _view_student_grades(students, gradebook)

        elif choice == "4":
            _view_course_grades(courses, gradebook)

        else:
            print("Invalid choice. Please try again.")


def _add_grade(students, courses, gradebook):
    """Add a new grade entry."""
    try:
        student_id = int(input("\nEnter student ID: "))

    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    if not dm.find_student(students, student_id):
        print(f"Error: Student with ID {student_id} not found.")
        return

    course_code = sanitize_input(input("Enter course code: ")).upper()

    if not dm.find_course(courses, course_code):
        print(f"Error: Course '{course_code}' not found.")
        return

    grade_input = sanitize_input(input("Enter grade (A/B/C/D/F): "))

    try:
        gradebook.add_grade(student_id, course_code, grade_input)

        print(
            f"Grade '{grade_input.upper()}' recorded for "
            f"student {student_id} in {course_code}."
        )

    except (InvalidGradeError, ValueError) as exc:
        print(f"Error: {exc}")


def _update_grade(students, courses, gradebook):
    """Update an existing grade entry."""
    try:
        student_id = int(input("\nEnter student ID: "))

    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    if not dm.find_student(students, student_id):
        print(f"Error: Student with ID {student_id} not found.")
        return

    course_code = sanitize_input(input("Enter course code: ")).upper()

    if not dm.find_course(courses, course_code):
        print(f"Error: Course '{course_code}' not found.")
        return

    new_grade = sanitize_input(input("Enter new grade (A/B/C/D/F): "))

    try:
        gradebook.update_grade(student_id, course_code, new_grade)
        print(
            f"Grade updated to '{new_grade.upper()}' for "
            f"student {student_id} in {course_code}."
        )

    except (InvalidGradeError, ValueError) as exc:
        print(f"Error: {exc}")


def _view_student_grades(students, gradebook):
    """View all grades and GPA for a specific student."""
    try:
        student_id = int(input("\nEnter student ID: "))

    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    student = dm.find_student(students, student_id)

    if not student:
        print(f"Error: Student with ID {student_id} not found.")
        return

    grades = gradebook.get_student_grades(student_id)

    if not grades:
        print(f"\nNo grades recorded for {student.name}.")
        return

    print(f"\nTranscript for {student.name} (ID: {student_id}):")

    headers = ["Course", "Grade", "Points"]

    rows = [
        [g["course_code"], g["grade"], GRADE_MAP[g["grade"]]]
        for g in grades
    ]

    print(format_table(headers, rows))

    gpa = gradebook.calculate_gpa(student_id)

    print(f"  GPA: {gpa:.2f}")


def _view_course_grades(courses, gradebook):
    """View all grades for a specific course."""
    code = sanitize_input(input("\nEnter course code: ")).upper()
    course = dm.find_course(courses, code)

    if not course:
        print(f"Error: Course '{code}' not found.")
        return

    grades = gradebook.get_course_grades(code)

    if not grades:
        print(f"\nNo grades recorded for {course.title}.")
        return

    print(f"\nGrades for {course.course_code} — {course.title}:")

    headers = ["Student ID", "Grade", "Points"]
    rows = [
        [g["student_id"], g["grade"], GRADE_MAP[g["grade"]]]
        for g in grades
    ]

    print(format_table(headers, rows))


# ======================================================================
# Reports
# ======================================================================

def reports_menu(students, courses, instructors, gradebook):
    """Handle the Reports submenu.

    Args:
        students (list[Student]): Current student list.
        courses (list[Course]): Current course list.
        instructors (list[Instructor]): Current instructor list.
        gradebook (GradeBook): The grade registry.
    """
    while True:
        print_header("Reports")

        print_menu([
            "All Students Summary",
            "All Courses Summary",
            "All Instructors Summary",
            "Student Transcript",
            "Course Grade Distribution",
        ])

        choice = get_choice()

        if choice == "0":
            break

        elif choice == "1":
            _view_all_students(students)

        elif choice == "2":
            _view_all_courses(courses)

        elif choice == "3":
            _view_all_instructors(instructors)

        elif choice == "4":
            _view_student_grades(students, gradebook)

        elif choice == "5":
            _grade_distribution(courses, gradebook)

        else:
            print("Invalid choice. Please try again.")


def _grade_distribution(courses, gradebook):
    """Display grade distribution for a course."""
    code = sanitize_input(input("\nEnter course code: ")).upper()
    course = dm.find_course(courses, code)

    if not course:
        print(f"Error: Course '{code}' not found.")
        return

    grades = gradebook.get_course_grades(code)

    if not grades:
        print(f"\nNo grades recorded for {course.title}.")
        return

    # Count occurrences of each grade
    distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for entry in grades:
        grade = entry["grade"]

        if grade in distribution:
            distribution[grade] += 1

    print(
        f"\nGrade Distribution for {course.course_code} — {course.title}:"
    )

    headers = ["Grade", "Count", "Percentage"]
    total = len(grades)
    rows = []

    for grade in ["A", "B", "C", "D", "F"]:
        count = distribution[grade]
        pct = (count / total * 100) if total > 0 else 0
        rows.append([grade, count, f"{pct:.1f}%"])

    print(format_table(headers, rows))
    print(f"  Total graded: {total}")


# ======================================================================
# Main Menu & Entry Point
# ======================================================================

def main_menu():
    """Run the main application loop.

    Loads data from CSV files, presents the main menu, and saves
    data on exit.
    """
    # Load all data
    print("Loading data...")

    students = dm.load_students()
    courses = dm.load_courses()
    instructors = dm.load_instructors()
    gradebook = dm.load_grades()

    print(
        f"Loaded: {len(students)} students, {len(courses)} courses, "
        f"{len(instructors)} instructors, "
        f"{len(gradebook.entries)} grades."
    )

    while True:
        print_header("UniDept Management System")
        print("  1. Student Management")
        print("  2. Course Management")
        print("  3. Instructor Management")
        print("  4. Grade Management")
        print("  5. Reports")
        print("  6. Save & Exit")
        print()

        choice = get_choice()

        if choice == "1":
            student_menu(students, courses)

        elif choice == "2":
            course_menu(courses, instructors)

        elif choice == "3":
            instructor_menu(instructors, courses)

        elif choice == "4":
            grade_menu(students, courses, gradebook)

        elif choice == "5":
            reports_menu(students, courses, instructors, gradebook)

        elif choice == "6":
            print("\nSaving data...")

            try:
                dm.save_all(students, courses, instructors, gradebook)
                print("All data saved successfully.")

            except Exception as exc:
                print(f"Error saving data: {exc}")
            print("Goodbye!")

            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
