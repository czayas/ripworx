#!/usr/bin/env python3
"""
Muestra el sitio en la PC antes de publicarlo: arranca un servidor web local con esta carpeta,
abre la página en una pestaña del navegador predeterminado y espera. Al apretar cualquier tecla
en la consola, cierra el servidor.

Uso:  python3 ver-sitio.py [puerto]     (por defecto 8000; si está ocupado, prueba el siguiente)
      --red   también se puede abrir desde otros equipos de la misma red (por ejemplo, el
              celular): muestra la dirección que hay que escribir en el navegador.

Funciona en Linux, macOS y Windows, solo con Python 3 (sin nada que instalar).
"""
import functools
import http.server
import os
import socket
import sys
import threading
import webbrowser

AQUI = os.path.dirname(os.path.abspath(__file__))


class Silencioso(http.server.SimpleHTTPRequestHandler):
    """sirve los archivos sin escribir una línea por cada pedido"""
    def log_message(self, *args):
        pass


def ip_local():
    """la dirección de esta PC en la red local (para abrir el sitio desde el celular)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.168.0.1', 9))   # no se manda nada: solo elige la interfaz de salida
        return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        s.close()


def esperar_tecla():
    """espera una tecla cualquiera (sin necesidad de Enter)"""
    if os.name == 'nt':
        import msvcrt
        msvcrt.getwch()
        return
    import termios
    import tty
    fd = sys.stdin.fileno()
    if not os.isatty(fd):               # sin consola (por ejemplo, desde otro programa): Enter
        sys.stdin.readline()
        return
    antes = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, antes)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    red = '--red' in sys.argv
    puerto = int(args[0]) if args else 8000
    manejador = functools.partial(Silencioso, directory=AQUI)
    servidor = None
    for p in range(puerto, puerto + 20):
        try:
            servidor = http.server.ThreadingHTTPServer(('0.0.0.0' if red else '127.0.0.1', p), manejador)
            puerto = p
            break
        except OSError:
            continue
    if servidor is None:
        sys.exit(f'No encontré un puerto libre entre {puerto} y {puerto + 19}.')
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    url = f'http://localhost:{puerto}/'
    print(f'Sitio de RIPworx en {url}')
    if red:
        print(f'Desde otro equipo de la misma red: http://{ip_local()}:{puerto}/')
    webbrowser.open_new_tab(url)
    print('Presiona cualquier tecla para cerrar el servidor.')
    try:
        esperar_tecla()
    except KeyboardInterrupt:
        pass
    servidor.shutdown()
    servidor.server_close()
    print('Servidor cerrado.')


if __name__ == '__main__':
    main()
