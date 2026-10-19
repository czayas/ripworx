# RIPworx

El sitio de RIPworx: juegos para computadoras retro, hechos en Asunción, Paraguay. Se publica con
GitHub Pages en <https://czayas.github.io/ripworx/>.

Por ahora tiene un juego: **Pothole Rush** para Commodore 64 (versión de prueba 11c, solo PAL).

## Qué hay

| Ruta | Qué es |
|---|---|
| `index.html` | El inicio de RIPworx, con la lista de juegos. |
| `potholerush/index.html` | La página de Pothole Rush. |
| `potholerush/img/` | Capturas de la C64, el video de una partida, los sprites y la tapa. |
| `descargas/` | El zip para descargar: `.d64`, `.prg`, los manuales en español y en inglés y un `LEAME-README.txt`. |
| `estilo.css` | El estilo común (la estética de la caja y del manual de Pothole Rush). |
| `idioma.js` | Español o inglés: el que eligió el visitante; si no eligió, el de su navegador (español si está en español, si no, inglés). Sin JavaScript se ve en inglés. |
| `fuentes/` | Raleway Black y TeX Gyre Adventor en WOFF2 (licencias en `fuentes/LICENCIAS.md` y `OFL-Raleway.txt`). |
| `img/` | Los logotipos de RIPworx (blanco y violeta), el ícono y la miniatura del inicio. |

Los textos están en los dos idiomas en el mismo HTML: cada uno va con `lang="es"` o `lang="en"`
y el CSS muestra solo el elegido.

## Cómo se actualiza

El zip, las capturas y el video se arman desde el repositorio del juego (`czayas/potholerush`):

```bash
tools/sitio/preparar.sh ../ripworx 11c      # la versión va en el nombre del zip
```

El texto de la página se edita a mano en `potholerush/index.html` (los dos idiomas juntos). Si
cambia la versión, hay que cambiar también el enlace del zip y el texto que dice la versión.

## Ver la página en la PC antes de publicar

```bash
cd ripworx
python3 -m http.server 8000      # y abrir http://localhost:8000 en el navegador
```

## Publicar

Con una cuenta gratuita de GitHub, Pages solo publica desde repositorios públicos. Cuando la
página esté lista: Settings → General → Change visibility (público) y Settings → Pages → Deploy
from a branch → `main`, carpeta `/ (root)`.
