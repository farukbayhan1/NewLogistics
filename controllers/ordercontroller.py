from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidget, QTableWidgetItem, QFileDialog, QHeaderView
from PyQt5.QtCore import Qt
from services.orderservice import OrderService
from services.employeeservice import AddEmployeeService
from views.form.createorder import CreateOrder
from views.tabs.order.updateorder import UpdateOrderTab
import pandas as pd


class OrderController:
    def __init__(self, tab:QWidget):
        self.tab = tab
        self.service = OrderService()
        self.username = self.tab.username
        self.user_role = self.tab.user_role
        self.tab.pushButtonImport.clicked.connect(self.import_order)
        self.order_form = CreateOrder()
        self.connect_signal()
    

    def connect_signal(self):
        self.tab.pushButtonOpenOrderForm.clicked.connect(self.open_create_order_form)
        self.tab.pushButtonSend.clicked.connect(self.handle_import_data)
        self.order_form.pushButtonOrderCreate.clicked.connect(self.handle_create_order_form)
    
    def import_order(self):
        try:

            file_path, _ = QFileDialog.getOpenFileName(self.tab, "Dosya Seç", "", "Excel Dosyaları (*.xls *.xlsx)")
            if file_path:
                df = pd.read_excel(file_path)
                df.columns = df.columns.str.strip()
                column_mapping = {
                    "Sipariş No": "order_no",
                    "İrs No": "order_document_no",
                    "Tes. Adres": "order_delivery_adress",
                    "Plaka": "order_number_plate",
                    "Sürücü": "order_driver",
                    "Paket Ad.": "order_box_count",
                    "Sip. Onay Tarihi": "order_confirmation_date",
                    "Plan Onay Tar.": "order_plan_confirmation_date",
                    "Siparişi Veren Müş.": "employee_name",
                    "Sefer No": "order_trip_number"
                }
                expected_columns = set(column_mapping.keys())
                found_columns = set(df.columns)
                missing_columns = expected_columns - found_columns

                if missing_columns:
                    QMessageBox.critical(self.tab, "Eksik Sütunlar",f"Aşağıdaki gerekli sütunlar eksik:\n\n{', '.join(missing_columns)}")
                    return
                
                else:
                    df = df[list(column_mapping.keys())].rename(columns=column_mapping)
                    df["username"] = self.username
                    self.loaded_df = df
                    self.load_data = self.loaded_df.to_dict(orient="records")
                    self.tab.tableWidgetImportedOrders.setRowCount(len(df))
                    self.tab.tableWidgetImportedOrders.setColumnCount(len(df.columns))
                    self.headers = list(column_mapping.keys()) + ["username"]
                    self.tab.tableWidgetImportedOrders.setHorizontalHeaderLabels(self.headers)
                    self.tab.tableWidgetImportedOrders.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    self.tab.tableWidgetImportedOrders.setWordWrap(False)
                    username_index = self.headers.index("username")
                    self.tab.tableWidgetImportedOrders.setColumnHidden(username_index, True)
                    for row_idx, row in df.iterrows():
                        for col_idx, value in enumerate(row):
                            item = QTableWidgetItem(str(value))
                            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                            item.setToolTip(str(value)) 
                            self.tab.tableWidgetImportedOrders.setItem(row_idx, col_idx, item)
                    
                            
        except Exception as e:
            print(str(e))
            QMessageBox.warning(self.tab,"Hata",f"Import İşleminde Bir hata Oluştu: {str(e)}")

    def open_create_order_form(self):
        self.load_employee()
        self.order_form.show()
        self.order_form.animation.start()

    def handle_create_order_form(self):
        order_no = self.order_form.lineEditOrderNumber.text().upper().strip()
        order_document_no = self.order_form.lineEditOrderDocumentNumber.text().upper().strip()
        order_delivery_adress = self.order_form.textEditOrderDestinationAdress.toPlainText().upper().strip()
        order_number_plate = self.order_form.lineEditOrderPlateNumber.text().upper().strip()
        order_driver = self.order_form.lineEditOrderDriver.text().upper().strip()
        order_box_count = str(self.order_form.spinBoxOrderBoxCount.value())
        order_confirmation_date = self.order_form.lineEditOrderConfirmDate.text()
        order_plan_confirmation_date = self.order_form.lineEditOrderPlanConfirmDate.text()
        order_trip_number = self.order_form.lineEditOrderTripNumber.text().upper().strip()
        employee_name = self.order_form.comboBoxEmployee.currentText().upper().strip()

        try:
            # Service Func And Create Data
            result = self.service.add_order({
                "order_no":order_no,
                "order_document_no":order_document_no,
                "order_delivery_adress":order_delivery_adress,
                "order_number_plate":order_number_plate,
                "order_driver":order_driver,
                "order_box_count":order_box_count,
                "order_confirmation_date":order_confirmation_date,
                "order_plan_confirmation_date":order_plan_confirmation_date,
                "order_trip_number":order_trip_number,
                "employee_name":employee_name,
                "username":self.username
            })

            if "Bilgi" in result:
                return QMessageBox.information(self.order_form,"Bilgi","Sipariş Ekleme İşlemi Başarıyla Gerçekleşti")
            elif "Hata" in result:
                hata = result.get("Hata")
                return QMessageBox.warning(self.order_form,"Hata", f"Sipariş Ekleme İşleminde Hata Oluştu {str(hata)}")
        except Exception as e:
            print(str(e))
            return QMessageBox.warning(self.order_form,"Hata",f"Sunucu Hatası: {str(e)}")
        
    def handle_import_data(self):
        result = self.service.add_order(self.load_data)
        if "Bilgi" in result:
            return QMessageBox.information(self.tab,"Bilgi","Sipariş Ekleme İşlemi Başarılı")
        elif "Hata" in result:
            hata = result.get("Hata")
            print(hata)
            return QMessageBox.warning(self.tab,"Hata","Sipariş Ekleme İşleminde Hata Oluştu")

    def load_employee(self):
        employee_service = AddEmployeeService()
        employee_data = employee_service.get_employees()

    def load_orders(self):
        # Burada siparişlerin yüklenmesi için filtreler oluştur


 
    
  




        