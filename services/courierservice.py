from api.courierapi import CourierApi

class CourierService:
    def __init__(self):
        self.api_client = CourierApi()
    
    def add_courier(self,courier_data):
        return self.api_client.add_courier_api(courier_data)
    def get_couriers(self):
        return self.api_client.get_couriers_api()
    