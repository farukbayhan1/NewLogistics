from api.userapi import UserApi

class AddUserService:
    def __init__(self):
        self.api_client = UserApi()
    
    def add_user(self, user_data):
        return self.api_client.add_user_api(user_data)
    def get_users(self):
       return self.api_client.get_user_api()
     
    
    

