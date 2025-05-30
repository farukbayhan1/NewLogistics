import requests
from resources.config import BASE_URL

class VehicleApi:
    def add_vehicle_api(self,vehicle_data):
        url = f"{BASE_URL}/vehicle"
        response = requests.post(url, json=vehicle_data)
        if response.status_code in (201, 200, 400, 401):
            return response.json()
        else:
            Exception(f" Araç Ekleme İşleminde Hata Oluştu: {response.status_code} - {response.text}")
        
    def get_vehicle_api(self):
        url = f"{BASE_URL}/vehicle"
        response = requests.get(url)
        if response.status_code in (200, 400, 401):
            return response.json()
        else:
            raise Exception(f"Araçlar Alınırken Hata Oluştu: {response.status_code} - {response.text}")
