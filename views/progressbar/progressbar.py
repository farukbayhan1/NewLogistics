from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
import sys

class LoadingDialog(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/templates/progressbar.ui", self)
        
        # Layout yoksa elle tanımla (geçici çözüm)
        if not self.layout():
            layout = QVBoxLayout(self)
            layout.addWidget(self.labelAnimation)
            # Eğer QPushButton varsa, onu da ekle: layout.addWidget(self.pushButton)

    
        #self.setFixedSize(self.size())
        self.setStyleSheet("background: transparent;")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(30, 30)
        self.setMaximumSize(170,150)
        self.movie = QMovie("ui/icons/buttons/boxes.gif")
        self.labelAnimation.setMovie(self.movie)
        self.labelAnimation.setScaledContents(True)
        self.movie.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = LoadingDialog()
    dialog.show()
    sys.exit(app.exec_())
