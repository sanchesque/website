# Traspaso: sanchesque.com y perfil de GitHub

Área de la sesión «Sanchesque.com» (decisión 0015): `website/` (repo
`sanchesque/website`, rama `master`) y `github-profile/` (repo
`sanchesque/.github`, rama `main`). El backlog completo está en
`admin/web-backlog.md`; aquí solo lo que está en marcha.

- **Objetivo:** web en Cloudflare Workers (D-05) estable y cerrar
  lo que queda del plan de dominios. Se comprueba con
  `python3 scripts/check_site.py _site` y mirando la web publicada.
- **Turno:** Claude (desde 2026-11-20)
- **Rama:** `master`. Push = publicar en sanchesque.com (Workers Builds:
  `sh scripts/build_site.sh && python3 scripts/check_site.py _site`,
  luego `npx wrangler deploy`). Las demás ramas generan vistas previas
  en `sanchesque-website.sanchesque-studios.workers.dev`.
- **Archivos en uso:** ninguno ahora mismo.

## Hecho

- 16 a 19-nov · Claude: logotipo de Garaticker en su página; DNS de
  `sanchesque.com` en Cloudflare (zona `04cb72bf…`, servidores de
  nombres cambiados el 17-nov) y vigilado hasta el 19-nov; correo bien.
- 20-nov · Claude: la web publica solo una lista cerrada
  (`scripts/build_site.sh` → `_site/`); `README.md`, `HANDOFF.md` y los
  scripts dan 404.
- 20-nov · Claude, con el sí de Alex: **paso 8 terminado.** Worker
  `sanchesque-website`; Workers Builds sobre `master`; 301 de
  `/carpeta` a `/carpeta/` (`_redirects` generado); `_headers` con CSP
  en modo informe (regla propia para la ayuda de Garaticker), COOP/CORP
  (`/img/*` en `cross-origin`) y reglas de especulación; página legal
  es/en dice Cloudflare; `sanchesque.com` y `www` en el Worker (regla
  `www` → apex 301, Always Use HTTPS); Crawler Hints activado; Action de
  Pages retirada y rama `cloudflare-workers` fusionada (borrada el
  22-nov). CodeQL ya no analiza GitHub Actions (22-nov).
  Vuelta atrás del dominio: quitar los dos dominios del Worker y crear
  `sanchesque.com` A 185.199.108-111.153, AAAA 2606:50c0:8000-8003::153
  y `www` CNAME `sanchesque.github.io` (TTL 3600, sin proxy).
- 20-nov · Claude, con el sí de Alex y a petición de Tabaibi: DNS del
  panel. A temporal `tabaibi-panel-new` → `89.117.63.57`; `tabaibi-panel`
  pasa de CNAME a Northflank a A `89.117.63.57` (los dos sin proxy, TTL
  60).
- 22-nov · Claude, con el sí de Alex: mejoras de `modern-web-review.md`,
  puntos 1 a 8 y 10, publicadas en `388ceef` y comprobadas en vivo.
- 23-nov · Claude, con el sí de Gestión y de Alex: punto 11, publicado
  en `c703f34` y comprobado en vivo. `scripts/lang-redirect.js`
  bloqueante en el `<head>` de las tres páginas en español redirige a
  la ruta del `hreflang="en"` antes de pintar (sin parpadeo ni doble
  conteo en GoatCounter); `lang.js` solo guarda el clic.
- 23-nov · Claude, con el sí de Alex: `/favicon.ico` y
  `/apple-touch-icon.png` de la raíz, 301 a `img/brand/` (`d67235d`,
  comprobado en vivo). Caché de `/fonts/*` a 30 días (`9f0f93e`, entró
  con el paso 8) comprobada en vivo. La regla de caché de la zona es de
  Garaticker (`stickers.sanchesque.com`), no de la web.
- 23-nov · Claude, con el sí de Alex: CSP real (`db7d6f7`), una sola
  cabecera `Content-Security-Policy` (absorbe la de `frame-ancestors`);
  la ayuda de Garaticker conserva la suya con `'unsafe-inline'`.
  Comprobado en vivo: cabecera en 8 páginas; consola sin errores en `/`,
  `/en/` y la ayuda; Manrope, imágenes, GoatCounter y el buscador de la
  ayuda funcionan. No hay formularios. Vuelta atrás: renombrar las tres
  `Content-Security-Policy` de `_headers` a `-Report-Only`.
