import requests
from resources.config import BASE_URL

class DriverApi:
    
    
    def add_driver_api(self, driver_data):
        url = f"{BASE_URL}/driver"
        response = requests.post(url, json=driver_data)
        if response.status_code in (201, 400, 401):
            return response.json()
        else:
            raise Exception(f"Sürücü Eklenirken Hata Oluştu: {response.status_code} - {response.text}")
    
    def get_drivers_api(self):
        url = f"{BASE_URL}/driver"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code in (404, 401):
            return response.json()
        else:
            raise Exception(f"Sürücüler Alınırken Hata Oluştu: {response.status_code} - {response.text}")
        
    def update_driver(self,driver_data):
        url = f"{BASE_URL}/driver"
        response = requests.put(url,json=driver_data)
        if response.status_code in (201,400,401):
            return response.json()
        else:
            raise Exception(f"Sürücü Bilgileri Güncellenirken Hata Oluştu: {response.status_code} - {response.text}")

        


            


        
        
    