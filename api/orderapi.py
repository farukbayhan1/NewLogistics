import requests
from resources.config import BASE_URL

class OrderApi:
    def add_order(self,order_data):
        url = f"{BASE_URL}/order"
        response = requests.post(url, json=order_data)
        if response.status_code in (201, 200, 400, 401):
            return response.json()
        else:
            Exception(f"Sipariş Oluşturma İşleminde Hata Oluştu: {response.status_code} - {response.text}")

    def get_orders(self,filters=None):
        url = f"{BASE_URL}/order"
        response = requests.get(url,params=filters)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Sipariş Listeleme Hatası: {response.status_code} - {response.text}")

    def update_orders(self,order_data):
        url = f"{BASE_URL}/order"
        response = requests.put(url,json=order_data)
        if response.status_code in (200, 201, 400, 401):
            return response.json()
        else:
            raise Exception(f"Sipariş Güncelleme Hatası: {response.status_code} - {response.text}")
                