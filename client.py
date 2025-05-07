import requests


url = 'http://127.0.0.1:5000/mensaje'

respuesta = requests.get(url)

print("Respuesta del servidor:", respuesta.text)
