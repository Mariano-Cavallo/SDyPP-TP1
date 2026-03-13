import socket
import time

HOST = "127.0.0.1"
PORT = 5000

while True:
    try:
        print("Intentando conectar con B...")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        print("Conectado con B")

        # Enviar saludo
        mensaje = "Hola B, te saluda A."
        client_socket.send(mensaje.encode())
        print("Saludo enviado")

        # Recibir respuesta
        respuesta = client_socket.recv(1024)

        if not respuesta:
            raise ConnectionError("Conexión cerrada por el servidor")

        print("Servidor responde:", respuesta.decode())

        client_socket.close()

        # Esperar antes de volver a saludar
        time.sleep(5)

    except (ConnectionRefusedError, ConnectionResetError, ConnectionError, OSError):
        print("Conexión perdida con B. Reintentando en 5 segundos...")
        time.sleep(5)