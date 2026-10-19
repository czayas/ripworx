#!/usr/bin/env python3
# Capturas de Jumping Jim (v1.1.0) para jumpingjim/img/: la versión de demostración del juego
# (TEST=7, piloto automático; PROMO, el título 5 s) empezando en cada nivel.
# Uso: herramientas/jumpingjim-capturas.py niveles|video, con el repositorio czayas/jumpingjim
# en JJ (variable de entorno, por defecto ../jumpingjim), ACME y VICE (x64sc, xvfb-run).
# Los cuadros elegidos para el sitio: el título, c00300 de nivel1; cada nivel, la captura
# número 14 (segundo 14); el video, los segundos 8 a 26 del nivel 1, un cuadro de cada dos.
import os, subprocess, sys
RAIZ_JJ = os.environ.get('JJ', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'jumpingjim'))
sys.path.insert(0, os.path.join(RAIZ_JJ, 'tools'))
from vice_harness import Vice, load_labels
JJ = os.path.join(RAIZ_JJ, 'platforms', 'c64')
OUT = os.environ.get('SALIDA', 'capturas-jj')
os.makedirs(OUT, exist_ok=True)
def armar(nivel):
    prg = f'{OUT}/promo{nivel}.prg'; lbl = f'{OUT}/promo{nivel}.lbl'
    subprocess.run(['acme', '-f', 'cbm', '-DTEST=7', '-DPROMO=1', f'-DSTARTLEVEL={nivel}', f'-DSTARTBCD={nivel}',
                    '--vicelabels', lbl, '-o', prg, 'main.a'], cwd=JJ + '/src', check=True)
    return prg, lbl
def correr(nivel, cuadros, cada, nombre):
    prg, lbl = armar(nivel)
    lab = load_labels(lbl)
    d = f'{OUT}/{nombre}'; os.makedirs(d, exist_ok=True)
    with Vice(prg, video='pal') as v:
        v.start(lab['irq_top'])
        for f in range(cuadros):
            v.next_frame()
            if f % cada == 0:
                v.screenshot().save(f'{d}/c{f:05d}.png')
    print(nombre, 'listo')
modo = sys.argv[1]
if modo == 'niveles':
    for n in range(1, 9):
        correr(n, 50 * 22, 50, f'nivel{n}')
elif modo == 'video':
    correr(2, 50 * 30, 2, 'video')
