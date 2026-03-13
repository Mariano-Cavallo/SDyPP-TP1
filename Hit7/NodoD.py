import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading

current_nodes = []
next_nodes = []

start_time = time.time()
window_start = int(time.time() // 60) * 60

FILE = "inscripciones.json"


def save_state():
    data = {
        "timestamp": time.time(),
        "current_nodes": current_nodes,
        "next_nodes": next_nodes
    }

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def window_manager():
    global current_nodes, next_nodes, window_start

    while True:
        time.sleep(60)

        print("Cambio de ventana")

        current_nodes = next_nodes
        next_nodes = []

        window_start = int(time.time() // 60) * 60

        save_state()


class Handler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_GET(self):

        if self.path == "/health":

            uptime = time.time() - start_time

            response = {
                "status": "ok",
                "current_window_start": window_start,
                "active_nodes": len(current_nodes)
            }

            self._set_headers()
            self.wfile.write(json.dumps(response).encode())

        if self.path == "/peers":

            response = {
                "peers": current_nodes
            }

            self._set_headers()
            self.wfile.write(json.dumps(response).encode())

    def do_POST(self):

        if self.path == "/register":

            global next_nodes

            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)

            node = json.loads(body.decode())

            new_node = {
                "ip": node["ip"],
                "port": node["port"]
            }

            peers = current_nodes.copy()

            next_nodes.append(new_node)

            print("Nodo registrado para próxima ventana:", new_node)

            save_state()

            response = {
                "peers": peers
            }

            self._set_headers()
            self.wfile.write(json.dumps(response).encode())


def run():

    thread = threading.Thread(target=window_manager, daemon=True)
    thread.start()

    server = HTTPServer(("0.0.0.0", 8000), Handler)

    print("Nodo D corriendo en puerto 8000")

    server.serve_forever()


if __name__ == "__main__":
    run()