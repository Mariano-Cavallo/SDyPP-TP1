def test_main_json(capfd):
    import threading
    import time
    from Hit5.ClienteServidor import main

    ip = "127.0.0.1"

    t1 = threading.Thread(target=main, args=("A", ip, 5003, ip, 5004, 1))
    t2 = threading.Thread(target=main, args=("B", ip, 5004, ip, 5003, 1))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    time.sleep(0.2)  

    salida = capfd.readouterr().out

    assert "Mensaje recibido en nodo A" in salida
    assert "Mensaje recibido en nodo B" in salida

    assert "'nombre': 'A'" in salida
    assert "'nombre': 'B'" in salida
    assert "'mesnaje': 'Hola'" in salida