import threading
import time
import io
import contextlib
from Hit1.ServerB import ejecutar_servidor
from Hit1.ClienteA import ejecutar_cliente

def test_interaccion_proceso():
    # 1. Iniciar servidor en segundo plano
    server_thread = threading.Thread(target=ejecutar_servidor, daemon=True)
    server_thread.start()
    
    time.sleep(0.2)  # Espera para el bind del socket

    # 2. Capturar la salida estándar (stdout) para validar el comportamiento
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        ejecutar_cliente()
    
    output = f.getvalue()

    # 3. Validar los resultados impresos
    assert "Hola A, soy B. Saludo recibido." in output
    print("Prueba de integración exitosa: Mensaje detectado en consola.")

if __name__ == "__main__":
    test_interaccion_proceso()