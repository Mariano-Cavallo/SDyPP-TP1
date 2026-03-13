import socket
import threading
import sys
import time

listen_ip = sys.argv[1]
listen_port = int(sys.argv[2])
remote_ip = sys.argv[3]
remote_port = int(sys.argv[4])


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
                mensaje = data.decode()
                print(f"[SERVIDOR] Recibido: {mensaje}")

                respuesta = "Hola, saludo recibido."
                conn.send(respuesta.encode())

        except ConnectionResetError:
            print("[SERVIDOR] Cliente desconectado abruptamente")

        finally:
            conn.close()


def cliente():
    while True:
        try:
            print(f"[CLIENTE] Intentando conectar a {remote_ip}:{remote_port}")

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((remote_ip, remote_port))

            saludo = "Hola desde nodo C"
            sock.send(saludo.encode())

            respuesta = sock.recv(1024)

            if respuesta:
                print("[CLIENTE] Respuesta:", respuesta.decode())

            sock.close()

            time.sleep(5)

        except (ConnectionRefusedError, ConnectionResetError, OSError):
            print("[CLIENTE] No se pudo conectar. Reintentando en 3 segundos...")
            time.sleep(3)


# Crear threads
thread_servidor = threading.Thread(target=servidor)
thread_cliente = threading.Thread(target=cliente)

thread_servidor.start()
thread_cliente.start()

thread_servidor.join()
thread_cliente.join()