from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QAbstractItemView,
)

from session_manager import WindowManager
from student import student_manager

from ui_app import Ui_AppWindow


class AppWindow(QMainWindow):
    def __init__(self, user_email: str, parent=None):
        super().__init__(parent)
        self.user_email = user_email
        self.ui = Ui_AppWindow()
        self.ui.setupUi(self)
        self.setup_ui()

    def setup_ui(self):
        """Thiết lập giao diện app"""
        # Setup window icon
        self.setup_window_icon()

        # Update welcome message with user email
        self.ui.welcomeLabel.setText(f"Chào mừng, {self.user_email}")

        # Connect signals
        self.ui.logoutButton.clicked.connect(self.handle_logout)
        self.ui.actionLogout.triggered.connect(self.handle_logout)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.show_about)

        # Connect tab switching menu actions
        self.ui.actionDashboard.triggered.connect(self.switch_to_dashboard)
        self.ui.actionStudents.triggered.connect(self.switch_to_students)
        self.ui.actionCourses.triggered.connect(self.switch_to_courses)
        self.ui.actionAttendance.triggered.connect(self.switch_to_attendance)
        self.ui.actionReports.triggered.connect(self.switch_to_reports)

        # Connect student management signals
        self.ui.addStudentButton.clicked.connect(self.add_student)
        self.ui.studentSearchEdit.textChanged.connect(self.search_students)

        # Setup students table
        self.setup_students_table()
        self.load_students_data()

        # Connect student manager signals
        student_manager.students_changed.connect(self.load_students_data)

        # Set status bar message
        self.ui.statusbar.showMessage("Sẵn sàng - Seminary Management System")

    def setup_window_icon(self):
        """Setup window icon using logo.ico"""
        WindowManager.setup_window_icon(self)

    def handle_logout(self):
        """Handle logout"""
        WindowManager.handle_logout(self)

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "Về Seminary Management System",
            "Seminary Management System v0.1.0\n\n"
            "Hệ thống quản lý Chủng viện\n"
            "Phát triển bằng PySide6 (Qt for Python)\n\n"
            "© 2025 Seminary Management Team",
        )

    # Tab switching methods
    def switch_to_dashboard(self):
        """Switch to Dashboard tab"""
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.statusbar.showMessage("Dashboard - Tổng quan hệ thống")

    def switch_to_students(self):
        """Switch to Students tab"""
        self.ui.tabWidget.setCurrentIndex(0)  # Student tab is index 0
        self.ui.statusbar.showMessage("Students - Quản lý sinh viên")
        self.refresh_students()

    def switch_to_courses(self):
        """Switch to Courses tab"""
        self.ui.tabWidget.setCurrentIndex(2)
        self.ui.statusbar.showMessage("Courses - Quản lý khóa học")

    def switch_to_attendance(self):
        """Switch to Attendance tab"""
        self.ui.tabWidget.setCurrentIndex(3)
        self.ui.statusbar.showMessage("Attendance - Quản lý điểm danh")

    def switch_to_reports(self):
        """Switch to Reports tab"""
        self.ui.tabWidget.setCurrentIndex(4)
        self.ui.statusbar.showMessage("Reports - Báo cáo và thống kê")

    # Student Management Methods
    def setup_students_table(self):
        """Setup students table widget"""
        table = self.ui.studentTableWidget

        # Set column widths
        table.setColumnWidth(0, 80)  # ID
        table.setColumnWidth(1, 200)  # Tên
        table.setColumnWidth(2, 120)  # Ngày Sinh
        table.setColumnWidth(3, 150)  # Quê Quán
        table.setColumnWidth(4, 200)  # Giao Xứ
        table.setColumnWidth(5, 150)  # Giáo Phận
        table.setColumnWidth(6, 150)  # Thao tác

        # Set table properties
        table.setSortingEnabled(True)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)

    def load_students_data(self):
        """Load students data into table"""
        try:
            students = student_manager.get_all_students()
            table = self.ui.studentTableWidget

            # Clear existing data
            table.setRowCount(0)

            # Add students to table
            for row, student in enumerate(students):
                table.insertRow(row)

                # Add data to columns
                table.setItem(row, 0, QTableWidgetItem(student.id))
                table.setItem(row, 1, QTableWidgetItem(student.name))
                table.setItem(row, 2, QTableWidgetItem(student.birth_date))
                table.setItem(row, 3, QTableWidgetItem(student.hometown))
                table.setItem(row, 4, QTableWidgetItem(student.parish))
                table.setItem(row, 5, QTableWidgetItem(student.diocese))

                # Add action buttons
                self.add_action_buttons(row, student.id)

            # Update status
            total_students = len(students)
            self.ui.statusbar.showMessage(f"Đã tải {total_students} sinh viên")

        except Exception as e:
            QMessageBox.critical(
                self, "Lỗi", f"Không thể tải dữ liệu sinh viên: {str(e)}"
            )

    def add_action_buttons(self, row: int, student_id: str):
        """Add action buttons (Edit/Delete) to table row"""
        # Create widget container
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)

        # Edit button
        edit_btn = QPushButton("Sửa")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        edit_btn.clicked.connect(lambda: self.edit_student(student_id))

        # Delete button
        delete_btn = QPushButton("Xóa")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_student(student_id))

        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
        layout.addStretch()

        self.ui.studentTableWidget.setCellWidget(row, 6, widget)

    def refresh_students(self):
        """Refresh students data"""
        student_manager.load_data()
        self.load_students_data()
        self.ui.studentSearchEdit.clear()
        QMessageBox.information(self, "Thành công", "Đã làm mới dữ liệu sinh viên")

    def search_students(self, query: str):
        """Search students based on query"""
        try:
            if not query.strip():
                # Show all students if search is empty
                self.load_students_data()
                return

            # Get filtered students
            filtered_students = student_manager.search_students(query)
            table = self.ui.studentTableWidget

            # Clear existing data
            table.setRowCount(0)

            # Add filtered students to table
            for row, student in enumerate(filtered_students):
                table.insertRow(row)

                table.setItem(row, 0, QTableWidgetItem(student.id))
                table.setItem(row, 1, QTableWidgetItem(student.name))
                table.setItem(row, 2, QTableWidgetItem(student.birth_date))
                table.setItem(row, 3, QTableWidgetItem(student.hometown))
                table.setItem(row, 4, QTableWidgetItem(student.parish))
                table.setItem(row, 5, QTableWidgetItem(student.diocese))

                self.add_action_buttons(row, student.id)

            # Update status
            self.ui.statusbar.showMessage(
                f"Tìm thấy {len(filtered_students)} sinh viên"
            )

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tìm kiếm: {str(e)}")

    def add_student(self):
        """Add new student"""
        try:
            # For now, show a simple input dialog
            # TODO: Create a proper add student dialog
            QMessageBox.information(
                self,
                "Thêm Sinh Viên",
                "Tính năng thêm sinh viên mới sẽ được triển khai trong phiên bản tiếp theo.\n\n"
                "Hiện tại bạn có thể xem dữ liệu mẫu trong bảng.",
            )

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm sinh viên: {str(e)}")

    def edit_student(self, student_id: str):
        """Edit student"""
        try:
            student = student_manager.get_student_by_id(student_id)
            if not student:
                QMessageBox.warning(self, "Cảnh báo", "Không tìm thấy sinh viên")
                return

            # For now, show student info
            # TODO: Create a proper edit student dialog
            info = (
                f"Thông tin sinh viên:\n\n"
                f"ID: {student.id}\n"
                f"Tên: {student.name}\n"
                f"Ngày sinh: {student.birth_date}\n"
                f"Tuổi: {student.get_age()}\n"
                f"Quê quán: {student.hometown}\n"
                f"Giao xứ: {student.parish}\n"
                f"Giáo phận: {student.diocese}"
            )

            QMessageBox.information(self, "Thông tin Sinh Viên", info)

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi chỉnh sửa sinh viên: {str(e)}")

    def delete_student(self, student_id: str):
        """Delete student"""
        try:
            student = student_manager.get_student_by_id(student_id)
            if not student:
                QMessageBox.warning(self, "Cảnh báo", "Không tìm thấy sinh viên")
                return

            # Confirm deletion
            reply = QMessageBox.question(
                self,
                "Xác nhận xóa",
                f"Bạn có chắc chắn muốn xóa sinh viên '{student.name}' (ID: {student.id})?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                if student_manager.delete_student(student_id):
                    QMessageBox.information(
                        self, "Thành công", "Đã xóa sinh viên thành công"
                    )
                    self.load_students_data()
                else:
                    QMessageBox.critical(self, "Lỗi", "Không thể xóa sinh viên")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa sinh viên: {str(e)}")
