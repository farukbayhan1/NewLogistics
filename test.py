from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,QGraphicsOpacityEffect
from PyQt5 import uic
from PyQt5.QtCore import Qt, QPropertyAnimation
from ui.icons.buttons import buttons_resources



class OrderDropDown(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/templates/orderdropdown.ui", self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setStyleSheet("background: transparent;")
        self.setGraphicsEffect(None) # Shadow Effect
        self.opacity_effect = QGraphicsOpacityEffect(self) #Opacity Effect
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)

class EmployeeDropDown(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/templates/employeedropdown.ui", self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setStyleSheet("background: transparent;")
        self.setGraphicsEffect(None) # Shadow Effect
        self.opacity_effect = QGraphicsOpacityEffect(self) #Opacity Effect
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)

class VehicleAndTrip(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/templates/vehicleandtripdropdown.ui", self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setStyleSheet("background: transparent;")
        self.setGraphicsEffect(None) # Shadow Effect
        self.opacity_effect = QGraphicsOpacityEffect(self) #Opacity Effect
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)

class Personel(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/templates/personeldropdown.ui", self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setStyleSheet("background: transparent;")
        self.setGraphicsEffect(None) # Shadow Effect
        self.opacity_effect = QGraphicsOpacityEffect(self) #Opacity Effect
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)

class Report(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/templates/reportdropdown.ui", self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setStyleSheet("background: transparent;")
        self.setGraphicsEffect(None) # Shadow Effect
        self.opacity_effect = QGraphicsOpacityEffect(self) #Opacity Effect
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/templates/main.ui", self)
        # Icon Only Widget Buttons
        self.dropdownorder = OrderDropDown()
        self.dropdownemployee = EmployeeDropDown()
        self.dropdownvehicleandtrip = VehicleAndTrip()
        self.dropdownpersonel = Personel()
        self.dropdownreport = Report()
        
        #Buttons Connect
        self.pushButtonEmployee.clicked.connect(lambda: self.show_dropdown(self.pushButtonEmployee, self.dropdownemployee))
        self.pushButtonOrder.clicked.connect(lambda: self.show_dropdown(self.pushButtonOrder, self.dropdownorder))
        self.pushButtonTruck.clicked.connect(lambda: self.show_dropdown(self.pushButtonTruck, self.dropdownvehicleandtrip))
        self.pushButtonCourier.clicked.connect(lambda: self.show_dropdown(self.pushButtonCourier, self.dropdownpersonel))
        self.pushButtonReport.clicked.connect(lambda: self.show_dropdown(self.pushButtonReport, self.dropdownreport))

    def show_dropdown(self, button, dropdown_widget):
        pos = button.mapToGlobal(button.rect().topRight())
        self_x = pos.x() + 10  # 10px sağa kaydır
        self_y = pos.y()       # Gerekirse buraya da +5 veya -5 gibi ekleme yapabilirsin
        dropdown_widget.move(self_x, self_y)
        dropdown_widget.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
