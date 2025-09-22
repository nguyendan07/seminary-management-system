"""
Student Management Module
Handles student data operations for Seminary Management System
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from PySide6.QtCore import QObject, Signal


class Student(BaseModel):
    """Student data model using Pydantic"""

    model_config = ConfigDict(
        # Allow field validation on assignment
        validate_assignment=True,
        # Use enum values instead of enum objects
        use_enum_values=True,
        # Validate default values
        validate_default=True,
        # Extra attributes are forbidden
        extra="forbid",
    )

    id: str = Field(..., min_length=1, max_length=10, description="Student ID")
    name: str = Field(
        ..., min_length=1, max_length=100, description="Student full name"
    )
    birth_date: str = Field(..., description="Birth date in DD/MM/YYYY format")
    hometown: str = Field(
        ..., min_length=1, max_length=100, description="Student hometown"
    )
    parish: str = Field(..., min_length=1, max_length=100, description="Student parish")
    diocese: str = Field(
        ..., min_length=1, max_length=100, description="Student diocese"
    )

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v):
        """Validate birth date format"""
        try:
            datetime.strptime(v, "%d/%m/%Y")
            return v
        except ValueError:
            raise ValueError("Birth date must be in DD/MM/YYYY format")

    @field_validator("id")
    @classmethod
    def validate_student_id(cls, v):
        """Validate student ID format"""
        if not v.startswith("SV"):
            raise ValueError("Student ID must start with 'SV'")
        if len(v) < 3:
            raise ValueError("Student ID must have at least 3 characters")
        return v.upper()

    def to_dict(self) -> Dict[str, Any]:
        """Convert student to dictionary"""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """Create student from dictionary"""
        return cls.model_validate(data)

    def get_age(self) -> int:
        """Calculate age from birth date"""
        try:
            birth_date = datetime.strptime(self.birth_date, "%d/%m/%Y")
            today = datetime.now()
            age = today.year - birth_date.year
            if today.month < birth_date.month or (
                today.month == birth_date.month and today.day < birth_date.day
            ):
                age -= 1
            return age
        except (ValueError, TypeError):
            return 0


class StudentManager(QObject):
    """Manages student operations - CRUD, search, data persistence"""

    # Signals for UI updates
    students_changed = Signal()
    student_added = Signal(str)  # student_id
    student_updated = Signal(str)  # student_id
    student_deleted = Signal(str)  # student_id

    DATA_FILE = "students_data.json"

    def __init__(self):
        super().__init__()
        self.students: List[Student] = []
        self.load_data()

    def get_data_file_path(self) -> str:
        """Get the full path to the data file"""
        return os.path.join(os.path.dirname(__file__), self.DATA_FILE)

    def load_data(self) -> bool:
        """Load students data from JSON file"""
        try:
            data_file = self.get_data_file_path()

            if not os.path.exists(data_file):
                # Create sample data if file doesn't exist
                self.create_sample_data()
                return True

            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.students = [
                Student.from_dict(student_data)
                for student_data in data.get("students", [])
            ]
            print(f"Loaded {len(self.students)} students from file")
            return True

        except Exception as e:
            print(f"Error loading students data: {e}")
            # Create sample data as fallback
            self.create_sample_data()
            return False

    def save_data(self) -> bool:
        """Save students data to JSON file"""
        try:
            data_file = self.get_data_file_path()

            data = {
                "students": [student.to_dict() for student in self.students],
                "last_updated": datetime.now().isoformat(),
                "total_count": len(self.students),
            }

            with open(data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"Saved {len(self.students)} students to file")
            return True

        except Exception as e:
            print(f"Error saving students data: {e}")
            return False

    def create_sample_data(self) -> None:
        """Create sample student data"""
        sample_students = [
            Student(
                id="SV001",
                name="Nguyễn Văn An",
                birth_date="15/03/1995",
                hometown="Hà Nội",
                parish="Gx Thánh Giuse",
                diocese="Gp Hà Nội",
            ),
            Student(
                id="SV002",
                name="Trần Thành Bình",
                birth_date="22/07/1996",
                hometown="TP.HCM",
                parish="Gx Đức Bà",
                diocese="Gp TP.HCM",
            ),
            Student(
                id="SV003",
                name="Lê Minh Cường",
                birth_date="08/11/1994",
                hometown="Đà Nẵng",
                parish="Gx Chính Tòa",
                diocese="Gp Đà Nẵng",
            ),
            Student(
                id="SV004",
                name="Phạm Quang Dũng",
                birth_date="03/12/1997",
                hometown="Hải Phòng",
                parish="Gx Thánh Tâm",
                diocese="Gp Hải Phòng",
            ),
            Student(
                id="SV005",
                name="Hoàng Văn Em",
                birth_date="28/05/1995",
                hometown="Huế",
                parish="Gx Phú Cam",
                diocese="Gp Huế",
            ),
            Student(
                id="SV006",
                name="Vũ Thành Phúc",
                birth_date="14/09/1996",
                hometown="Nam Định",
                parish="Gx Thánh Phêrô",
                diocese="Gp Bùi Chu",
            ),
            Student(
                id="SV007",
                name="Đặng Minh Quang",
                birth_date="07/01/1998",
                hometown="Nghệ An",
                parish="Gx Kim Liên",
                diocese="Gp Vinh",
            ),
            Student(
                id="SV008",
                name="Bùi Văn Hùng",
                birth_date="19/04/1995",
                hometown="Thái Bình",
                parish="Gx Kẻ Sặt",
                diocese="Gp Hải Phòng",
            ),
            Student(
                id="SV009",
                name="Đinh Công Minh",
                birth_date="26/10/1997",
                hometown="Quảng Ninh",
                parish="Gx Cửa Ông",
                diocese="Gp Hà Nội",
            ),
            Student(
                id="SV010",
                name="Ngô Thành Nam",
                birth_date="12/06/1996",
                hometown="Cần Thơ",
                parish="Gx Chính Tòa",
                diocese="Gp Cần Thơ",
            ),
        ]

        self.students = sample_students
        self.save_data()
        print(f"Created {len(sample_students)} sample students")

    # CRUD Operations
    def get_all_students(self) -> List[Student]:
        """Get all students"""
        return self.students.copy()

    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        """Get student by ID"""
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def add_student(self, student: Student) -> bool:
        """Add new student"""
        try:
            # Check if ID already exists
            if self.get_student_by_id(student.id):
                print(f"Student with ID {student.id} already exists")
                return False

            self.students.append(student)
            self.save_data()
            self.student_added.emit(student.id)
            self.students_changed.emit()
            print(f"Added student: {student.name}")
            return True

        except Exception as e:
            print(f"Error adding student: {e}")
            return False

    def update_student(self, student_id: str, updated_student: Student) -> bool:
        """Update existing student"""
        try:
            for i, student in enumerate(self.students):
                if student.id == student_id:
                    self.students[i] = updated_student
                    self.save_data()
                    self.student_updated.emit(student_id)
                    self.students_changed.emit()
                    print(f"Updated student: {updated_student.name}")
                    return True

            print(f"Student with ID {student_id} not found")
            return False

        except Exception as e:
            print(f"Error updating student: {e}")
            return False

    def delete_student(self, student_id: str) -> bool:
        """Delete student by ID"""
        try:
            for i, student in enumerate(self.students):
                if student.id == student_id:
                    deleted_student = self.students.pop(i)
                    self.save_data()
                    self.student_deleted.emit(student_id)
                    self.students_changed.emit()
                    print(f"Deleted student: {deleted_student.name}")
                    return True

            print(f"Student with ID {student_id} not found")
            return False

        except Exception as e:
            print(f"Error deleting student: {e}")
            return False

    # Search and Filter Operations
    def search_students(self, query: str) -> List[Student]:
        """Search students by name, ID, hometown, parish, or diocese"""
        if not query.strip():
            return self.get_all_students()

        query = query.lower().strip()
        results = []

        for student in self.students:
            if (
                query in student.id.lower()
                or query in student.name.lower()
                or query in student.hometown.lower()
                or query in student.parish.lower()
                or query in student.diocese.lower()
            ):
                results.append(student)

        return results

    def filter_by_diocese(self, diocese: str) -> List[Student]:
        """Filter students by diocese"""
        return [
            student
            for student in self.students
            if student.diocese.lower() == diocese.lower()
        ]

    def filter_by_parish(self, parish: str) -> List[Student]:
        """Filter students by parish"""
        return [
            student
            for student in self.students
            if student.parish.lower() == parish.lower()
        ]

    def filter_by_hometown(self, hometown: str) -> List[Student]:
        """Filter students by hometown"""
        return [
            student
            for student in self.students
            if student.hometown.lower() == hometown.lower()
        ]

    # Statistics and Utility Methods
    def get_total_count(self) -> int:
        """Get total number of students"""
        return len(self.students)

    def get_statistics(self) -> Dict[str, Any]:
        """Get student statistics"""
        total = len(self.students)

        # Count by diocese
        diocese_count = {}
        parish_count = {}
        hometown_count = {}

        for student in self.students:
            diocese_count[student.diocese] = diocese_count.get(student.diocese, 0) + 1
            parish_count[student.parish] = parish_count.get(student.parish, 0) + 1
            hometown_count[student.hometown] = (
                hometown_count.get(student.hometown, 0) + 1
            )

        return {
            "total_students": total,
            "diocese_distribution": diocese_count,
            "parish_distribution": parish_count,
            "hometown_distribution": hometown_count,
            "unique_dioceses": len(diocese_count),
            "unique_parishes": len(parish_count),
            "unique_hometowns": len(hometown_count),
        }

    def generate_next_id(self) -> str:
        """Generate next student ID"""
        if not self.students:
            return "SV001"

        # Find the highest ID number
        max_num = 0
        for student in self.students:
            if student.id.startswith("SV"):
                try:
                    num = int(student.id[2:])
                    max_num = max(max_num, num)
                except (ValueError, IndexError):
                    continue

        return f"SV{(max_num + 1):03d}"

    def export_to_csv(self, file_path: str) -> bool:
        """Export students data to CSV file"""
        try:
            import csv

            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = [
                    "ID",
                    "Tên",
                    "Ngày Sinh",
                    "Tuổi",
                    "Quê Quán",
                    "Giao Xứ",
                    "Giáo Phận",
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for student in self.students:
                    writer.writerow(
                        {
                            "ID": student.id,
                            "Tên": student.name,
                            "Ngày Sinh": student.birth_date,
                            "Tuổi": student.get_age(),
                            "Quê Quán": student.hometown,
                            "Giao Xứ": student.parish,
                            "Giáo Phận": student.diocese,
                        }
                    )

            print(f"Exported {len(self.students)} students to {file_path}")
            return True

        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False


# Global instance for easy access
student_manager = StudentManager()
