"""
Session Management Module
Handles user session operations for Seminary Management System
"""

import json
import os
from datetime import datetime, timedelta
from PySide6.QtCore import QStandardPaths
from PySide6.QtGui import QIcon


class SessionManager:
    """Manages user session operations - login, logout, session validation"""

    SESSION_FILE = "session.json"
    SESSION_DURATION_HOURS = 24

    @staticmethod
    def get_session_file_path():
        """Get the full path to the session file"""
        config_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, SessionManager.SESSION_FILE)

    @staticmethod
    def save_user_session(email: str):
        """Lưu thông tin session của user"""
        try:
            session_file = SessionManager.get_session_file_path()

            # Thông tin session
            session_data = {
                "user_email": email,
                "login_time": datetime.now().isoformat(),
                "expires_at": (
                    datetime.now()
                    + timedelta(hours=SessionManager.SESSION_DURATION_HOURS)
                ).isoformat(),
                "is_active": True,
            }

            # Ghi session vào file
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)

            print(f"Session saved for user: {email}")
            return True

        except Exception as e:
            print(f"Error saving session: {e}")
            return False

    @staticmethod
    def clear_user_session():
        """Xóa thông tin session"""
        try:
            session_file = SessionManager.get_session_file_path()

            if os.path.exists(session_file):
                os.remove(session_file)
                print("Session cleared")
                return True

            return True  # Session không tồn tại cũng coi như đã clear

        except Exception as e:
            print(f"Error clearing session: {e}")
            return False

    @staticmethod
    def check_existing_session():
        """Kiểm tra session hiện tại khi khởi động ứng dụng"""
        try:
            session_file = SessionManager.get_session_file_path()

            if not os.path.exists(session_file):
                return None

            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)

            # Kiểm tra session có hết hạn không
            expires_at = datetime.fromisoformat(session_data.get("expires_at", ""))
            if datetime.now() > expires_at:
                os.remove(session_file)  # Xóa session hết hạn
                return None

            if session_data.get("is_active", False):
                return session_data

        except Exception as e:
            print(f"Error checking session: {e}")

        return None

    @staticmethod
    def is_session_valid():
        """Kiểm tra session hiện tại có hợp lệ không"""
        session = SessionManager.check_existing_session()
        return session is not None

    @staticmethod
    def get_current_user():
        """Lấy thông tin user hiện tại từ session"""
        session = SessionManager.check_existing_session()
        if session:
            return session.get("user_email")
        return None


class WindowManager:
    """Manages window navigation and lifecycle"""
    
    @staticmethod
    def setup_window_icon(window):
        """Setup window icon for any window using logo.ico"""
        icon_path = os.path.join(os.path.dirname(__file__), "images", "logo.ico")
        if os.path.exists(icon_path):
            window.setWindowIcon(QIcon(icon_path))
            return True
        return False

    @staticmethod
    def show_login_window():
        """Hiển thị cửa sổ login"""
        # Import ở đây để tránh circular import
        from mainwindow import MainWindow

        login_window = MainWindow()
        login_window.show()
        login_window.ui.emailInput.clear()
        login_window.ui.passwordInput.clear()
        login_window.ui.emailInput.setFocus()
        return login_window

    @staticmethod
    def handle_logout(current_window=None):
        """Xử lý đăng xuất chung cho tất cả các window"""
        try:
            # Xóa session
            SessionManager.clear_user_session()

            # Đóng cửa sổ hiện tại nếu có
            if current_window:
                current_window.close()

            # Hiển thị cửa sổ login
            WindowManager.show_login_window()

            return True

        except Exception as e:
            print(f"Error during logout: {e}")
            return False
