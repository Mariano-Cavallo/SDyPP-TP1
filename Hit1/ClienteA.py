import socket


def ejecutar_cliente(host="127.0.0.1", port=5000):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        mensaje = "Hola B, te saluda A."
        client_socket.send(mensaje.encode())
        
        respuesta = client_socket.recv(1024).decode()
        print(f"Cliente recibió: {respuesta}")
        
        client_socket.close()
    except Exception as e:
        print(f"Error en cliente: {e}")

if __name__ == "__main__":
    ejecutar_cliente()