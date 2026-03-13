import socket
import threading
import sys
import time
import json

listen_ip = sys.argv[1]
listen_port = int(sys.argv[2])
remote_ip = sys.argv[3]
remote_port = int(sys.argv[4])
nombre = sys.argv[5]  # Nombre del nodo (A, B o C)


def servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_ip, listen_port))
    server_socket.listen(5)

    print(f"[SERVIDOR] Escuchando en {listen_ip}:{listen_port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"[SERVIDOR] Conexión recibida de {addr}")

        try:
            data = conn.recv(1024)

            if data:
                # Deserializar JSON recibido
                mensaje_json = json.loads(data.decode())

                print("[SERVIDOR] Mensaje recibido:", mensaje_json)

                # Crear respuesta
                respuesta = {
                    "mensaje": "Saludo recibido",
                    "origen": mensaje_json.get("origen")
                }

                # Serializar JSON
                conn.send(json.dumps(respuesta).encode())

        except (ConnectionResetError, json.JSONDecodeError):
            print("[SERVIDOR] Error en la conexión o en el formato JSON")

        finally:
            conn.close()


def cliente():
    while True:
        try:
            print(f"[CLIENTE] Intentando conectar a {remote_ip}:{remote_port}")

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((remote_ip, remote_port))

            # Crear mensaje JSON
            saludo = {
                "origen": f"{listen_ip}:{listen_port}",
                "mensaje": f"Hola desde nodo {nombre}"
            }

            # Serializar JSON
            sock.send(json.dumps(saludo).encode())

            respuesta = sock.recv(1024)

            if respuesta:
                # Deserializar JSON
                respuesta_json = json.loads(respuesta.decode())
                print("[CLIENTE] Respuesta recibida:", respuesta_json)

            sock.close()

            time.sleep(5)

        except (ConnectionRefusedError, ConnectionResetError, OSError):
            print("[CLIENTE] No se pudo conectar. Reintentando en 3 segundos...")
            time.sleep(3)


thread_servidor = threading.Thread(target=servidor)
thread_cliente = threading.Thread(target=cliente)

thread_servidor.start()
thread_cliente.start()

thread_servidor.join()
thread_cliente.join()