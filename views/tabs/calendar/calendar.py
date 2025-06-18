from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QCalendarWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPropertyAnimation

class Calendar(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        uic.loadUi("ui/templates/tabs/calendar/calendar.ui", self)
        
        # Takvim widget'ını bul
        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")  # Qt Designer'daki objectName
        
        # Opacity Effect
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(1)
        self.setGraphicsEffect(self.opacity_effect)
        
        # Animasyon
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        
        # Pencere Ayarları
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(242, 246, 252, 255);
                border-radius: 15px;
                border: 1px solid #ccc;
            }
        """)
        
        # Controller ile iletişim
        self.controller = controller
        if self.controller and self.calendar:
            self.calendar.selectionChanged.connect(self.send_date_to_controller)

    def send_date_to_controller(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.controller.handle_date_selection(selected_date)

    def mousePressEvent(self, event):
        if not self.geometry().contains(event.globalPos()):
            self.close()