/*
 * Idioma del sitio: el que eligió el visitante (guardado en el navegador); si no eligió
 * nada, español si su navegador está en español, y si no, inglés. El botón .idioma cambia
 * entre los dos. Sin JavaScript se ve el inglés (data-idioma="en" en el HTML).
 */
(function () {
  var raiz = document.documentElement;
  function guardado() { try { return localStorage.getItem('ripworx-idioma'); } catch (e) { return null; } }
  function guardar(v) { try { localStorage.setItem('ripworx-idioma', v); } catch (e) { } }
  function delNavegador() {
    var l = (navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || 'en']);
    for (var i = 0; i < l.length; i++) {
      var c = String(l[i]).toLowerCase();
      if (c.indexOf('es') === 0) return 'es';
      if (c.indexOf('en') === 0) return 'en';
    }
    return 'en';
  }
  function poner(v) {
    raiz.setAttribute('data-idioma', v);
    raiz.setAttribute('lang', v);
    var t = raiz.getAttribute('data-titulo-' + v);
    if (t) document.title = t;
  }
  var g = guardado();
  poner(g === 'es' || g === 'en' ? g : delNavegador());
  document.addEventListener('DOMContentLoaded', function () {
    var bs = document.querySelectorAll('.idioma');
    for (var i = 0; i < bs.length; i++) bs[i].addEventListener('click', function () {
      var v = raiz.getAttribute('data-idioma') === 'es' ? 'en' : 'es';
      poner(v); guardar(v);
    });
  });
})();
