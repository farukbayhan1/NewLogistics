import requests
from resources.config import BASE_URL

class DriverApi:
    
    
    def add_driver(self, driver_data):
        url = f"{BASE_URL}/driver"
        response = requests.post(url, json=driver_data)
        if response.status_code == 201:
            return response.json()
        else:
            Exception(f"Failed to add driver: {response.status_code} - {response.text}")

            


        
        
    