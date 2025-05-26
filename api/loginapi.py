import requests
from resources.config import BASE_URL

class LoginApi:
   

    def login_api(self,user_data):
        url = f"{BASE_URL}/login"
        response = requests.post(url,json=user_data)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return response.json()
        else:
            raise Exception(f"Login işlemi başarısız, status code: {response.status_code}")
            