<<<<<<< HEAD
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
=======
import subprocess
import sys
import time
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_nodo(script):
    path = os.path.join(BASE_DIR, script)

    return subprocess.Popen(
        [sys.executable, "-u", path],  # 🔥 sin buffer
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )


def test_sistema_inscripciones():
    ip = "127.0.0.1"
    puerto = "5000"

    # ------------------------
    # Nodo D
    # ------------------------
    nodo_d = run_nodo("Hit7/NodoD.py")
    nodo_d.stdin.write(ip + "\n")
    nodo_d.stdin.write(puerto + "\n")
    nodo_d.stdin.flush()

    time.sleep(2)

    # ------------------------
    # Nodo C x2
    # ------------------------
    nodo_c1 = run_nodo("Hit7/NodoC.py")
    nodo_c2 = run_nodo("Hit7/NodoC.py")

    for nodo in [nodo_c1, nodo_c2]:
        nodo.stdin.write(ip + "\n")
        nodo.stdin.write(puerto + "\n")
        nodo.stdin.flush()

    # ⏳ esperar ejecución
    time.sleep(10)

    # ------------------------
    # 🔥 MATAR PROCESOS (CLAVE)
    # ------------------------
    nodo_d.kill()
    nodo_c1.kill()
    nodo_c2.kill()

    time.sleep(1)  # deja que liberen buffers

    # ------------------------
    # AHORA SÍ LEER
    # ------------------------
    out = ""

    for proc in [nodo_d, nodo_c1, nodo_c2]:
        try:
            out += proc.stdout.read()
        except:
            pass

    print("\n--- OUTPUT ---\n", out)

    # ------------------------
    # ASSERTS
    # ------------------------
    assert "Solicitud de inscripcion recibida" in out
    assert "Se actualizo la lista de inscriptos" in out
    assert "Hola Server, soy el cliente" in out
    assert "Hola cliente, soy el Server" in out
>>>>>>> a86a0d563b3313fbbaeaeadaa1332364ec74f6ce
