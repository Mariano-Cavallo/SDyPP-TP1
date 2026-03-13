import socket
import threading
import requests
import sys
import json
import time

registry_ip = sys.argv[1]
registry_port = sys.argv[2]

registry_url = f"http://{registry_ip}:{registry_port}/register"


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
                    "type": "reply",
                    "message": "Saludo recibido"
                }

                conn.send(json.dumps(response).encode())

        except:
            pass

        finally:
            conn.close()


def saludar_peer(ip, port):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))

        msg = {
            "type": "greeting",
            "message": "Hola desde nodo C"
        }

        s.send(json.dumps(msg).encode())

        response = s.recv(1024)

        if response:
            print("Respuesta de", ip, port, json.loads(response.decode()))

        s.close()

    except Exception as e:
        print("No se pudo conectar a", ip, port)


def main():

    # crear socket con puerto aleatorio
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 0))

    listen_ip, listen_port = server_socket.getsockname()

    server_socket.listen(5)

    # iniciar servidor en thread
    thread = threading.Thread(target=servidor, args=(server_socket,))
    thread.daemon = True
    thread.start()

    # registrar nodo en D
    register_data = {
        "ip": socket.gethostbyname(socket.gethostname()),
        "port": listen_port
    }

    response = requests.post(registry_url, json=register_data)

    peers = response.json()["peers"]

    print("Peers recibidos:", peers)

    # saludar a cada peer
    for peer in peers:
        saludar_peer(peer["ip"], peer["port"])

    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()