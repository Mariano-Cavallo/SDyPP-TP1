import subprocess
import time
import sys

nodo_a = [
    "python", "-u", "Hit8/ClienteServidorC.py",
    "127.0.0.1", "50051",
    "127.0.0.1", "50052",
    "A"
]

nodo_b = [
    "python", "-u", "Hit8/ClienteServidorC.py",
    "127.0.0.1", "50052",
    "127.0.0.1", "50051",
    "B"
]

print("Iniciando nodos...")

proceso_a = subprocess.Popen(nodo_a, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
proceso_b = subprocess.Popen(nodo_b, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

time.sleep(12)

print("Cerrando nodos...")

proceso_a.kill()
proceso_b.kill()

out_a, err_a = proceso_a.communicate()
out_b, err_b = proceso_b.communicate()

print("---- Nodo A ----")
print(out_a)
print("---- Nodo B ----")
print(out_b)

ok_a = "Saludo recibido" in out_a
ok_b = "Saludo recibido" in out_b

if ok_a and ok_b:
    print("Test OK ")
    sys.exit(0)
else:
    print("Test FALLÓ ")
    sys.exit(1)