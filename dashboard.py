from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)

from session_manager import WindowManager


class DashboardWindow(QMainWindow):
    """Dashboard window - Cửa sổ chính tạm thời của ứng dụng Seminary Management System"""

    def __init__(self, user_email: str, parent=None):
        super().__init__(parent)
        self.user_email = user_email
        self.setup_ui()

    def setup_ui(self):
        """Thiết lập giao diện dashboard"""
        self.setWindowTitle("Seminary Management System - Dashboard")
        self.setGeometry(200, 200, 800, 600)
        
        # Setup window icon
        self.setup_window_icon()

        # Widget chính
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Welcome message
        welcome_label = QLabel(f"Chào mừng, {self.user_email}!")
        welcome_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1F41BB;
                margin: 20px;
                qproperty-alignment: AlignCenter;
            }
        """)

        # Status message
        status_label = QLabel("Cửa sổ chính đang được phát triển...")
        status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #666;
                margin: 10px;
                qproperty-alignment: AlignCenter;
            }
        """)

        # Logout button
        logout_button = QPushButton("Đăng xuất")
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #1F41BB;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                max-width: 150px;
            }
            QPushButton:hover {
                background-color: #1a3aa3;
            }
        """)
        logout_button.clicked.connect(self.handle_logout)

        # Add widgets to layout
        layout.addWidget(welcome_label)
        layout.addWidget(status_label)
        layout.addStretch()
        layout.addWidget(logout_button, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setCentralWidget(central_widget)
    
    def setup_window_icon(self):
        """Setup window icon using logo.ico"""
        WindowManager.setup_window_icon(self)

    def handle_logout(self):
        """Xử lý đăng xuất"""
        WindowManager.handle_logout(self)
