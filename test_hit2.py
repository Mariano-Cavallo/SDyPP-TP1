import subprocess
import sys
import time
import threading

def stream_reader(pipe, label, results):
    """Lee la salida y la almacena para validación."""
    try:
        for line in iter(pipe.readline, ''):
            clean_line = line.strip()
            if clean_line:
                print(f"[{label}] {clean_line}")
                results.append(clean_line)
    except Exception:
        pass

def start_server():
    """Inicia una nueva instancia de ServerB.py."""
    return subprocess.Popen(
        [sys.executable, "-u", "hit2\ServerB.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

def run_test():
    outputs = []
    print("--- Iniciando Test de Reconexión ---")
    
    # 1. Iniciar ClienteA (se mantiene activo durante todo el test)
    client = subprocess.Popen(
        [sys.executable, "-u", "hit2\ClienteA.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    threading.Thread(target=stream_reader, args=(client.stdout, "CLIENT", outputs), daemon=True).start()

    # --- CICLO 1: Conexión Inicial ---
    print("\n[TEST] Iniciando Servidor (Intento 1)...")
    server = start_server()
    threading.Thread(target=stream_reader, args=(server.stdout, "SERVER", outputs), daemon=True).start()
    
    time.sleep(4) # Tiempo para saludo inicial
    
    print("\n[TEST] Cerrando Servidor...")
    server.kill()
    
    # --- ESPERA: El cliente debe entrar en modo reintento ---
    print("\n[TEST] Esperando 6 segundos (simulando caída del servicio)...")
    time.sleep(6)
    
    # --- CICLO 2: Reconexión ---
    print("\n[TEST] Reiniciando Servidor (Intento 2)...")
    server = start_server()
    threading.Thread(target=stream_reader, args=(server.stdout, "SERVER", outputs), daemon=True).start()
    
    time.sleep(5) # Tiempo para que el cliente detecte el servidor y reconecte

    print("\n--- Finalizando Test ---")
    client.kill()
    server.kill()
    
    # Verificación de doble éxito
    conteo_conexiones = sum(1 for line in outputs if "Conectado con B" in line)
    
    if conteo_conexiones >= 2:
        print(f"\nRESULTADO: TEST EXITOSO ({conteo_conexiones} conexiones detectadas)")
    else:
        print(f"\nRESULTADO: TEST FALLIDO (Solo {conteo_conexiones} conexión/es)")

if __name__ == "__main__":
    run_test()