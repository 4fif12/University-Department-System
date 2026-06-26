# UniDept — University Department Management System

A Python command-line application for managing students, courses, instructors, and grades within a university department.

## Purpose

UniDept provides a simple, menu-driven interface for department administrators to:

- Register and manage student records
- Create and configure courses with capacity limits
- Assign instructors to courses
- Record and update student grades
- Generate reports including transcripts, rosters, and grade distributions

## Installation and Execution

### Requirements

- **Python 3.8 or higher** (no external packages required)

### Running the Program

1. Clone or download this repository:

   ```bash
   git clone https://github.com/4fif12/UniDept.git
   cd UniDept
   ```

2. Run the program:
   ```bash
   python main.py
   ```

The system will load sample data from the `data/` directory and present the main menu.

## Example Usage

### Adding a New Student

```
+==============================================+
|        Student Management                    |
+==============================================+
  1. Add New Student
  2. View All Students
  ...
  0. Back to Main Menu

Enter your choice: 1

--- Add New Student ---
Enter student name: John Brown
Enter student email: john.brown@university.edu
Student added successfully: [ID: 6] John Brown (john.brown@university.edu) — Courses: None
```

### Viewing a Student Transcript

```
Enter student ID: 1

Transcript for Alice Johnson (ID: 1):
+--------+-------+--------+
| Course | Grade | Points |
+--------+-------+--------+
| CS101  | A     | 4.0    |
| MA201  | B     | 3.0    |
+--------+-------+--------+
  GPA: 3.50
```

### Viewing Grade Distribution

```
Enter course code: CS101

Grade Distribution for CS101 — Introduction to Computer Science:
+-------+-------+------------+
| Grade | Count | Percentage |
+-------+-------+------------+
| A     | 1     | 33.3%      |
| B     | 1     | 33.3%      |
| C     | 1     | 33.3%      |
| D     | 0     | 0.0%       |
| F     | 0     | 0.0%       |
+-------+-------+------------+
  Total graded: 3
```

## Key Features

- **Student Management** — Add, search, view, enrol, drop, and remove students
- **Course Management** — Add, search, view courses; assign instructors; view rosters
- **Instructor Management** — Add, search, view, and remove instructors
- **Grade Management** — Record and update letter grades (A–F) with GPA calculation
- **Reports** — Student transcripts, course grade distributions, summaries
- **Data Persistence** — All data saved to CSV files with crash-safe atomic writes
- **Input Validation** — Email format checking, grade validation, duplicate detection
- **Exception Handling** — Custom exceptions with user-friendly error messages

## Files

| File                   | Description                                             |
| ---------------------- | ------------------------------------------------------- |
| `main.py`              | Entry point with interactive menu-driven CLI            |
| `student.py`           | Student class — manages student records                 |
| `course.py`            | Course class — manages course details and enrolment     |
| `instructor.py`        | Instructor class — manages faculty records              |
| `gradebook.py`         | GradeBook class — manages grade entries and GPA         |
| `data_manager.py`      | CSV file I/O, transactional operations, ID generation   |
| `utils.py`             | Custom exceptions, validation helpers, table formatting |
| `data/students.csv`    | Student records                                         |
| `data/courses.csv`     | Course records                                          |
| `data/instructors.csv` | Instructor records                                      |
| `data/grades.csv`      | Grade records                                           |
| `report.md`            | Written project report                                  |

## Known Limitations

- **In-memory model**: All data is loaded into memory at startup. Not suitable for very large datasets.
- **Single-user**: No authentication or access control. Designed for a single administrator.
- **No external dependencies**: Uses only Python standard library modules.




