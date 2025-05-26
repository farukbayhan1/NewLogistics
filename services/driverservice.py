from api.driverapi import DriverApi

class DriverService:
    def __init__(self):
        self.api_client = DriverApi()
    
    def add_driver(self, driver_data):
        return self.api_client.add_driver_api(driver_data)
    
    def get_drivers(self):
        return self.api_client.get_drivers_api()

    

