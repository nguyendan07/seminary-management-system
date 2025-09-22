from PySide6.QtWidgets import QMainWindow, QMessageBox

from session_manager import WindowManager
from ui_dashboard import Ui_DashboardWindow


class DashboardWindow(QMainWindow):
    """Dashboard window - Cửa sổ chính tạm thời của ứng dụng Seminary Management System"""

    def __init__(self, user_email: str, parent=None):
        super().__init__(parent)
        self.user_email = user_email
        self.ui = Ui_DashboardWindow()
        self.ui.setupUi(self)
        self.setup_ui()

    def setup_ui(self):
        """Thiết lập giao diện dashboard"""
        # Setup window icon
        self.setup_window_icon()

        # Update welcome message with user email
        self.ui.welcomeLabel.setText(f"Chào mừng, {self.user_email}!")

        # Connect signals
        self.ui.logoutButton.clicked.connect(self.handle_logout)
        self.ui.actionLogout.triggered.connect(self.handle_logout)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.show_about)

        # Set status bar message
        self.ui.statusbar.showMessage("Sẵn sàng - Dashboard đang được phát triển")

    def setup_window_icon(self):
        """Setup window icon using logo.ico"""
        WindowManager.setup_window_icon(self)

    def handle_logout(self):
        """Xử lý đăng xuất"""
        WindowManager.handle_logout(self)

    def show_about(self):
        """Hiển thị thông tin về ứng dụng"""
        QMessageBox.about(
            self,
            "Về Seminary Management System",
            "Seminary Management System v0.1.0\n\n"
            "Hệ thống quản lý Chủng viện\n"
            "Phát triển bằng PySide6 (Qt for Python)\n\n"
            "© 2025 Seminary Management Team",
        )
