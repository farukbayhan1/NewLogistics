def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
        self._drag_pos = event.globalPos()

def mouseMoveEvent(self, event):
    if event.buttons() == Qt.LeftButton:
        self.move(self.pos() + event.globalPos() - self._drag_pos)
        self._drag_pos = event.globalPos()
        event.accept()



# Windows Buttons

self.btnClose.clicked.connect(self.close)
self.btnMinimize.clicked.connect(self.showMinimized)

# Buttons Styles
QPushButton#btnClose:hover {
    background-color: #e74c3c;
}
QPushButton#btnMinimize:hover {
    background-color: #f1c40f;
}
QPushButton#btnMaximize:hover {
    background-color: #2ecc71;
}


# Maximize/Restore için:
def toggle_max_restore(self):
    if self.isMaximized():
        self.showNormal()
    else:
        self.showMaximized()

self.btnMaximize.clicked.connect(self.toggle_max_restore)

#