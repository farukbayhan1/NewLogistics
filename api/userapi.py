import requests
from resources.config import BASE_URL
class UserApi:
    
    def add_user_api(self, user_data):
        url = f"{BASE_URL}/user"
        response = requests.post(url, json=user_data)
        if response.status_code in (201, 200, 400, 401):
            return response.json()
        else:
            Exception(f"Kullanıcı Eklenirken Hata Oluştu: {response.status_code} - {response.text}")

    def get_user_api(self):
        url = f"{BASE_URL}/user"
        response = requests.get(url)
        if response.status_code in (200, 400, 401):
            return response.json()
        else:
            raise Exception(f"Kullanıcılar Alınırken Hata Oluştu: {response.status_code} - {response.text}")