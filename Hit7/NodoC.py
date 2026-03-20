import socket
import pickle
import threading

ip_remota=input("Ingrese la IP remota del Administrador al cual desea solicitarle la inscripcion:")
puerto_remoto = int(input("Ingrese el puerto remoto del Administrador al cual desea solicitarle la inscripcion:"))

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 0))
ip_escucha, puerto_escucha= server.getsockname()


def notificacion_actualizacion_inscriptos():
    mensaje , lista_inscriptos = pickle.loads(cliente.recv(1024))
    print(f"{mensaje}\n")
    print("Lista de inscriptos: \n")
    for n in lista_inscriptos:
        print(n)
        ip=n.get("Ip")
        puerto = n.get("Puerto")
<<<<<<< HEAD
        if (ip,puerto) != (ip_escucha,puerto_escucha):
            hilo_saludo_server = threading.Thread(target=saludar_server, args=(ip,puerto,))
            hilo_saludo_server.start()
=======
        print(f"{ip}:{puerto}")
        if (ip,puerto) != (ip_escucha,puerto_escucha):
            hilo_saludo_server = threading.Thread(target=saludar_server, args=(ip,puerto,))
            hilo_saludo_server.start()
            print("Hilo saludo iniciado")
>>>>>>> 4fa331874b5cff2c8e400073d12de8d19339b8b9
    cliente.close()    
            
   

def saludar_server(ip, puerto):
<<<<<<< HEAD
=======
    print("Hilo saludo_server intentando conectarse al par inscripto")
>>>>>>> 4fa331874b5cff2c8e400073d12de8d19339b8b9
    cliente_saludo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_saludo.connect((ip, puerto))
    cliente_saludo.send("Hola Server, soy el cliente".encode())
    respuesta = cliente_saludo.recv(1024).decode()
    print(respuesta)        


def intentar_conexion():
    cliente.connect((ip_remota, puerto_remoto))
    cliente.send(pickle.dumps((ip_escucha, puerto_escucha)))
    mensaje = cliente.recv(1024).decode()
    print(f"{mensaje}\n")
    notificacion_actualizacion_inscriptos()
    
    
def escuchar_saludos():
    server.listen()
<<<<<<< HEAD
    print(f"Server escuchando saludos en {ip_escucha}:{puerto_escucha}")
=======
    print("Server escuchando saludos")
>>>>>>> 4fa331874b5cff2c8e400073d12de8d19339b8b9
    while True:
        cliente, cliente_ip = server.accept()
        hilo_saludo = threading.Thread(target=recibir_saludo, args=(cliente,))
        hilo_saludo.start()

def recibir_saludo(cliente1):
    saludo = cliente1.recv(1024).decode()
    print(saludo)
    cliente1.send(f"Hola cliente, soy el Server con socket {ip_escucha}:{puerto_escucha}".encode())
    cliente1.close()
   
hilo_escucha=threading.Thread(target=escuchar_saludos, args=())
hilo_escucha.start()
intentar_conexion()