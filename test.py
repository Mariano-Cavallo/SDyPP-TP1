import subprocess
import time
import socket

def test_full_integration():
    # 1. Lanzamos el Servidor B en segundo plano
    server_proc = subprocess.Popen(["python3", "ServerB.py"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True)
    
    # Esperamos un momento a que el socket del servidor abra el puerto 5000
    time.sleep(2) 

    try:
        # 2. Ejecutamos el Cliente A y capturamos su salida
        client_result = subprocess.run(["python3", "ClienteA.py"], 
                                       capture_output=True, 
                                       text=True, 
                                       timeout=10)
        
        # 3. Verificaciones
        # Revisamos si el cliente imprimió la respuesta esperada
        assert "Hola A, soy B. Saludo recibido." in client_result.stdout
        
    finally:
        # Limpieza: Matamos el proceso del servidor al terminar
        server_proc.terminate()
        server_proc.wait()

def test_port_availability():
    """Verifica si el puerto 5000 está libre antes de empezar (útil en CI/CD)"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 5000))
    sock.close()
    # Si result es distinto de 0, el puerto está libre
    assert result != 0, "El puerto 5000 ya está ocupado. El test fallará."