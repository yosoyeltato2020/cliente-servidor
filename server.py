from flask import Flask

app = Flask(__name__)

@app.route('/mensaje')
def enviar_mensaje():
    return "Hola mundo desde el servidor"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
