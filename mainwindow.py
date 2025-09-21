# This Python file uses the following encoding: utf-8
import sys
import os
import re
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt, QTimer

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Setup circular logo
        self.setup_circular_logo()
        
        # Setup validation
        self.setup_validation()
        
        # Kết nối signals
        self.ui.submitButton.clicked.connect(self.handle_login)
        self.ui.forgotPasswordLink.mousePressEvent = self.handle_forgot_password
        
        # Enable Enter key để submit
        self.ui.passwordInput.returnPressed.connect(self.handle_login)
        self.ui.emailInput.returnPressed.connect(self.handle_login)
    
    def setup_circular_logo(self):
        """Create a circular logo from the logo image"""
        if hasattr(self.ui, 'logoLabel'):
            # Load the logo image
            logo_path = os.path.join(os.path.dirname(__file__), "images", "logo.png")
            
            if os.path.exists(logo_path):
                # Load and scale the original image
                original_pixmap = QPixmap(logo_path)
                size = 120  # Size of the circular logo (increased from 90)
                
                # Create a circular mask
                circular_pixmap = QPixmap(size, size)
                circular_pixmap.fill(Qt.transparent)
                
                painter = QPainter(circular_pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                
                # Create circular path
                path = QPainterPath()
                path.addEllipse(0, 0, size, size)
                painter.setClipPath(path)
                
                # Scale and draw the original image
                scaled_pixmap = original_pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                x = (size - scaled_pixmap.width()) // 2
                y = (size - scaled_pixmap.height()) // 2
                painter.drawPixmap(x, y, scaled_pixmap)
                painter.end()
                
                # Set the circular logo
                self.ui.logoLabel.setPixmap(circular_pixmap)
                self.ui.logoLabel.setAlignment(Qt.AlignCenter)
    
    def setup_validation(self):
        # Email validation pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        self.email_regex = re.compile(email_pattern)
    
    def validate_email(self, email: str) -> bool:
        return bool(self.email_regex.match(email))
    
    def handle_login(self):
        # Disable button để tránh double-click
        self.ui.submitButton.setEnabled(False)
        self.ui.submitButton.setText("Đang đăng nhập...")
        
        try:
            # Lấy và validate input
            email = self.ui.emailInput.text().strip()
            password = self.ui.passwordInput.text().strip()
            
            # Validation
            if not email:
                self.show_error("Vui lòng nhập email!")
                return
                
            if not self.validate_email(email):
                self.show_error("Email không hợp lệ!")
                return
                
            if not password:
                self.show_error("Vui lòng nhập password!")
                return
                
            if len(password) < 6:
                self.show_error("Password phải có ít nhất 6 ký tự!")
                return
            
            # Thực hiện authentication
            if self.authenticate_user(email, password):
                self.show_success("Đăng nhập thành công!")
                QTimer.singleShot(1000, self.accept_login)  # Delay 1s trước khi chuyển
            else:
                self.show_error("Email hoặc password không đúng!")
                self.ui.passwordInput.clear()
                self.ui.passwordInput.setFocus()
                
        except Exception as e:
            self.show_error(f"Có lỗi xảy ra: {str(e)}")
        finally:
            # Re-enable button
            self.ui.submitButton.setEnabled(True)
            self.ui.submitButton.setText("Sign in")
    
    def authenticate_user(self, email: str, password: str) -> bool:
        # TODO: Thay thế bằng logic authentication thực tế
        # Ví dụ: database query, API call, etc.
        
        # Demo data
        valid_users = {
            "admin@seminary.edu": "admin123",
            "user@seminary.edu": "user123"
        }
        
        return valid_users.get(email) == password
    
    def show_error(self, message: str):
        QMessageBox.warning(self, "Lỗi", message)
    
    def show_success(self, message: str):
        QMessageBox.information(self, "Thành công", message)
    
    def handle_forgot_password(self, event):
        # Xử lý click vào "Forgot your password?"
        QMessageBox.information(self, "Quên mật khẩu", 
                               "Tính năng khôi phục mật khẩu sẽ được triển khai sau!")
    
    def accept_login(self):
        # Logic sau khi đăng nhập thành công
        # user_email = self.ui.emailInput.text()
        
        # TODO: Mở cửa sổ chính của ứng dụng
        # TODO: Lưu thông tin session
        # TODO: Đóng cửa sổ login
        
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
