from flask import Flask, render_template_string, redirect, url_for
import random

app = Flask(__name__)

# Configuración del tablero
FILAS = 10
COLUMNAS = 20
tablero = []

def crear_tablero(filas, columnas):
    return [[random.choice([0, 1]) for _ in range(columnas)] for _ in range(filas)]

def contar_vecinas_vivas(tablero, x, y):
    filas = len(tablero)
    columnas = len(tablero[0])
    vecinas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    
    vivas = 0
    for dx, dy in vecinas:
        nx, ny = x + dx, y + dy
        if 0 <= nx < filas and 0 <= ny < columnas:
            vivas += tablero[nx][ny]
    
    return vivas

def siguiente_generacion(tablero):
    filas = len(tablero)
    columnas = len(tablero[0])
    nuevo_tablero = [[0 for _ in range(columnas)] for _ in range(filas)]
    
    for i in range(filas):
        for j in range(columnas):
            vivas = contar_vecinas_vivas(tablero, i, j)
            if tablero[i][j] == 1 and vivas in [2, 3]:
                nuevo_tablero[i][j] = 1
            elif tablero[i][j] == 0 and vivas == 3:
                nuevo_tablero[i][j] = 1
    return nuevo_tablero

# HTML para renderizar
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Juego de la Vida</title>
    <style>
        table { border-collapse: collapse; }
        td {
            width: 20px;
            height: 20px;
            border: 1px solid #ccc;
        }
        .viva { background-color: black; }
        .muerta { background-color: white; }
        button {
            margin-top: 10px;
            padding: 10px 20px;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <h1>Juego de la Vida de Conway</h1>
    <table>
        {% for fila in tablero %}
        <tr>
            {% for celda in fila %}
            <td class="{{ 'viva' if celda == 1 else 'muerta' }}"></td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    <form action="{{ url_for('siguiente') }}" method="post">
        <button type="submit">Siguiente Generación</button>
    </form>
    <form action="{{ url_for('reiniciar') }}" method="post">
        <button type="submit">Reiniciar Tablero</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def mostrar_tablero():
    return render_template_string(HTML_TEMPLATE, tablero=tablero)

@app.route("/siguiente", methods=["POST"])
def siguiente():
    global tablero
    tablero[:] = siguiente_generacion(tablero)
    return redirect(url_for('mostrar_tablero'))

@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    global tablero
    tablero[:] = crear_tablero(FILAS, COLUMNAS)
    return redirect(url_for('mostrar_tablero'))

if __name__ == "__main__":
    tablero = crear_tablero(FILAS, COLUMNAS)
    app.run(host="0.0.0.0", port=5000)