- 23-nov · Claude, a petición de Gestión (plan de la web aprobado,
  decisión 0020): quitada la línea «WhatsApp próximamente» del contacto
  en `/` y `/en/`. `.soon` se queda para App Store y Google Play.
- 23-nov · Alex: revisión de indexación (exportes en `admin/seo/`).
  Google, 18 indexadas y 4 sin indexar (1 redirección, 3 rastreadas sin
  indexar); sitemaps y host bien. Bing, 2 indexadas; aún no ha vuelto a
  rastrear tras el cambio a Cloudflare. Sin errores de DNS ni servidor.

## Falta

- [ ] **Panel de Tabaibi:** borrar `tabaibi-panel-new` cuando Tabaibi
  avise del final del traslado (hacia el 27-nov o después), con el sí
  de Alex. Mientras dure el rodaje, vuelta atrás si Tabaibi la pide:
  borrar el A de `tabaibi-panel` y crear el CNAME
  `tabaibi-panel.sanchesque.com.alex-s8yt.dns.northflank.app` (sin
  proxy, TTL 60).
- [ ] **Paso 9 (Alex), entre el 27-nov y el 4-dic:** desactivar GitHub
  Pages sin borrar su TXT y activar DNSSEC (el DS se pone en IONOS con
  la clave de su API). Después, revocar la clave de IONOS.
- [ ] **Hacia el 7-dic, 404 de Googlebot:** el 23-nov eran el 21 % del
  rastreo (pico el 15-nov, aún en GitHub Pages). Rastreo propio del
  23-nov: ningún enlace ni recurso nuestro roto. Si el porcentaje no
  baja, Alex abre en Search Console Ajustes › Estadísticas de rastreo ›
  «No se ha encontrado (404)», que lista las URL, y se decide.
  Candidatas: URL antiguas e internas que ya dan 404 a propósito.
  `/favicon.ico` y `/apple-touch-icon.png` en la raíz redirigen con 301
  a `img/brand/` desde el 23-nov (`build_site.sh` añade las dos reglas
  a `_redirects`).
- [ ] **GIPHY (D-07):** cuando apruebe el canal de marca, volver a poner
  sus enlaces en el pie, `sameAs`, la página de Garaticker y el perfil.

## Preguntas abiertas

Ninguna. La protección de dominio de IONOS no hace falta (Alex,
22-nov).

## Para quien coja el turno

- Nada se sube sin el sí de Alex en el chat de esta sesión; el de otra
  sesión no vale. Cada escritura en Cloudflare o IONOS, también.
- Las copias de marca (`styles/brand/`, `img/brand/`, `fonts/`) no se
  editan: se cambian en `brand/` y se traen con `scripts/sync_brand.sh`.
  La ayuda de Garaticker se trae con `scripts/sync_garaticker.sh help`.
- Sin raya larga (U+2014) en ningún texto. Web bilingüe: cada cambio va
  en `/` y en `/en/`. `check_site.py` lo comprueba.
- Reglas fijas: `/tabaibi/` y `/en/tabaibi/` no se mueven; WhatsApp
  del estudio no se enlaza (no es público); no se publica la privacidad de
  Garaticker; GPTBot y OAI-SearchBot pueden leer la web (sin bloqueo de
  bots de IA en Cloudflare).
- Un archivo público nuevo en la raíz o una carpeta nueva se añade a
  `scripts/build_site.sh`; si no, no se publica.
- Clave de IONOS: en el llavero (`ionos-dns-api`), se lee solo en línea
  y nunca se imprime. Puede escribir en todas las zonas: no tocar
  `erasmuswork.com`, `fontelabakery.com` ni `novalchem.com`.
- `wrangler login` tiene sesión OAuth en este Mac
  (`cloudflare-sticker@sanchesque.com`); `npx wrangler logout` al
  cerrar el paso 9.
- `github-profile/`: limpio, `89d9454` en origin, nada en marcha.
