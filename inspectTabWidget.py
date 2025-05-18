from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QPushButton, QVBoxLayout
from PyQt5 import uic
import sys

class OrnekSayfa(QWidget):
    def __init__(self, isim):
        super().__init__()
        self.setObjectName(isim)  # sekmeleri tanımak için objectName önemli
        layout = QVBoxLayout()
        layout.addWidget(QPushButton(f"{isim} içeriği"))
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.tabWidget: QTabWidget = self.findChild(QTabWidget, "tabWidget")
        self.btn1: QPushButton = self.findChild(QPushButton, "btn1")  # örnek icon butonu
        self.btn2: QPushButton = self.findChild(QPushButton, "btn2")

        self.btn1.clicked.connect(lambda: self.tabAc("Sayfa1"))
        self.btn2.clicked.connect(lambda: self.tabAc("Sayfa2"))

    def tabAc(self, isim):
        # Daha önce açılmış mı kontrol et
        for i in range(self.tabWidget.count()):
            if self.tabWidget.widget(i).objectName() == isim:
                self.tabWidget.setCurrentIndex(i)
                return

        # Yoksa yeni sekme olarak ekle
        yeniSayfa = OrnekSayfa(isim)
        self.tabWidget.addTab(yeniSayfa, isim)
        self.tabWidget.setCurrentWidget(yeniSayfa)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
