import socket

def ejecutar_servidor(host="127.0.0.1", port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    conn, addr = server_socket.accept()
    mensaje = conn.recv(1024).decode()
    
    respuesta = "Hola A, soy B. Saludo recibido."
    conn.send(respuesta.encode())

    print("Mensaje recibido:", mensaje)
    
    conn.close()
    server_socket.close()
    return mensaje

if __name__ == "__main__":
    ejecutar_servidor()