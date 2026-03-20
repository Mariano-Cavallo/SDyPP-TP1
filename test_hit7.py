import subprocess
import sys
import time
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_nodo(script):
    path = os.path.join(BASE_DIR, script)

    return subprocess.Popen(
        [sys.executable, "-u", path],  # 🔥 sin buffer
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )


def test_sistema_inscripciones():
    ip = "127.0.0.1"
    puerto = "5000"

    # ------------------------
    # Nodo D
    # ------------------------
    nodo_d = run_nodo("Hit7/NodoD.py")
    nodo_d.stdin.write(ip + "\n")
    nodo_d.stdin.write(puerto + "\n")
    nodo_d.stdin.flush()

    time.sleep(2)

    # ------------------------
    # Nodo C x2
    # ------------------------
    nodo_c1 = run_nodo("Hit7/NodoC.py")
    nodo_c2 = run_nodo("Hit7/NodoC.py")

    for nodo in [nodo_c1, nodo_c2]:
        nodo.stdin.write(ip + "\n")
        nodo.stdin.write(puerto + "\n")
        nodo.stdin.flush()

    # ⏳ esperar ejecución
    time.sleep(10)

    # ------------------------
    # 🔥 MATAR PROCESOS (CLAVE)
    # ------------------------
    nodo_d.kill()
    nodo_c1.kill()
    nodo_c2.kill()

    time.sleep(1)  # deja que liberen buffers

    # ------------------------
    # AHORA SÍ LEER
    # ------------------------
    out = ""

    for proc in [nodo_d, nodo_c1, nodo_c2]:
        try:
            out += proc.stdout.read()
        except:
            pass

    print("\n--- OUTPUT ---\n", out)

    # ------------------------
    # ASSERTS
    # ------------------------
    assert "Solicitud de inscripcion recibida" in out
    assert "Se actualizo la lista de inscriptos" in out
    assert "Hola Server, soy el cliente" in out
    assert "Hola cliente, soy el Server" in out