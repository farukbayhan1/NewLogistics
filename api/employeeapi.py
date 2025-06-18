import requests
from resources.config import BASE_URL

class EmployeeApi:
    


    def add_employee_api(self,employee_data):
        url = f"{BASE_URL}/employee"
        response = requests.post(url, json=employee_data)
        if response.status_code in (201, 400, 401):
            return response.json()
        else:
           raise Exception(f"Müşteri Eklenirken Hata Oluştu: {response.status_code} - {response.text}")
    
    def get_employee_api(self):
        url = f"{BASE_URL}/employee"
        response = requests.get(url)
        if response.status_code in (200, 400,401):
            return response.json()
        else:
            raise Exception(f"Müşteriler Alınırken Hata Oluştu: {response.status_code} - {response.text}")
    
    def update_employee_api(self,employee_data):
        url = f"{BASE_URL}/employee"
        response = requests.put(url,json=employee_data)
        if response.status_code in (201,400,401):
            return response.json()
        else:
            raise Exception(f"Müşteri Bilgilerini Güncelleme İşleminde Hata Oluştu: {response.status_code} - {response.text}")
        

        