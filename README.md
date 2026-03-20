# Grupo La 25

Integrantes:
- AIMALE VALENTINO
- CAVALLO SASSI MARIANO
- MARINO LAUTARO

## Estructura del TP
Cada hit está en su carpeta `Hit1`, `Hit2`, ..., `Hit8`. Este README describe qué hace cada hit y cómo correrlo.

---

## Hit1: Cliente A <-> Servidor B (TCP básico)

### Cómo funciona
1. `ServerB.py` crea un socket TCP, hace `bind` y `listen` en el puerto 5000.
2. Espera una conexión, recibe un mensaje y responde con "Hola A, soy B. Saludo recibido.".
3. `ClienteA.py` se conecta al servidor, envía un saludo y muestra la respuesta.

### Ejecución
1. En una terminal: `python Hit1/ServerB.py`
2. En otra terminal: `python Hit1/ClienteA.py`


## Hit2: Cliente con reconexión automática

### Cómo funciona
1. `ServerB.py` es igual a Hit1 con TCP escuchando y respondiendo.
2. `ClienteA.py` intenta reconectar continuamente a `127.0.0.1:5000`.
3. Si la conexión falla, duerme 5 segundos y vuelve a intentar.

### Ejecución
1. Iniciar servidor: `python Hit2/ServerB.py`
2. Iniciar cliente: `python Hit2/ClienteA.py`
3. Para probar reconexión: detener servidor y reiniciarlo; el cliente se reconectará.


## Hit3: Cliente y servidor de ejemplo TCP con reconexión visual

### Cómo funciona
1. `ServerB.py` gestiona una conexión y responde con un saludo.
2. `ClienteA.py` se conecta, envía saludo y recibe respuesta.
3. Tiene reintento al detectar que la conexión se perdió.

### Ejecución
1. `python Hit3/ServerB.py`
2. `python Hit3/ClienteA.py`

---

## Hit4: Nodo C con servidor y cliente TCP en threads

### Cómo funciona
1. El script lee `listen_ip`, `listen_port`, `remote_ip`, `remote_port` desde `sys.argv`.
2. Crea un thread servidor que acepta conexiones y envía respuesta.
3. Crea un thread cliente que se conecta periódicamente al nodo remoto y envía saludos.

### Ejecución
`python Hit4/ClienteServidor.py nombre_nodo ip_origen puerto_origen ip_remota puerto_remoto y numero de rondas`

---

## Hit5: Mensajes JSON entre nodos (serialización)

### Cómo funciona
1. Mismo enfoque dual (servidor + cliente) con threads.
2. En cliente, envía JSON con `origen` y `mensaje`.
3. Servidor parsea JSON y responde con JSON estructurado.

### Ejecución
`python Hit5/ClienteServidorC.py nombre ip_origen puerto_origen ip_remota puerto_remoto y numero de rondas`

---

## Hit6: Registro de pares usando HTTP y saludo TCP

### Cómo funciona
1. `NodoD.py` crea un servicio HTTP en `8000` con rutas `/register` y `/health`.
2. `NodoC.py` inicia servidor TCP en puerto aleatorio y se registra en `NodoD` con `requests.post`.
3. `NodoD` devuelve pares registrados; `NodoC` saluda a cada uno por TCP.

### Ejecución
1. Iniciar regitro: `python Hit6/NodoD.py`
2. Iniciar nodo C: `python Hit6/NodoC.py 127.0.0.1 5000`

---

## Hit7: Ventanas temporales de nodos con registro y pares

### Cómo funciona
1. `NodoD.py` maneja registro en `/register`, y retorna pares de la ventana actual.
2. Mantiene `current_nodes` y `next_nodes`; cambia ventana cada 60s.
3. `NodoC.py` registra su IP/puerto y saluda a pares en cada ejecución.

### Ejecución
1. `python Hit7/NodoD.py`
2. `python Hit7/NodoC.py 127.0.0.1 8000`

---

## Hit8: Comunicación gRPC bidireccional (nodos con servicio y cliente)

### Cómo funciona
1. `comunicacion.proto` define un `NodoService` con RPC `EnviarMensaje`.
2. `ClienteServidorC.py` arranca un servidor gRPC y un cliente en threads.
3. Cliente envía `Mensaje` y recibe `Respuesta` con gRPC.


## Dependencias
Instalar con pip:

```bash
pip install grpcio grpcio-tools requests
```



