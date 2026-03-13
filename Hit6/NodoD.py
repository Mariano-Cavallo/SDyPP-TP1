import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

nodes = []
start_time = time.time()


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
                "registered_nodes": len(nodes),
                "uptime_seconds": uptime
            }

            self._set_headers()
            self.wfile.write(json.dumps(response).encode())

    def do_POST(self):

        if self.path == "/register":

            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)

            node = json.loads(body.decode())

            ip = node["ip"]
            port = node["port"]

            new_node = {"ip": ip, "port": port}

            # obtener nodos existentes antes de agregar el nuevo
            peers = nodes.copy()

            nodes.append(new_node)

            response = {
                "peers": peers
            }

            self._set_headers()
            self.wfile.write(json.dumps(response).encode())


def run():
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("Nodo D corriendo en puerto 8000")
    server.serve_forever()


if __name__ == "__main__":
    run()