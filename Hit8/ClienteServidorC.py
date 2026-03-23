##gRPC es un protocolo de aplicacion que corre encima de TCP, por lo que levantar servidor, 
##inicializar ip+puerto de escucha en TCP, no lo hacemos directamente nosotros sino que lo 
##hacemos indirectamente mediante la libreria de gRPC. Es decir, se encarga esta ultima 
##de implementarlo

import grpc
import signal
import sys
import threading
from concurrent import futures ##paquete para concurrencia de alto nivel, futures es un submodulo del paquete que ejecuta tareas en paralelo (Threads) y maneja los resultados en objetos de tipo Future
import time
import statistics
import comunicacion_pb2
import comunicacion_pb2_grpc
"""
try:
    import comunicacion_pb2
    import comunicacion_pb2_grpc
except ModuleNotFoundError:
    # Fallback para ejecucion desde raiz del repo (CI/Linux)
    from Hit8 import comunicacion_pb2
    from Hit8 import comunicacion_pb2_grpc
"""

server = None  # referencia global al servidor gRPC para poder detenerlo

class Servicer(comunicacion_pb2_grpc.NodoServiceServicer):##Hereda de NodoServiceServicer
    def EnviarMensaje(self, request, context):
        print (f"{request}")
        return comunicacion_pb2.Respuesta(
            mensaje= "Hola cliente",
            origen = "Server gRPC"
        )

def servidor():
    global server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) ##Equivalente a crear el servidor en la libreria de socket
    server.add_insecure_port(f"{ip_escucha}:{puerto_escucha}")##Equivalente a bind en la libreria de socket
    comunicacion_pb2_grpc.add_NodoServiceServicer_to_server(Servicer(), server)
    server.start()##Equivalente a .listen() en socket, se pone el server en escucha
    print("Servidor iniciado", flush=True)  # se imprime DESPUES de .start() para garantizar que el puerto ya esta escuchando
    server.wait_for_termination()##Mantiene el hilo_servidor vivo mientras el server siga corriendo

if len(sys.argv) == 6:
    ip_escucha = sys.argv[1]
    puerto_escucha = int(sys.argv[2])
    ip_remota = sys.argv[3]
    puerto_remoto = int(sys.argv[4])
    rondas = int(sys.argv[5])
else:
    ip_escucha = input("Ingrese la IP en la que va a escuchar el servidor gRPC: ")
    puerto_escucha = int(input("Ingrese el puerto en el que va a escuchar el servidor gRPC: "))

def _detener_servidor(signum=None, frame=None):
    if server:
        server.stop(0)

signal.signal(signal.SIGTERM, _detener_servidor)

hilo_server = threading.Thread(target=servidor, args=())  # NO daemon: el proceso debe vivir mientras el servidor este activo
print(f"Voy a escuchar en {ip_escucha}:{puerto_escucha}")
hilo_server.start()
if len(sys.argv) != 6:
    ip_remota = input("Ingrese la IP del servidor gRPC al cual desea saludar: ")
    puerto_remoto = int(input("Ingrese el puerto del servidor gRPC al cual desea saludar: "))
    rondas = int(input("Ingrese cantidad de rondas para medir: "))





def cliente():
    destino = f"{ip_remota}:{puerto_remoto}"

    # Crea un canal nuevo en cada intento: reusar el mismo canal en estado
    # TRANSIENT_FAILURE puede hacer que gRPC no reintente la conexion correctamente.
    canal = None
    while True:
        if canal:
            canal.close()
        canal = grpc.insecure_channel(destino)##Equivalente a cliente .connect() en socket
        try:
            grpc.channel_ready_future(canal).result(timeout=2)
            print(f"Canal gRPC listo contra {destino}", flush=True)
            break
        except grpc.FutureTimeoutError:
            print(f"Servidor remoto {destino} aun no disponible. Reintentando en 1s...", flush=True)
            time.sleep(1)

    cliente_stub = comunicacion_pb2_grpc.NodoServiceStub(canal)

    latencias = []
    bytes_salida = []
    bytes_respuesta = []

    for i in range(rondas):
        request = comunicacion_pb2.Mensaje(
            mensaje="Hola Server",
            origen="Cliente gRPC"
        )

        request_bytes = request.SerializeToString()
        tamanio_request = len(request_bytes)

        inicio = time.perf_counter()
        respuesta_server = cliente_stub.EnviarMensaje(request, wait_for_ready=True)
        fin = time.perf_counter()

        respuesta_bytes = respuesta_server.SerializeToString()
        tamanio_respuesta = len(respuesta_bytes)
        latencia_ms = (fin - inicio) * 1000

        latencias.append(latencia_ms)
        bytes_salida.append(tamanio_request)
        bytes_respuesta.append(tamanio_respuesta)

        print(f"[METRICA PROTOBUF] ronda={i + 1} bytes_salida={tamanio_request} bytes_respuesta={tamanio_respuesta} latencia_ms={latencia_ms:.3f}")
        print(f"[RESPUESTA PROTOBUF] {respuesta_server}")

    if latencias:
        print("\n===== RESUMEN PROTOBUF (Hit8) =====")
        print(f"Mensajes medidos: {len(latencias)}")
        print(
            f"Latencia ms -> min={min(latencias):.3f} "
            f"prom={statistics.mean(latencias):.3f} max={max(latencias):.3f}"
        )
        print(
            f"Bytes salida -> min={min(bytes_salida)} "
            f"prom={statistics.mean(bytes_salida):.2f} max={max(bytes_salida)}"
        )
        print(
            f"Bytes respuesta -> min={min(bytes_respuesta)} "
            f"prom={statistics.mean(bytes_respuesta):.2f} max={max(bytes_respuesta)}"
        )



hilo_cliente = threading.Thread(target = cliente, args=())
hilo_cliente.start()
hilo_cliente.join()

try:
    hilo_server.join()  # bloquea hasta que el servidor sea detenido (Ctrl+C o SIGTERM)
except KeyboardInterrupt:
    _detener_servidor()

