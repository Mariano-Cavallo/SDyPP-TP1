import subprocess
import sys
import time
import threading

def stream_reader(pipe, label, results):
    """Lee la salida y la almacena para validación en tiempo real."""
    try:
        # Se usa iter para leer línea por línea sin bloquear el hilo principal
        for line in iter(pipe.readline, ''):
            clean_line = line.strip()
            if clean_line:
                print(f"[{label}] {clean_line}")
                results.append(clean_line)
    except Exception:
        pass

def start_client():
    """Inicia una nueva instancia de ClienteA.py con salida sin buffer."""
    return subprocess.Popen(
        [sys.executable, "-u", "hit3\\ClienteA.py"], # -u para evitar buffering
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

def run_test():
    outputs = []
    print("--- Iniciando Test: Reconexión de Cliente ---")
    
    # 1. Iniciar Servidor (Se mantiene activo durante todo el test)
    print("\n[TEST] Iniciando Servidor B...")
    server = subprocess.Popen(
        [sys.executable, "-u", "hit3\\ServerB.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    threading.Thread(target=stream_reader, args=(server.stdout, "SERVER", outputs), daemon=True).start()
    
    time.sleep(2) # Tiempo para que el servidor abra el puerto

    # --- CICLO 1: Primera conexión del Cliente ---
    print("\n[TEST] Lanzando Cliente (Intento 1)...")
    client = start_client()
    threading.Thread(target=stream_reader, args=(client.stdout, "CLIENT_1", outputs), daemon=True).start()
    
    time.sleep(4) # Tiempo para conexión y saludo
    
    print("\n[TEST] Cerrando primer Cliente...")
    client.terminate()
    client.wait() # Esperar a que el proceso se limpie
    
    print("\n[TEST] Pausa de 3 segundos...")
    time.sleep(3)
    
    # --- CICLO 2: Segunda conexión del Cliente ---
    print("\n[TEST] Lanzando Cliente (Intento 2)...")
    client = start_client()
    threading.Thread(target=stream_reader, args=(client.stdout, "CLIENT_2", outputs), daemon=True).start()
    
    time.sleep(4) # Tiempo para reconexión

    print("\n--- Finalizando Test ---")
    # Limpieza final
    client.terminate()
    server.terminate()
    
    # Verificación de lógica: buscar mensajes de éxito en la lista 'outputs'
    # Ajusta "Conectado con B" por el mensaje exacto que imprima tu ClienteA.py
    conteo_conexiones = sum(1 for line in outputs if "Conectado con B" in line)
    
    print("\n--------------------------------------")
    if conteo_conexiones >= 2:
        print(f"RESULTADO: TEST EXITOSO ({conteo_conexiones} conexiones detectadas)")
        sys.exit(0)
    else:
        print(f"RESULTADO: TEST FALLIDO (Solo {conteo_conexiones} conexión/es detectadas)")
        sys.exit(1)

if __name__ == "__main__":
    run_test()