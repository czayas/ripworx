#!/usr/bin/env python3
"""
Arma las novedades del sitio a partir de noticias.json (en la raíz):
  - la sección NOVEDADES / NEWS del inicio (index.html, entre <!-- noticias:inicio --> y
    <!-- noticias:fin -->), con las últimas 5;
  - la página con todas: noticias/index.html;
  - los canales RSS: noticias.xml (en español) y news.xml (en inglés).
Uso: python3 herramientas/noticias.py      (sin nada que instalar)
"""
import datetime
import html
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = 'https://ripworx.dev/'
EN_INICIO = 5
PRODUCTOS = {'pr': ('Pothole Rush', 'potholerush/'), 'jj': ('Jumping Jim', 'jumpingjim/'),
             'rw': ('RIPworx', '')}
MESES_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DIAS_RFC = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

e = html.escape


def cargar():
    with open(os.path.join(RAIZ, 'noticias.json'), encoding='utf-8') as f:
        n = json.load(f)['noticias']
    return sorted(n, key=lambda x: x['fecha'], reverse=True)   # estable: el orden del archivo


def fecha_es(d):
    return f'{d.day:02d}/{d.month:02d}/{d.year}'


def fecha_en(d):
    return f'{MESES_EN[d.month - 1]} {d.day}, {d.year}'


def lista(noticias, prefijo):
    """la lista de noticias en HTML; prefijo: cómo llegar a la raíz desde la página ("" o "../")"""
    out = ['<ol class="noticias">']
    for n in noticias:
        d = datetime.date.fromisoformat(n['fecha'])
        nombre, pagina = PRODUCTOS[n['producto']]
        enlace = prefijo + n['enlace'] if n['enlace'] else (prefijo or './')
        out.append(f'  <li class="noticia {n["producto"]}">')
        out.append(f'    <p class="cabeza"><time datetime="{n["fecha"]}"><span lang="en">{fecha_en(d)}</span>'
                   f'<span lang="es">{fecha_es(d)}</span></time> '
                   f'<a class="etiqueta" href="{prefijo + pagina if pagina else (prefijo or "./")}">{nombre}</a></p>')
        for idioma in ('en', 'es'):
            t = n[idioma]
            out.append(f'    <p lang="{idioma}"><a class="titular" href="{enlace}">{e(t["titulo"])}</a> {e(t["texto"])}</p>')
        out.append('  </li>')
    out.append('</ol>')
    return '\n'.join(out)


def seccion_inicio(noticias):
    return '\n'.join([
        '<!-- noticias:inicio (lo escribe herramientas/noticias.py a partir de noticias.json: no editar a mano) -->',
        '<section class="recuadro" id="novedades">',
        '  <h2><span lang="en">NEWS</span><span lang="es">NOVEDADES</span></h2>',
        lista(noticias[:EN_INICIO], ''),
        '  <p class="mas-noticias"><a href="noticias/"><span lang="en">All news</span><span lang="es">Todas las novedades</span></a>'
        ' · <a href="news.xml" lang="en">RSS</a><a href="noticias.xml" lang="es">RSS</a></p>',
        '</section>',
        '<!-- noticias:fin -->'])


def pagina_archivo(noticias):
    return f'''<!doctype html>
<html lang="en" data-idioma="en"
      data-titulo-en="News · RIPworx"
      data-titulo-es="Novedades · RIPworx">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>News · RIPworx</title>
<meta name="description" content="News about RIPworx games for retro computers: new versions, machines and downloads.">
<link rel="icon" href="../img/icono.png">
<link rel="alternate" type="application/rss+xml" title="RIPworx news (English)" href="../news.xml">
<link rel="alternate" type="application/rss+xml" title="Novedades de RIPworx (español)" href="../noticias.xml">
<link rel="stylesheet" href="../estilo.css?v={VERSION_ESTILO}">
<script src="../idioma.js"></script>
</head>
<body class="inicio-pag">
<!-- página escrita por herramientas/noticias.py a partir de noticias.json: no editar a mano -->

<header class="inicio corto">
  <a class="volver" href="../">&larr; RIPworx</a>
  <button class="idioma" type="button"><span lang="en">Español</span><span lang="es">English</span></button>
  <h1 style="margin:0"><a href="../"><img class="marca" src="../img/ripworx-blanco.png" alt="RIPWORX" width="586" height="133"></a></h1>
</header>

<main>
<section class="recuadro" id="novedades">
  <h2><span lang="en">ALL NEWS</span><span lang="es">TODAS LAS NOVEDADES</span></h2>
{lista(noticias, '../')}
  <p class="mas-noticias"><span lang="en">Follow the news in your feed reader:</span><span lang="es">Sigue las novedades en tu lector de noticias:</span>
  <a href="../news.xml" lang="en">RSS</a><a href="../noticias.xml" lang="es">RSS</a></p>
</section>
</main>

<footer>
  <p lang="en">Visit <a href="https://www.youtube.com/@retroinfopy">Retro Informática Paraguay</a> on YouTube.</p>
  <p lang="es">Visita <a href="https://www.youtube.com/@retroinfopy">Retro Informática Paraguay</a> en YouTube.</p>
  <p lang="en">© 2026 RIPworx. Commodore 64 is a trademark of its respective owner.</p>
  <p lang="es">© 2026 RIPworx. Commodore 64 es una marca registrada de su respectivo dueño.</p>
</footer>

</body>
</html>
'''


