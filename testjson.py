import json

with open('resources/il.json','r',encoding=('utf-8')) as f:
    city = json.load(f)

if isinstance(city,dict) and 'il' in city:
    city_list = city['il']
else:
    city_list = city

print(city_list[0])