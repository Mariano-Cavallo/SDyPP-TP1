import socket
import threading
import time
import pytest
from ServerB import HOST, PORT  # Asegúrate que tus archivos sean importables

def run_server():
    """Función para ejecutar el servidor en un hilo separado."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    
    conn, addr = server_socket.accept()
    mensaje = conn.recv(1024).decode()
    
    respuesta = "Hola A, soy B. Saludo recibido."
    conn.send(respuesta.encode())
    
    conn.close()
    server_socket.close()
    return mensaje

def test_communication():
    # 1. Iniciar servidor en un hilo (thread)
    # Usamos una lista para capturar el valor retornado por el hilo si fuera necesario
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    
    # Pequeña espera para asegurar que el servidor esté escuchando
    time.sleep(1)
    
    # 2. Lógica del Cliente (emulando ClienteA.py)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(("127.0.0.1", PORT))
        
        mensaje_enviado = "Hola B, te saluda A."
        client_socket.send(mensaje_enviado.encode())
        
        respuesta = client_socket.recv(1024).decode()
        
        # 3. Validaciones (Assertions)
        assert respuesta == "Hola A, soy B. Saludo recibido."
        
    finally:
        client_socket.close()
        server_thread.join(timeout=5)