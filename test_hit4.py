def test_main_comunicacion(capfd):
    import threading
    import time
    from Hit4.ClienteServidor import main

    ip = "127.0.0.1"

    t1 = threading.Thread(target=main, args=("A", ip, 5001, ip, 5002, 1))
    t2 = threading.Thread(target=main, args=("B", ip, 5002, ip, 5001, 1))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    time.sleep(0.2)  # 🔥 IMPORTANTE

    salida = capfd.readouterr().out

    assert "Mensaje recibido en nodo A" in salida
    assert "Mensaje recibido en nodo B" in salida