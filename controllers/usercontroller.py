from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem, QAbstractItemView, QProgressBar, QApplication
from PyQt5.QtCore import QEvent,QObject
from services.userservice import AddUserService



class AddUserController():
    def __init__(self, tab:QWidget):
        self.tab = tab
        self.username = tab.username
        self.user_role = tab.user_role

        self.connect_signal()
        self.service = AddUserService()
        self.tab.lineEditUserName.focusInEvent = lambda event: print(self.tab.lineEditUserName.text())
        self.combobox_add_item()
        self.tab.tableWidgetUsers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.load_users()

    def combobox_add_item(self):
        authority_list = ['user','admin']
        for i in authority_list:
            self.tab.comboBoxAuthority.addItem(i)    

    def connect_signal(self):
        self.tab.pushButtonCreateUser.clicked.connect(self.handle_user_add)
   
    def handle_user_add(self):
        
        # Admin Controller
        if not self.user_role == 'admin':
            QMessageBox.warning(self.tab,"Uyarı", "Kullanıcının Yetkisi Yok")
        
        else:
            # Get Data From User
            add_username = self.tab.lineEditUserName.text().strip()
            add_password = self.tab.lineEditPassword.text()
            add_userrole = self.tab.comboBoxAuthority.currentText()

            # User Name and Password Validation
            if not add_username or not add_password or not add_userrole:
                QMessageBox.warning(self.tab, "Uyarı", "Kullanıcı Adı, Şifre ve Yetki Zorunludur.")
                return
            
            try:
                result = self.service.add_user({
                    "username": add_username,
                    "password": add_password,
                    "authority": add_userrole
                })
                self.tab.lineEditUserName.clear()
                self.tab.lineEditPassword.clear()
                self.tab.comboBoxAuthority.setCurrentIndex(0)
                if "Bilgi" in result:
                    new_result = result.get("Bilgi")
                    QMessageBox.information(self.tab,"Bilgi",f"{new_result}")
                    self.load_users()
                elif "Hata" in result:
                    QMessageBox.warning(self.tab,"Hata","Kullanıcı Daha Önce Eklenmiş")
                    self.load_users()
                print(result)
            except Exception as e:
                QMessageBox.warning(self.tab, "Hata", f"Kullanıcı Oluşturulurken Bir hata oluştu: {str(e)}")
                self.load_users()
                print(str(e))
                return
            
    def load_users(self):
        if self.user_role == 'admin':
            try:
                user_list = self.service.get_users()
                print(user_list)
                self.tab.tableWidgetUsers.setRowCount(len(user_list))
                self.tab.tableWidgetUsers.setColumnCount(2)
                self.tab.tableWidgetUsers.setHorizontalHeaderLabels(["Kullanıcı Adı", "Yetki"])
                
                for row_index, user in enumerate(user_list):
                    self.tab.tableWidgetUsers.setItem(row_index, 0, QTableWidgetItem(user["userName"]))
                    self.tab.tableWidgetUsers.setItem(row_index, 1, QTableWidgetItem(user["userRoleName"]))

            except Exception as e:
                QMessageBox.warning(self.tab, "Hata", f"Kullanıcılar alınırken hata oluştu: {str(e)}")
                print(str(e))
        