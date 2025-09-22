from PySide6.QtWidgets import QMainWindow, QMessageBox

from session_manager import WindowManager
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
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.statusbar.showMessage("Students - Quản lý sinh viên")

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
