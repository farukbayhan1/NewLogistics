import requests
from resources.config import BASE_URL

class CourierApi:

    def add_courier_api(self,courier_data):
        url = f"{BASE_URL}/courier"
        response = requests.post(url,json=courier_data)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return response.json()
        elif response.status_code == 401:
            return response.json()
        else:
            Exception(f"Kurye Eklenirken Hata Oluştu: {response.status_code} - {response.text}")

    def get_couriers_api(self):
        url = f"{BASE_URL}/courier"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code in (404,401):
            return response.json()
        else:
            Exception(f"Kuryeler Alınırken Hata Oluştu: {response.status_code} - {response.text}")