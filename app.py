from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTabWidget,
    QMessageBox,
)

from session_manager import WindowManager


class AppWindow(QMainWindow):
    def __init__(self, user_email: str, parent=None):
        super().__init__(parent)
        self.user_email = user_email
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Seminary Management System - Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        
        # Setup window icon
        self.setup_window_icon()

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)

        # Header
        header_layout = QHBoxLayout()
        welcome_label = QLabel(f"Chào mừng, {self.user_email}")
        welcome_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1F41BB;
                padding: 10px;
            }
        """)

        logout_button = QPushButton("Đăng xuất")
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        logout_button.clicked.connect(self.handle_logout)

        header_layout.addWidget(welcome_label)
        header_layout.addStretch()
        header_layout.addWidget(logout_button)

        # Tab widget for different modules
        tab_widget = QTabWidget()
        tab_widget.addTab(QLabel("Dashboard Content"), "Dashboard")
        tab_widget.addTab(QLabel("Student Management"), "Students")
        tab_widget.addTab(QLabel("Course Management"), "Courses")
        tab_widget.addTab(QLabel("Attendance"), "Attendance")
        tab_widget.addTab(QLabel("Reports"), "Reports")

        layout.addLayout(header_layout)
        layout.addWidget(tab_widget)

        # Status bar
        self.statusBar().showMessage("Ready")
    
    def setup_window_icon(self):
        """Setup window icon using logo.ico"""
        WindowManager.setup_window_icon(self)

    def handle_logout(self):
        """Handle logout"""
        WindowManager.handle_logout(self)

    def show_about(self):
        QMessageBox.about(
            self,
            "About",
            "Seminary Management System v0.1.0\n\nBuilt with PySide6 (Qt for Python)",
        )
