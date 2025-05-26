import requests
from resources.config import BASE_URL

class EmployeeApi:
    


    def add_employee_api(self,employee_data):
        url = f"{BASE_URL}/employee"
        response = requests.post(url, json=employee_data)
        if response.status_code == 201:
            return response.json()
        else:
            Exception(f"Failed to add employee: {response.status_code} - {response.text}")

    def get_employee_api(self):
        url = f"{self.BASE_URL}/employee"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get employees: {response.status_code} - {response.text}")
        