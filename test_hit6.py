import subprocess
import time
import requests
import sys
import os

def run_test():
    print("--- Iniciando Prueba de Red P2P Automática ---")
    
    # Forzar a Python a no usar buffer para que el test lea los prints al instante
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    # 1. Iniciar NodoD
    print("Lanzando NodoD...")
    proc_d = subprocess.Popen([sys.executable, "Hit6\\NodoD.py"], env=env)
    time.sleep(2)

    try:
        # 2. Iniciar NodoC_1 (Alfa)
        print("Lanzando NodoC_1...")
        proc_c1 = subprocess.Popen([sys.executable, "Hit6\\NodoC.py", "127.0.0.1", "5000", "Nodo_Alfa"], env=env)
        time.sleep(2)

        # 3. Iniciar NodoC_2 (Beta) y capturar su salida
        print("Lanzando NodoC_2...")
        # Usamos PIPE para poder leer lo que Nodo_Beta imprime en consola
        proc_c2 = subprocess.Popen(
            [sys.executable, "Hit6\\NodoC.py", "127.0.0.1", "5000", "Nodo_Beta"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )

        # 4. Esperar a que ocurra el intercambio
        print("Esperando intercambio de mensajes (5 segundos)...")
        time.sleep(5)

        # 5. Verificación Automática
        print("\n--- Verificando Resultados ---")
        
        # Validar registro en NodoD
        res_d = requests.get("http://127.0.0.1:5000/Health")
        nodos_registrados = res_d.json().get("nodos", 0) if res_d.status_code == 200 else 0
        
        # Validar comunicación P2P leyendo la consola de Nodo_Beta
        # Nota: terminate() es necesario antes de leer si el proceso es infinito
        proc_c2.terminate()
        stdout_beta, _ = proc_c2.communicate()

        registro_ok = nodos_registrados == 2
        comunicacion_ok = "Respuesta de" in stdout_beta and "Saludo recibido" in stdout_beta

        if registro_ok:
            print("[CONTEO] OK: 2 nodos registrados.")
        else:
            print(f"[CONTEO] ERROR: Se esperaban 2 nodos, hay {nodos_registrados}.")

        if comunicacion_ok:
            print("[P2P] OK: Nodo_Beta recibió respuesta de Nodo_Alfa.")
        else:
            print("[P2P] ERROR: No se detectó el intercambio de mensajes en los logs.")

        # Veredicto Final
        print("\n--------------------------------------")
        if registro_ok and comunicacion_ok:
            print("RESULTADO DEL TEST: FUNCIONÓ")
        else:
            print("RESULTADO DEL TEST: FALLÓ")
        print("--------------------------------------")

    except Exception as e:
        print(f"Error durante el test: {e}")
    finally:
        # Limpieza total de procesos
        try: proc_c1.terminate() 
        except: pass
        try: proc_c2.terminate() 
        except: pass
        try: proc_d.terminate() 
        except: pass
        print("Procesos cerrados.")

if __name__ == "__main__":
    run_test()