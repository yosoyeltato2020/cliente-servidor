import requests


url = 'http://127.0.0.1:5000/mensaje'

r = requests.get(url)

print("Respuesta del servidor:", r.text)
