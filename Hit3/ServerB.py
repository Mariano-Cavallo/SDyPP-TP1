import socket

HOST = "0.0.0.0"
PORT = 5000

# Crear socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permitir reutilizar el puerto rápidamente
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Asociar dirección y puerto
server_socket.bind((HOST, PORT))

# Escuchar conexiones
server_socket.listen(1)

print("Servidor iniciado...")

while True:
    print("Esperando conexión...")

    try:
        # Aceptar conexión
        conn, addr = server_socket.accept()
        print("Conectado con:", addr)

        while True:
            mensaje = conn.recv(1024)

            if not mensaje:
                print("Cliente desconectado.")
                break

            print("Cliente dice:", mensaje.decode())

            respuesta = "Hola A, soy B. Saludo recibido."
            conn.send(respuesta.encode())

        conn.close()

    except Exception as e:
        print("Error en la conexión:", e)
        conn.close()