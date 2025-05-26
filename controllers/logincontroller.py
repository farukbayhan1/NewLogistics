from PyQt5.QtWidgets import QMessageBox, QWidget
from services.loginservice import LoginService
from views.index import MainWindow

class LoginController:
    def __init__(self,window:QWidget):
        self.window = window
        self.service = LoginService()
        self.connect_signal()
        
    def connect_signal(self):
        self.window.pushButtonEnter.clicked.connect(self.handle_login)
        
    def handle_login(self):
        
        # Get Data
        username = self.window.lineEditUserName.text().strip()
        user_password = self.window.lineEditUserPassword.text().strip()
        if not username or not user_password:
            QMessageBox.warning(self.window,"Uyarı", "Kullanıcı Adı ve Şifre Zorunludur")
            return
        
        #Service
        try:
            result = self.service.login({
                "username":username,
                "password":user_password
            })
            
            if "Bilgi" in result:
                user_role = result.get("Bilgi")
                QMessageBox.information(self.window, "Giriş Başarılı", f"Hoşgeldin! {username.capitalize()}")
                self.open_main_window(username,user_role)
            if "Hata" in result:
                hata = result.get("Hata")
                QMessageBox.information(self.window,"Hata",f"{str(hata)}")

        except Exception as e:
            QMessageBox.warning(self.window, "Hata", f"Giriş işleminde hata oluştu:\n{str(e)}")
            print(str(e))

    def open_main_window(self,username,user_role):
        self.main_window = MainWindow(username,user_role)
        self.main_window.show()
        self.window.close()

