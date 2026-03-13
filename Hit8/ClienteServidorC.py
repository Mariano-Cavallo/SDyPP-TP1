import grpc
from concurrent import futures
import time
import threading
import sys

import comunicacion_pb2
import comunicacion_pb2_grpc


listen_ip = sys.argv[1]
listen_port = sys.argv[2]
remote_ip = sys.argv[3]
remote_port = sys.argv[4]
nombre = sys.argv[5]


# ------------------------
# SERVIDOR gRPC
# ------------------------

class NodoService(comunicacion_pb2_grpc.NodoServiceServicer):

    def EnviarMensaje(self, request, context):

        print("[SERVIDOR] Mensaje recibido:")
        print("Origen:", request.origen)
        print("Mensaje:", request.mensaje)

        respuesta = comunicacion_pb2.Respuesta(
            mensaje="Saludo recibido",
            origen=request.origen
        )

        return respuesta


def servidor():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    comunicacion_pb2_grpc.add_NodoServiceServicer_to_server(
        NodoService(), server
    )

    server.add_insecure_port(f"{listen_ip}:{listen_port}")
    server.start()

    print(f"[SERVIDOR] Escuchando en {listen_ip}:{listen_port}")

    server.wait_for_termination()


# ------------------------
# CLIENTE gRPC
# ------------------------

def cliente():

    while True:

        try:

            print(f"[CLIENTE] Conectando a {remote_ip}:{remote_port}")

            canal = grpc.insecure_channel(f"{remote_ip}:{remote_port}")
            stub = comunicacion_pb2_grpc.NodoServiceStub(canal)

            mensaje = comunicacion_pb2.Mensaje(
                origen=f"{listen_ip}:{listen_port}",
                mensaje=f"Hola desde nodo {nombre}"
            )

            respuesta = stub.EnviarMensaje(mensaje)

            print("[CLIENTE] Respuesta recibida:")
            print(respuesta)

            time.sleep(5)

        except Exception:

            print("[CLIENTE] No se pudo conectar. Reintentando...")
            time.sleep(3)


# ------------------------
# MAIN
# ------------------------

thread_servidor = threading.Thread(target=servidor)
thread_cliente = threading.Thread(target=cliente)

thread_servidor.start()
thread_cliente.start()

thread_servidor.join()
thread_cliente.join()