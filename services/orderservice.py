from api.orderapi import OrderApi

class OrderService:
    def __init__(self):
        self.api_client = OrderApi()
    
    def add_order(self, order_data):
        return  self.api_client.add_order(order_data)
    
    def get_orders(self,filters):
        return self.api_client.get_orders(filters)
    
    def update_order(self,order_data):
        return self.api_client.update_orders(order_data)