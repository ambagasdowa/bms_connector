import requests

url = 'https://10.14.17.105:8000/upload'
files = [('files', open('/home/ambagasdowa/geolocation.zip', 'rb')),
         ('files', open('/home/ambagasdowa/D3_OST.rar', 'rb'))]
resp = requests.post(url=url, files=files)
print(resp.json())
