##gRPC es un protocolo de aplicacion que corre encima de TCP, por lo que levantar servidor, 
##inicializar ip+puerto de escucha en TCP, no lo hacemos directamente nosotros sino que lo 
##hacemos indirectamente mediante la libreria de gRPC. Es decir, se encarga esta ultima 
##de implementarlo

import grpc
import comunicacion_pb2
import comunicacion_pb2_grpc
import threading
from concurrent import futures ##paquete para concurrencia de alto nivel, futures es un submodulo del paquete que ejecuta tareas en paralelo (Threads) y maneja los resultados en objetos de tipo Future
import time
import statistics


class Servicer(comunicacion_pb2_grpc.NodoServiceServicer):##Hereda de NodoServiceServicer
    def EnviarMensaje(self, request, context):
        print (f"{request}")
        return comunicacion_pb2.Respuesta(
            mensaje= "Hola cliente",
            origen = "Server gRPC"
        )

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) ##Equivalente a crear el servidor en la libreria de socket
    server.add_insecure_port(f"{ip_escucha}:{puerto_escucha}")##Equivalente a bind en la libreria de socket
    comunicacion_pb2_grpc.add_NodoServiceServicer_to_server(Servicer(), server)
    server.start()##Equivalente a .listen() en socket, se pone el server en escucha
    server.wait_for_termination()##Mantiene el hilo_servidor vivo mientras el server siga corriendo

ip_escucha = input("Ingrese la IP en la que va a escuchar el servidor gRPC: ")
puerto_escucha = int(input("Ingrese el puerto en el que va a escuchar el servidor gRPC: "))
hilo_server= threading.Thread(target=server, args=())
hilo_server.daemon = True
print(f"Voy a escuchar en {ip_escucha}:{puerto_escucha}")
hilo_server.start()
print("Servidor iniciado")
ip_remota = input("Ingrese la IP del servidor gRPC al cual desea saludar: ")
puerto_remoto = int(input("Ingrese el puerto del servidor gRPC al cual desea saludar: "))
rondas = int(input("Ingrese cantidad de rondas para medir: "))





def cliente():
    canal = grpc.insecure_channel(f"{ip_remota}:{puerto_remoto}")##Equivalente a cliente .connect() en socket
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
        respuesta_server = cliente_stub.EnviarMensaje(request)
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
        print("\n===== RESUMEN PROTOBUF (Hit9) =====")
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
hilo_server.join()

