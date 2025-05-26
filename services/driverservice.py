from api.driverapi import DriverApi

class AddDriverService:
    def __init__(self):
        self.api_client = DriverApi()
    
    def add_driver(self, driver_data):
        return self.api_client.add_driver(self,driver_data)
    

