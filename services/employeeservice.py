from api.employeeapi import EmployeeApi

class AddEmployeeService:
    def __init__(self):
        self.api_client = EmployeeApi()
    
    def add_employee(self, employee_data):
        return  self.api_client.add_employee_api(employee_data)
    
    def get_employee(self):
        return self.api_client.get_employee_api()
    