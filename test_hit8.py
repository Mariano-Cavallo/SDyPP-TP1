import subprocess
import threading
import time
import sys

def reader(pipe, name, flag):
    for line in iter(pipe.readline, ''):
        print(f"[{name}] {line.strip()}")
        if "Saludo recibido" in line:
            flag["ok"] = True
    pipe.close()

def start_node(cmd, name, flag):
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    t = threading.Thread(target=reader, args=(p.stdout, name, flag))
    t.daemon = True
    t.start()

    return p

nodo_a = ["python", "-u", "Hit8/ClienteServidorC.py",
          "127.0.0.1", "50051", "127.0.0.1", "50052", "A"]

nodo_b = ["python", "-u", "Hit8/ClienteServidorC.py",
          "127.0.0.1", "50052", "127.0.0.1", "50051", "B"]

flag_a = {"ok": False}
flag_b = {"ok": False}

print("Iniciando nodos...")

pa = start_node(nodo_a, "A", flag_a)
pb = start_node(nodo_b, "B", flag_b)

timeout = 20
start = time.time()

while time.time() - start < timeout:
    if flag_a["ok"] and flag_b["ok"]:
        break
    time.sleep(0.5)

print("Cerrando nodos...")

pa.kill()
pb.kill()

pa.wait()
pb.wait()

assert flag_a["ok"] and flag_b["ok"], "Los nodos no se saludaron correctamente"