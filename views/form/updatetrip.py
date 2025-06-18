from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QTableWidgetItem, QMessageBox, QHeaderView, QStyleOptionButton, QStyle
from PyQt5.QtCore import QPropertyAnimation, Qt, QRect, pyqtSignal
from PyQt5.QtGui import QPainter

from services.orderservice import OrderService

class CheckBoxHeader(QHeaderView):
    toggleCheckState = pyqtSignal(bool)

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.isChecked = False
        self.setSectionsClickable(True)
        self.sectionClicked.connect(self.handle_click)

    def paintSection(self, painter, rect, logicalIndex):
        super().paintSection(painter, rect, logicalIndex)
        if logicalIndex == 0:
            option = QStyleOptionButton()
            option.rect = QRect(rect.left() + 5, rect.center().y() - 10, 20, 20)
            option.state = QStyle.State_Enabled | (QStyle.State_On if self.isChecked else QStyle.State_Off)
            painter.save()
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)
            painter.restore()

    def handle_click(self, logicalIndex):
        if logicalIndex == 0:
            self.isChecked = not self.isChecked
            self.updateSection(0)
            self.toggleCheckState.emit(self.isChecked)

class TripUpdate(QWidget):
    def __init__(self, controller=None, trip_data=None):
        super().__init__()
        uic.loadUi("ui/templates/form/updateform/updatetrip.ui", self)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.setStyleSheet("background-color: rgba(242, 246, 252, 255); border-radius: 15px;")

        self.controller = controller
        self.trip_data = trip_data
        self.order_service = OrderService()
        self.selected_order_list = []

        self.load_trip_data()
        self.setup_order_table()

        self.tableWidgetLoading.itemChanged.connect(self.handle_check_box)
        self.lineEditLoadingOrderSearch.textChanged.connect(self.search_order)
        self.pushButtonAddOrder.clicked.connect(self.load_selected_orders)
        self.pushButtonDelete.clicked.connect(self.delete_selected_loaded_orders)

    def load_trip_data(self):
        self.lineEditTripNumber.setText(self.trip_data.get("tripCode", ""))
        self.lineEditVehiclePlateNumber.setText(self.trip_data.get("vehicleNumberPlate", ""))
        self.lineEditDriverName.setText(self.trip_data.get("driverName", ""))
        self.lineEditCourierName.setText(self.trip_data.get("courierName", ""))
        self.lineEditLoadingProvince.setText(self.trip_data.get("tripLoadingProvince", ""))
        self.lineEditLoadingDistrict.setText(self.trip_data.get("tripLoadingDistrict", ""))
        self.lineEditDestinationProvince.setText(self.trip_data.get("tripDestinationProvince", ""))
        self.lineEditDestinationDistrict.setText(self.trip_data.get("tripDestinationDistrict", ""))

    def setup_order_table(self):
        try:
            order_list = self.order_service.get_orders(filters={"trip_code": None})
            self.tableWidgetLoading.setRowCount(len(order_list))
            self.tableWidgetLoading.setColumnCount(10)

            header = CheckBoxHeader(Qt.Horizontal, self.tableWidgetLoading)
            self.tableWidgetLoading.setHorizontalHeader(header)
            header.toggleCheckState.connect(self.toggle_all_checkboxes)

            self.tableWidgetLoading.setHorizontalHeaderLabels([
                "", "Sipariş Id", "Müşteri Adı", "Sipariş Numarası", "İrsaliye Numarası",
                "Paket Ad.", "Teslimat Adresi", "Sipariş Onay Tarihi", "Plan Onay Tarihi", "Sipariş Sefer Numarası"
            ])

            for row_index, order in enumerate(order_list):
                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                checkbox_item.setCheckState(Qt.Unchecked)
                self.tableWidgetLoading.setItem(row_index, 0, checkbox_item)
                for col_index, value in enumerate([order[0], order[5], order[1], order[2], order[6], order[3], order[7], order[8], order[9]]):
                    self.tableWidgetLoading.setItem(row_index, col_index + 1, QTableWidgetItem(str(value)))

            self.tableWidgetLoading.setColumnHidden(1, True)
            self.tableWidgetLoading.horizontalHeader().setMinimumHeight(30)

        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Sipariş Bilgileri Getirilirken Hata Oluştu:\n{str(e)}")

    def toggle_all_checkboxes(self, check: bool):
        for row in range(self.tableWidgetLoading.rowCount()):
            item = self.tableWidgetLoading.item(row, 0)
            if item:
                item.setCheckState(Qt.Checked if check else Qt.Unchecked)

    def toggle_all_loaded_checkboxes(self, check: bool):
        for row in range(self.tableWidgetLoaded.rowCount()):
            item = self.tableWidgetLoaded.item(row, 0)
            if item:
                item.setCheckState(Qt.Checked if check else Qt.Unchecked)

    def handle_check_box(self, item):
        if item.column() == 0:
            row = item.row()
            order_id_item = self.tableWidgetLoading.item(row, 1)
            if order_id_item:
                order_id = order_id_item.text()
                if item.checkState() == Qt.Checked:
                    if order_id not in self.selected_order_list:
                        self.selected_order_list.append(order_id)
                else:
                    if order_id in self.selected_order_list:
                        self.selected_order_list.remove(order_id)

    def search_order(self, text):
        search_text = text.strip().upper().replace(" ", "")
        for row in range(self.tableWidgetLoading.rowCount()):
            item = self.tableWidgetLoading.item(row, 4)
            if item:
                item_text = item.text().strip().upper().replace(" ", "")
                self.tableWidgetLoading.setRowHidden(row, search_text not in item_text)

    def load_selected_orders(self):
        self.tableWidgetLoaded.setRowCount(0)
        for row in range(self.tableWidgetLoading.rowCount()):
            order_id_item = self.tableWidgetLoading.item(row, 1)
            if order_id_item and order_id_item.text() in self.selected_order_list:
                new_row = self.tableWidgetLoaded.rowCount()
                self.tableWidgetLoaded.insertRow(new_row)

                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                checkbox_item.setCheckState(Qt.Unchecked)
                self.tableWidgetLoaded.setItem(new_row, 0, checkbox_item)

                for col in range(2, 10):
                    item = self.tableWidgetLoading.item(row, col)
                    if item:
                        self.tableWidgetLoaded.setItem(new_row, col - 1, QTableWidgetItem(item.text()))

                hidden_id = QTableWidgetItem(order_id_item.text())
                hidden_id.setFlags(Qt.ItemIsEnabled)
                self.tableWidgetLoaded.setItem(new_row, 9, hidden_id)

        self.tableWidgetLoaded.setColumnCount(10)

        loaded_header = CheckBoxHeader(Qt.Horizontal, self.tableWidgetLoaded)
        self.tableWidgetLoaded.setHorizontalHeader(loaded_header)
        loaded_header.toggleCheckState.connect(self.toggle_all_loaded_checkboxes)

        self.tableWidgetLoaded.setHorizontalHeaderLabels([
            "", "Müşteri Adı", "Sipariş Numarası", "İrsaliye Numarası",
            "Paket Ad.", "Teslimat Adresi", "Sipariş Onay Tarihi",
            "Plan Onay Tarihi", "Sipariş Sefer Numarası", "Sipariş Id"
        ])
        self.tableWidgetLoaded.setColumnHidden(9, True)

    def delete_selected_loaded_orders(self):
        rows_to_delete = []
        for row in range(self.tableWidgetLoaded.rowCount()):
            item = self.tableWidgetLoaded.item(row, 0)
            if item and item.checkState() == Qt.Checked:
                order_id_item = self.tableWidgetLoaded.item(row, 9)
                if order_id_item:
                    rows_to_delete.append((row, order_id_item.text()))

        for row, order_id in reversed(rows_to_delete):
            self.tableWidgetLoaded.removeRow(row)
            if order_id in self.selected_order_list:
                self.selected_order_list.remove(order_id)
