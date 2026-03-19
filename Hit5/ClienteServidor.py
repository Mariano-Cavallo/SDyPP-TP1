import socket
import time
import sys
import threading
import json
"""
En este programa necesito definir hilos, porque tanto cliente como servidor son operaciones bloqueantes, es decir
 no ejecutan otro proceso hasta que se haya determinado el estado de la conexion como exitoso o fallo, y al ser dos instancias
 de un mismo programa necesito el cliente y el servidor en dos hilos distintos

"""


def cliente(name,port,ip,loop_rouds):
    for i in range(loop_rouds):
        #conexion de socket

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))

        print("Conectado")

        #envio de mensaje con serializacion
        texto = {
                   "mesnaje": "Hola", 
                   "nombre": name
                   }
        mensaje = json.dumps(texto)
        client_socket.send(mensaje.encode())
        print("Saludo enviado")
        time.sleep(10)

        client_socket.close()
        


def servidor(name,port,ip,loop_rouds):
    #conexion del socket
     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     server_socket.bind((ip, port))
     server_socket.listen(5)

    #recibir el mensaje con deserializacion
     for i in range(loop_rouds):
        conn, addr = server_socket.accept()
        data = conn.recv(1024)
        if data:
            mensaje = json.loads(data.decode())
           
            print(f"Mensaje recibido en nodo {name}: {mensaje}")

        conn.close()



# ejecucion de programa
def main(name, mi_ip, mi_port, otro_ip, otro_port, loop_rouds):
    thread_servidor = threading.Thread(
        target=servidor,
        args=(name, mi_port, mi_ip, loop_rouds)
    )

    thread_cliente = threading.Thread(
        target=cliente,
        args=(name, otro_port, otro_ip, loop_rouds)
    )

    thread_servidor.start()
    time.sleep(1)
    thread_cliente.start()

    thread_servidor.join()
    thread_cliente.join()


# (solo para ejecución por consola)
if __name__ == "__main__":
    name = sys.argv[1]
    mi_ip = sys.argv[2]
    mi_port = int(sys.argv[3])
    otro_ip = sys.argv[4]
    otro_port = int(sys.argv[5])
    loop_rouds = int(sys.argv[6])

    main(name, mi_ip, mi_port, otro_ip, otro_port, loop_rouds)