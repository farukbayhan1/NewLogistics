from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QFileDialog, QProgressDialog
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QMessageBox
import pandas as pd





class AddEmployeeTab(QWidget):
    def __init__(self,username,user_role):
        super().__init__()
        uic.loadUi("ui/templates/tabs/employee/addemployee.ui", self)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.username = username
        self.user_role = user_role
    
    def show_progress_dialog(self, message="İşlem Yapılıyor..."):
        self.progress_dialog = QProgressDialog(message, None, 0, 0, self.tab)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)
        self.progress_dialog.setCancelButton(None)
        self.progress_dialog.show()
    
    def hide_progress_dialog(self):
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.close()
            del self.progress_dialog
        
        
   

        
        




