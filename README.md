# RIPworx

El sitio de RIPworx: juegos para computadoras retro, hechos en Asunción, Paraguay. Se publica con
GitHub Pages en <https://czayas.github.io/ripworx/>.

Tiene dos juegos para Commodore 64: **Pothole Rush** (versión de prueba 11c, solo PAL) y
**Jumping Jim** (versión 1.1.0, PAL, NTSC y PAL-N; port del juego de roman126 para la ZX
Spectrum Next, con su permiso).

## Qué hay

| Ruta | Qué es |
|---|---|
| `index.html` | El inicio de RIPworx, con la lista de juegos. |
| `potholerush/index.html` | La página de Pothole Rush. |
| `potholerush/img/` | Capturas de la C64, el video de una partida, los sprites y la tapa. |
| `jumpingjim/index.html` | La página de Jumping Jim. |
| `jumpingjim/img/` | La ilustración de Carlos para la portada (`portada.webp`, `portada-og.jpg`), los ocho niveles, el título, los récords y el video. El logo arcoíris (`logo.png`) y el cielo del nivel 1 (`fondo.png`) quedan guardados, sin usar por ahora. |
| `herramientas/jumpingjim-capturas.py` | Saca de VICE las capturas y el video de Jumping Jim. |
| `descargas/` | Los zip para descargar: el de Pothole Rush (`.d64`, `.prg`, los manuales, un `LEAME-README.txt` y la licencia CC BY-NC-ND 4.0 en `LICENCIA-LICENSE.txt`) y el de Jumping Jim (copia del de `czayas/jumpingjim/releases/`). |
| `estilo.css` | El estilo común, onda Activision clásica: portada de color con el título en Raleway Black y la ilustración, y recuadros de borde grueso como en el manual de Pothole Rush. Cada página tiene su color: violeta Pothole Rush, verde Jumping Jim (el del borde de su ilustración) y azul marino el inicio. |
| `ver-sitio.py` | Muestra el sitio en la PC: servidor local y una pestaña del navegador (ver abajo). |
| `idioma.js` | Español o inglés: el que eligió el visitante; si no eligió, el de su navegador (español si está en español, si no, inglés). Sin JavaScript se ve en inglés. |
| `fuentes/` | Raleway Black y TeX Gyre Adventor en WOFF2 (licencias en `fuentes/LICENCIAS.md` y `OFL-Raleway.txt`). |
| `img/` | Los logotipos de RIPworx (blanco y violeta), el ícono y las miniaturas de las tarjetas del inicio. |

Los textos están en los dos idiomas en el mismo HTML: cada uno va con `lang="es"` o `lang="en"`
y el CSS muestra solo el elegido.

## Cómo se actualiza

El zip, las capturas y el video se arman desde el repositorio del juego (`czayas/potholerush`):

```bash
tools/sitio/preparar.sh ../ripworx 11c      # la versión va en el nombre del zip
```

El texto de la página se edita a mano en `potholerush/index.html` (los dos idiomas juntos). Si
cambia la versión, hay que cambiar también el enlace del zip y el texto que dice la versión.

Jumping Jim: el zip se copia tal cual de `releases/` del repositorio `czayas/jumpingjim`, y las
capturas salen de `herramientas/jumpingjim-capturas.py`.

## Ver la página en la PC antes de publicar

```bash
cd ripworx
python3 ver-sitio.py          # arranca el servidor y abre el sitio en el navegador
```

`ver-sitio.py` sirve esta carpeta en `http://localhost:8000/` (si el puerto está ocupado, usa
el siguiente libre; se puede elegir otro: `python3 ver-sitio.py 8080`) y abre una pestaña en el
navegador predeterminado. Al presionar cualquier tecla en la consola, cierra el servidor.
Con `--red` también se puede abrir desde otro equipo de la misma red (por ejemplo, un celular
conectado al mismo Wi-Fi): muestra la dirección para escribir en ese navegador. Funciona en
Linux, macOS y Windows, solo con Python 3.

## Publicar

Con una cuenta gratuita de GitHub, Pages solo publica desde repositorios públicos. Cuando la
página esté lista: Settings → General → Change visibility (público) y Settings → Pages → Deploy
from a branch → `main`, carpeta `/ (root)`.
