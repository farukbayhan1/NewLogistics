from api.vehicle import VehicleApi

class VehicleService:
    def __init__(self):
        self.api_client = VehicleApi()
    
    def add_vehicle(self,vehicle_data):
        return self.api_client.add_vehicle_api(vehicle_data)
    
    def get_vehicle(self):
        return self.api_client.get_vehicle_api()