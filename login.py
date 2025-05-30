from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5 import uic
from PyQt5.QtCore import Qt

from ui.icons.background import login_resources
from controllers.logincontroller import LoginController


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/templates/login.ui",self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.logincontroller = LoginController(self)
        



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())