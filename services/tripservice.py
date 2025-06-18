from api.tripapi import TripApi

class TripService:
    def __init__(self):
        self.api_client = TripApi()
    
    def create_trip(self, trip_data):
        return self.api_client.create_trip_api(trip_data)
    
    def get_trips(self):
        return self.api_client.get_trip_api()
    
    def load_trip(self,order_list):
        return self.api_client.load_trip(order_list)
    
    
    