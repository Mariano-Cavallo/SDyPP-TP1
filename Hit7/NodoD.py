
import socket
import time
from datetime import datetime
import pickle
import threading
from flask import Flask, jsonify, request

app = Flask(__name__)

ip_server= input("Ingrese la IP en la cual va a recibir inscripciones el administrador: ")
puerto_server = int(input("Ingrese el puerto en el cual va a recibir inscripciones el administrador: "))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_server, puerto_server))
lista_espera = []
lista_inscriptos = []
actualizacion = threading.Condition()


def escuchar_inscripciones():
    server.listen()
    while True:
        cliente, cliente_ip = server.accept()
        print("Conexion con cliente aceptada!")
        hilo_receptor_inscripciones = threading.Thread(target= recepcion_socket, args=(cliente,))
        hilo_receptor_inscripciones.start()


def recepcion_socket(cliente):
    datos = cliente.recv(1024)
    ip_lista, puerto = pickle.loads(datos)        
    print(f"IP cliente:{ip_lista}\n Puerto cliente:{puerto}")
    socket = {
        "Nodo" : f"Nodo numero {len(lista_espera)+1}",
        "Ip" : ip_lista,
        "Puerto":puerto,
        "Horario de solicitud": datetime.now().strftime("%H:%M:%S")
    }
    lista_espera.append(socket)
    mensaje="Solicitud de inscripcion recibida, vas a ser inscripto en la proxima ventana de inscripcion (cuando comience el proximo minuto)."
    cliente.send(mensaje.encode())    
    aviso_actualizacion(cliente)


def aviso_actualizacion(cliente):
    ##while True:
    with actualizacion:
        actualizacion.wait()##Espera a que se actualice la lista de inscriptos
    mensaje = "Se actualizo la lista de inscriptos, ya esta inscripto!"
    paquete = (mensaje, lista_inscriptos)
    cliente.send(pickle.dumps(paquete))




def actualizar_inscriptos():
    while True:
        lista_inscriptos.clear()
        for n in lista_espera:
            lista_inscriptos.append(n)
        lista_espera.clear()   
        with actualizacion:
            actualizacion.notify_all() ##Notifica a todos los hilos que se actualizaron los inscriptos
        time.sleep(60)


    
##VER LO QUE LE PREGUNTE A CHAT GPT LO DEL TIEMPO, DESPUES DE ESO YA SE TERMINA EL EJER


def sincronizar_inicio_minuto():
    ahora = datetime.now() ##La variable ahora tiene el tiempo actual
    segundos_restantes= 60-ahora.second ## segundos_restantes tiene los segundos que faltan para el proximo minuto
    time.sleep(segundos_restantes)
    actualizar_inscriptos()


@app.route("/inscriptos", methods=["GET"])##Le indica al servidor flask que funcion ejecutar al recibir una peticion http de tip GET
def obtener_inscriptos():
    hora_actual = datetime.now().strftime("%H:%M:%S")
    return jsonify({
        f"Inscriptos a las {hora_actual}":f"{lista_inscriptos}",
    })



if __name__=="__main__":
    hilo_flask = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000, "debug": False})
    hilo_flask.start()



hilo_manejo_inscriptos = threading.Thread(target=sincronizar_inicio_minuto, args=())
hilo_manejo_inscriptos.start()
escuchar_inscripciones()

