import requests
from resources.config import BASE_URL

class TripApi:
    def create_trip_api(self,trip_data):
        url = f"{BASE_URL}/trip"
        response = requests.post(url, json=trip_data)
        if response.status_code in (201, 200, 400, 401):
            return response.json()
        else:
            Exception(f"Sefer Oluşturma İşleminde Hata Oluştu: {response.status_code} - {response.text}")
        
    def get_trip_api(self):
        url = f"{BASE_URL}/trip"
        response = requests.get(url)
        if response.status_code in (200, 400, 401):
            return response.json()
        else:
            raise Exception(f"Seferler Alınırken Hata Oluştu: {response.status_code} - {response.text}")

    """def update_vehicle_api(self,vehicle_data):
        url = f"{BASE_URL}/vehicle"
        response = requests.put(url,json=vehicle_data)
        if response.status_code in (201,400,401):
            return response.json()
        else:
            raise Exception(f"Araç Bilgileri Güncelleme İşleminde Hata Oluştu: {response.status_code} - {response.text}")"""
    
    # Sefer Arama Eklenecek