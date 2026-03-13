import socket

HOST = "127.0.0.1"  # Dirección del servidor B
PORT = 5000         # Puerto del servidor

# Crear socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectarse al servidor
client_socket.connect((HOST, PORT))

# Enviar saludo
mensaje = "Hola B, te saluda A."
client_socket.send(mensaje.encode())

# Recibir respuesta
respuesta = client_socket.recv(1024).decode()
print("Servidor responde:", respuesta)

# Cerrar conexión
client_socket.close()