def rss(noticias, idioma):
    """RSS 2.0; cada noticia, a las 12:00 de Asunción del día"""
    def rfc(d):
        return f'{DIAS_RFC[d.weekday()]}, {d.day:02d} {MESES_EN[d.month - 1]} {d.year} 12:00:00 -0300'
    titulo = 'Novedades de RIPworx' if idioma == 'es' else 'RIPworx news'
    desc = ('Juegos para computadoras retro, hechos en Asunción, Paraguay.' if idioma == 'es'
            else 'Games for retro computers, made in Asunción, Paraguay.')
    pagina = 'noticias/'
    items = []
    for n in noticias:
        d = datetime.date.fromisoformat(n['fecha'])
        nombre = PRODUCTOS[n['producto']][0]
        t = n[idioma]
        link = SITIO + n['enlace']
        items.append(f'''  <item>
    <title>{e(t["titulo"] if t["titulo"].startswith(nombre) else nombre + ": " + t["titulo"])}</title>
    <link>{e(link)}</link>
    <guid isPermaLink="false">{e(n["fecha"] + "-" + n["producto"] + "-" + ident(n))}</guid>
    <pubDate>{rfc(d)}</pubDate>
    <description>{e(t["texto"])}</description>
  </item>''')
    hoy = datetime.date.fromisoformat(noticias[0]['fecha'])
    return f'''<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{titulo}</title>
  <link>{SITIO}{pagina}</link>
  <atom:link href="{SITIO}{'noticias.xml' if idioma == 'es' else 'news.xml'}" rel="self" type="application/rss+xml"/>
  <description>{desc}</description>
  <language>{'es' if idioma == 'es' else 'en'}</language>
  <lastBuildDate>{rfc(hoy)}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
'''


def ident(n):
    """un identificador fijo de cada noticia (no cambia si se agregan otras): las letras del título en inglés"""
    return ''.join(c for c in n['en']['titulo'].lower() if c.isalnum())[:40]


def version_estilo():
    import re
    with open(os.path.join(RAIZ, 'index.html'), encoding='utf-8') as f:
        return re.search(r'estilo\.css\?v=(\d+)', f.read()).group(1)


VERSION_ESTILO = None


def main():
    global VERSION_ESTILO
    VERSION_ESTILO = version_estilo()
    noticias = cargar()
    p = os.path.join(RAIZ, 'index.html')
    with open(p, encoding='utf-8') as f:
        s = f.read()
    ini, fin = '<!-- noticias:inicio', '<!-- noticias:fin -->'
    a, b = s.index(ini), s.index(fin) + len(fin)
    s = s[:a] + seccion_inicio(noticias) + s[b:]
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)
    os.makedirs(os.path.join(RAIZ, 'noticias'), exist_ok=True)
    with open(os.path.join(RAIZ, 'noticias', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(pagina_archivo(noticias))
    for idioma, nombre in (('es', 'noticias.xml'), ('en', 'news.xml')):
        with open(os.path.join(RAIZ, nombre), 'w', encoding='utf-8') as f:
            f.write(rss(noticias, idioma))
    print(f'{len(noticias)} noticias: index.html (las últimas {EN_INICIO}), noticias/index.html, noticias.xml, news.xml')


if __name__ == '__main__':
    main()
