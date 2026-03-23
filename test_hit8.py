
import os
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SCRIPT_HIT8 = BASE_DIR / "Hit8" / "ClienteServidorC.py"


def _start_node(name):
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    proc = subprocess.Popen(
        [sys.executable, "-u", str(SCRIPT_HIT8)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
        cwd=str(SCRIPT_HIT8.parent),
    )

    lines = []

    def _reader():
        for line in iter(proc.stdout.readline, ""):
            line = line.rstrip("\n")
            lines.append(line)
            print(f"[{name}] {line}", flush=True)

    t = threading.Thread(target=_reader, daemon=True)
    t.start()
    return proc, lines


def _send_lines(proc, values, name):
    for value in values:
        print(f"[TEST] Input a {name}: {value}", flush=True)
        proc.stdin.write(f"{value}\n")
    proc.stdin.flush()


def _wait_until(predicate, timeout=12, step=0.1):
    start = time.time()
    while time.time() - start < timeout:
        if predicate():
            return True
        time.sleep(step)
    return False


def _get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def test_saludo_bidireccional_grpc_hit8():
    print("[TEST] Iniciando prueba gRPC bidireccional Hit8", flush=True)
    port_a = _get_free_port()
    port_b = _get_free_port()
    while port_b == port_a:
        port_b = _get_free_port()

    nodo_a, out_a = _start_node("A")
    nodo_b, out_b = _start_node("B")

    try:
        _send_lines(nodo_a, ["127.0.0.1", str(port_a)], "A")
        _send_lines(nodo_b, ["127.0.0.1", str(port_b)], "B")

        ok_a_server = _wait_until(lambda: any("Servidor iniciado" in ln for ln in out_a), timeout=10)
        ok_b_server = _wait_until(lambda: any("Servidor iniciado" in ln for ln in out_b), timeout=10)
        print(f"[TEST] Servidor A iniciado: {ok_a_server}", flush=True)
        print(f"[TEST] Servidor B iniciado: {ok_b_server}", flush=True)

        assert ok_a_server and ok_b_server, "No iniciaron ambos servidores gRPC"

        _send_lines(nodo_a, ["127.0.0.1", str(port_b), "1"], "A")
        _send_lines(nodo_b, ["127.0.0.1", str(port_a), "1"], "B")

        ok_a_resp = _wait_until(lambda: any("[RESPUESTA PROTOBUF]" in ln for ln in out_a), timeout=15)
        ok_b_resp = _wait_until(lambda: any("[RESPUESTA PROTOBUF]" in ln for ln in out_b), timeout=15)
        print(f"[TEST] Nodo A recibió respuesta: {ok_a_resp}", flush=True)
        print(f"[TEST] Nodo B recibió respuesta: {ok_b_resp}", flush=True)

        assert ok_a_resp and ok_b_resp, "No hubo respuesta gRPC en ambos nodos"
        assert any("Hola Server" in ln for ln in out_a), "Nodo A no recibió saludo del nodo B"
        assert any("Hola Server" in ln for ln in out_b), "Nodo B no recibió saludo del nodo A"
        assert not any("Traceback" in ln for ln in out_a), "Nodo A tuvo una excepción"
        assert not any("Traceback" in ln for ln in out_b), "Nodo B tuvo una excepción"
        print("[TEST] OK: ambos nodos se saludaron por gRPC", flush=True)

    finally:
        print("[TEST] Cerrando procesos", flush=True)
        for proc in (nodo_a, nodo_b):
            if proc.poll() is None:
                proc.kill()
        for proc in (nodo_a, nodo_b):
            proc.wait(timeout=5)


if __name__ == "__main__":
    test_saludo_bidireccional_grpc_hit8()