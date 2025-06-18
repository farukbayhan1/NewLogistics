from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, QPropertyAnimation
from views.form.checkorder import CheckOrderForm
from services.orderservice import OrderService
from resources.dbmanager import execute_query
from resources.query.sqlitequery import GET_ALL,CHECK_BARCODE, ADD_BARCODE,COUNT_BARCODE,DELETE_BARCODES


class UpdateOrderTab(QWidget):
    def __init__(self,username,user_role):
        super().__init__()
        uic.loadUi("ui/templates/tabs/order/updateorder.ui", self)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.order_service = OrderService()
        self.check_form = CheckOrderForm()
        self.username = username
        self.user_role = user_role
        self.connect_signal()
        self.count_barcode()
        self.load_barcode()
        self.check_form.lineEditSearch.textChanged.connect(self.search_barcode)

    def connect_signal(self):
        self.pushButtonDocumentCheck.clicked.connect(self.open_check_form)
        self.check_form.pushButtonSend.clicked.connect(self.sent_data)
        self.check_form.lineEditReadBarcode.returnPressed.connect(self.insert_barcode)
     
    def open_check_form(self):
        self.check_form.show()
        self.check_form.animation.start()

    def insert_barcode(self):
        barcode = self.check_form.lineEditReadBarcode.text().strip()
        result = execute_query(CHECK_BARCODE,(barcode,),fetchone=True)
        if result:
            return QMessageBox.information(self.check_form,"Bilgi","Barkod Daha Önce Okutulmuş")
        else:
            execute_query(ADD_BARCODE,(barcode,),commit=True)
            self.check_form.lineEditReadBarcode.clear()
            self.count_barcode()
            self.load_barcode()
    
    def count_barcode(self):
        get_barcode_count = execute_query(COUNT_BARCODE,fetchone=True)
        count = get_barcode_count[0]
        self.check_form.labelCount.setText(str(count))

    def load_barcode(self):
        self.check_form.tableWidgetReadedOrder.setColumnCount(3)
        self.check_form.tableWidgetReadedOrder.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.check_form.tableWidgetReadedOrder.setHorizontalHeaderLabels([
            "İrsaliye Numarası",
            "Kontrol Tarihi",
            "Kontrol Durumu"
        ])
        rows = execute_query(GET_ALL,fetchall=True)
        self.check_form.tableWidgetReadedOrder.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            self.check_form.tableWidgetReadedOrder.setItem(row_index, 0, QTableWidgetItem(str(row[0])))
            self.check_form.tableWidgetReadedOrder.setItem(row_index, 1, QTableWidgetItem(str(row[1])))
            self.check_form.tableWidgetReadedOrder.setItem(row_index, 2, QTableWidgetItem(str(row[2])))
    
    def search_barcode(self):
        search_text = self.check_form.lineEditSearch.text().strip()
        for row in range(self.check_form.tableWidgetReadedOrder.rowCount()):
            item = self.check_form.tableWidgetReadedOrder.item(row,0)
            if item:
                item_text = item.text()
                self.check_form.tableWidgetReadedOrder.setRowHidden(row,search_text not in item_text)

    def sent_data(self):
        data = []
        try:
            rows = execute_query(GET_ALL,fetchall=True)
            for row in rows:
                data.append({
                    "order_document_no":row[0],
                    "check_date":row[1],
                    "status":row[2],
                    "username":self.username
                })
            self.order_service.update_order(data)
            execute_query(DELETE_BARCODES,commit=True)
            self.load_barcode()
            self.count_barcode()
            return QMessageBox.information(self.check_form,"Bilgi","İrsaliye Kontrol Verileri Gönderildi")
        except Exception as e:
            print(e)
            return QMessageBox.warning(self.check_form,"Hata",f"İrsaliye Kontrol Modülünde Hata: {str(e)}")

    



    

     

    