from flask import Flask,request, jsonify


app = Flask(__name__)

nodes = []  

@app.route('/Health', methods=['GET'])
def get_status():
    cantidad_nodos = len(nodes)
    return jsonify({"status": "active",
                     "code": 200,
                     "nodos": cantidad_nodos})

@app.route('/Register', methods=['POST'])
def post_ip():
    data = request.get_json()
    ip = data.get("ip")
    port = data.get("port")

    if ip and port:
        new_node = {"ip": ip, "port": port}
        pares = nodes.copy()  
        nodes.append(new_node)
        return jsonify({"mensaje": "Nodo registrado exitosamente",
                        "pares": pares}), 200
    else:
        return jsonify({"mensaje": "Datos inválidos"}), 400



if __name__ == '__main__':
    app.run(port=5000)