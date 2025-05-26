from api.loginapi import LoginApi

class LoginService:
    def __init__(self):
        self.api_client = LoginApi()

    def login(self,user_data):
        return self.api_client.login_api(user_data)
    
    