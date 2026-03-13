import socket

HOST = "0.0.0.0"   # Escucha en todas las interfaces
PORT = 5000        # Puerto del servidor

# Crear socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asociar dirección y puerto
server_socket.bind((HOST, PORT))

# Escuchar conexiones
server_socket.listen(1)
print("Servidor esperando conexión...")

# Aceptar conexión
conn, addr = server_socket.accept()
print("Conectado con:", addr)

# Recibir saludo
mensaje = conn.recv(1024).decode()
print("Cliente dice:", mensaje)

# Responder saludo
respuesta = "Hola A, soy B. Saludo recibido."
conn.send(respuesta.encode())

# Cerrar conexión
input("Presiona Enter para salir...")
conn.close()
server_socket.close()