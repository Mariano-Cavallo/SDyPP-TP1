import socket

HOST = "0.0.0.0"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("Servidor B esperando conexiones...")

while True:
    conn, addr = server_socket.accept()
    print("Cliente conectado:", addr)

    try:
        while True:
            data = conn.recv(1024)

            # Si el cliente cerró la conexión
            if not data:
                print("Cliente desconectado:", addr)
                break

            mensaje = data.decode()
            print("Cliente dice:", mensaje)

            respuesta = "Hola A, soy B. Saludo recibido."
            conn.send(respuesta.encode())

    except ConnectionResetError:
        print("Cliente terminó el proceso abruptamente:", addr)

    finally:
        conn.close()
        print("Conexión cerrada con", addr)