import threading
import time
import socket
import pickle
from datetime import datetime

# CONFIG
HOST = "127.0.0.1"
PUERTO_D = 6000   # puerto fijo para test

# ---------- SERVIDOR D (simplificado del tuyo) ----------

lista_espera = []
lista_inscriptos = []
condicion = threading.Condition()

def servidor_D():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PUERTO_D))
    server.listen()

    def actualizar():
        while True:
            time.sleep(2)  # en vez de 60 para test rápido
            with condicion:
                lista_inscriptos.clear()
                lista_inscriptos.extend(lista_espera)
                lista_espera.clear()
                condicion.notify_all()

    threading.Thread(target=actualizar, daemon=True).start()

    while True:
        cliente, _ = server.accept()
        threading.Thread(target=handler, args=(cliente,), daemon=True).start()

def handler(cliente):
    datos = cliente.recv(1024)
    ip, puerto = pickle.loads(datos)

    nodo = {
        "Ip": ip,
        "Puerto": puerto,
        "Horario": datetime.now().strftime("%H:%M:%S")
    }

    lista_espera.append(nodo)

    cliente.send("Registrado".encode())

    with condicion:
        condicion.wait()

    cliente.send(pickle.dumps(lista_inscriptos))
    cliente.close()

# ---------- CLIENTE C (simulado) ----------

def cliente_C(resultado):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PUERTO_D))

    cliente.send(pickle.dumps(("127.0.0.1", 7000)))

    cliente.recv(1024)  # mensaje inicial

    datos = cliente.recv(1024)
    lista = pickle.loads(datos)

    resultado.append(lista)

    cliente.close()

# ---------- TEST ----------

def test_inscripcion():
    resultado = []

    # 1. Levanto servidor D
    hilo_servidor = threading.Thread(target=servidor_D)
    hilo_servidor.start()
    time.sleep(1)  # dejo que arranque

    # 2. Simulo cliente C
    hilo_cliente= threading.Thread(target=cliente_C, args=(resultado,))
    hilo_cliente.start()
    hilo_cliente.join()
    # 3. Espero actualización (ventana)


    # 4. Verifico
    assert len(resultado) > 0, "No se recibió lista"
    assert len(resultado[0]) == 1, "No se inscribió correctamente"

    print("TEST OK")
    return

# ejecutar
if __name__ == "__main__":
    test_inscripcion()