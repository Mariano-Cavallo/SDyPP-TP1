import time
import socket ,json
import requests , sys
import threading


ip_serverD = sys.argv[1]
puerto_serverD = int(sys.argv[2])
nombre_nodo = sys.argv[3]


url = f"http://{ip_serverD}:{puerto_serverD}/Register"



def saludar_pares(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))

        mensaje = {
            "tipo": "saludos",
            "mensaje": f"Hola desde nodo {nombre_nodo}"
        }

        s.sendall(json.dumps(mensaje).encode())

        response = s.recv(1024)

        if response:
            print("Respuesta de", ip, port, json.loads(response.decode()))
        s.close()


    except Exception as e:
        print(f"Error al saludar al par {ip}:{port} - {e}")

def servidor(sock):

    print("Nodo escuchando en", sock.getsockname())

    while True:
        conn, addr = sock.accept()
        try:
            data = conn.recv(1024)

            if data:
                msg = json.loads(data.decode())
                print("Mensaje recibido:", msg)

                response = {
                    "tipo": "respuesta",
                    "mensaje": "Saludo recibido"
                }

                conn.sendall(json.dumps(response).encode())

        except:
            pass

        finally:
            conn.close()


def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 0))

    ip_escucha, puerto_escucha = server_socket.getsockname()

    server_socket.listen(5)

    thread = threading.Thread(target=servidor, args=(server_socket,))
    thread.daemon = True
    thread.start()

    datos = {
        "ip": ip_escucha,
        "port": puerto_escucha
    }
    try:
        respuesta = requests.post(url, json=datos)
        if respuesta.status_code == 200:
            print("Nodo registrado exitosamente")
            data = respuesta.json()
            nodos = data.get("pares", [])
            print("Pares actuales en el nodo D:", nodos)
        else:
            print(f"Error al registrar el nodo: {respuesta.status_code}")

        for nodo in nodos:
            saludar_pares(nodo["ip"], nodo["port"])
    
    except Exception as e:
        print(f"Error de conexión con NodoD: {e}")

    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()