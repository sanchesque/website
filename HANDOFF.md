# Traspaso: sanchesque.com y perfil de GitHub

Área de la sesión «Sanchesque.com» (decisión 0015): `website/` (repo
`sanchesque/website`, rama `master`; un push publica en GitHub Pages) y
`github-profile/` (repo `sanchesque/.github`, rama `main`). El backlog
completo está en `admin/web-backlog.md`; aquí solo lo que está en marcha.

- **Objetivo:** pasar la web de GitHub Pages a Cloudflare Workers (D-05,
  paso 8 de `admin/domains-hosting-plan.md`) sin corte, y aplicar las
  mejoras aprobadas de `admin/web-briefs/modern-web-review.md`. Se
  comprueba con `python3 scripts/check_site.py` y mirando la web
  publicada.
- **Turno:** Claude (desde 2026-11-20)
- **Rama:** `master` (push = publicar en sanchesque.com por Workers
  Builds). `cloudflare-workers` queda fusionada.
- **Archivos en uso:** ninguno ahora mismo.

## Hecho

- 2026-11-16 · Claude: logotipo de Garaticker en su página, es y en
  (`5a9b7a5`, publicado con el sí de Alex).
- 2026-11-16 · Claude: rama `cloudflare-workers` en origin (`681b18b`):
  `wrangler.jsonc`, `.assetsignore` y `_headers`, probada con
  `wrangler dev`, sin desplegar.
- 2026-11-16 · Claude: caché de `/fonts/*` a 30 días sin `immutable`
  (`9f0f93e`, solo en local, en `cloudflare-workers`).
- 2026-11-17 · Claude: DNS de `sanchesque.com` en Cloudflare (zona
  `04cb72bfb8a6a5fc3354c2f9c2b934de`, 22 registros sin proxy,
  servidores de nombres cambiados a las 16:54 por la API de IONOS).
  Correo comprobado en los dos sentidos.
- 2026-11-19 · Claude: vigilancia del DNS cerrada: zona activa, los tres
  resolvedores públicos dan Cloudflare, web y panel bien.
- 2026-11-20 · Claude: este traspaso (en `1b82d61`).
- 2026-11-20 · Claude: la Action de Pages publica solo una lista cerrada
  de archivos (`scripts/build_site.sh` → `_site/`, revisado con
  `check_site.py _site`); `README.md`, `HANDOFF.md` y los scripts
  internos dejan de publicarse. Alex lo pidió vía Gestión. Subido con el
  sí de Alex en `1b82d61` (aplastado con el traspaso) y comprobado en
  vivo: `/README.md`, `/HANDOFF.md` y `/scripts/check_site.py` dan 404;
  portada, `/en/`, `/legal/`, `/garaticker/help/`, `lang.js`, fuentes,
  imágenes, `robots.txt` y `sitemap.xml` dan 200.
- 2026-11-20 · Claude: Alex dijo «Sube y pasa a workers» (vía Gestión,
  confirmado aquí). `cloudflare-workers` subida con `9f0f93e` y `master`
  fusionado; Workers sirve `_site/` (`wrangler.jsonc`), `build_site.sh`
  copia `_headers` y se quita `.assetsignore`. Probado con `wrangler dev`:
  páginas 200, `/tabaibi` 307 a `/tabaibi/`, `README.md`, `HANDOFF.md`,
  `_headers` y scripts 404, cabeceras y caché de fuentes bien.
- 2026-11-20 · Claude: Worker `sanchesque-website` creado con
  `wrangler deploy` desde local (sí de Alex; la importación del panel
  fallaba con «This Worker does not exist»). Vista previa:
  `https://sanchesque-website.sanchesque-studios.workers.dev`, versión
  `055dad29`. Mismo resultado que en local: páginas 200, internos 404,
  404 bilingüe, cabeceras y cachés bien. `wrangler login` queda con
  sesión OAuth en este Mac (`cloudflare-sticker@sanchesque.com`).
- 2026-11-20 · Claude: Workers daba 307 en `/carpeta` → `/carpeta/`;
  Alex pidió 301 como Pages. `build_site.sh` genera `_site/_redirects`
  con un 301 por cada carpeta con `index.html` (21 reglas, se actualiza
  solo). Probado con `wrangler dev`: 301 con la consulta conservada,
  `/_redirects` da 404. Subido (`9ad7463`) y desplegado en workers.dev
  (versión `5a095f3b`), con el sí de Alex: las 21 reglas dan 301.
- 2026-11-20 · Claude (local, sin subir): página legal es/en dice que
  sirve Cloudflare (fecha 20-nov, `lastmod` del sitemap); `_headers` con
  CSP en modo informe (punto 12; la ayuda de Garaticker con su regla
  propia por los scripts y estilos en línea de Zensical), COOP y CORP
  `same-origin` con `/img/*` en `cross-origin` (13) y reglas de
  especulación `prefetch` moderadas por cabecera (14,
  `speculationrules.json`); el `style=` de Garaticker pasa a la clase
  `.spaced`. Probado con `wrangler dev`: cabeceras por ruta bien y sin
  avisos de CSP en las páginas propias. El punto 16 se deja: basta la CSP.
- 2026-11-20 · Claude, con el sí de Alex: **`sanchesque.com` servido por
  Workers.** Always Use HTTPS activado; regla de redirección `www` →
  apex (301, ruleset `5f2b99cf…`); borrados los 8 A/AAAA de GitHub Pages
  y el CNAME de `www`; dominios del Worker `sanchesque.com` y
  `www.sanchesque.com` (también en `wrangler.jsonc`, con `workers_dev`).
  Comprobado por Cloudflare: páginas 200, `/tabaibi` 301, internos 404,
  `http://` y `www` 301 a `https://sanchesque.com` con la consulta,
  cabeceras nuevas, `server: cloudflare`; MX y panel de Tabaibi sin
  cambios. Vuelta atrás: quitar los dos dominios del Worker y volver a
  crear `sanchesque.com` A 185.199.108-111.153, AAAA
  2606:50c0:8000-8003::153 y `www` CNAME `sanchesque.github.io` (TTL
  3600, sin proxy).
- 2026-11-20 · Claude, con el sí de Alex: `cloudflare-workers`
  fusionada en `master`; Action de Pages retirada; Workers Builds
  compila `master` con `sh scripts/build_site.sh && python3
  scripts/check_site.py _site`. GitHub Pages sigue activo con la última
  versión (no lo ve nadie): se desactiva en el paso 9.
- 2026-11-20 · Alex: repo conectado en Workers Builds (rama
  `cloudflare-workers`, `sh scripts/build_site.sh`, `npx wrangler
  deploy`). Primera compilación de `9ad7463`: success. Previews activadas
  para las demás ramas (`npx wrangler preview`); en `master` fallarán
  hasta la fusión, sin efecto en la web. Desde ahora, push a
  `cloudflare-workers` = desplegar en workers.dev.

## Falta

- [ ] Mejoras de `modern-web-review.md` en `master`, en un commit: puntos
  1 a 8 y 10 (el 7 como regla de `site.css`, DESIGN.md §5). Push con el
  sí de Alex.
- [ ] Punto 11: mirar en GoatCounter si `lang.js` cuenta dos visitas al
  redirigir a `/en/`; si se confirma, proponer el arreglo a Gestión.
- [ ] CSP: tras unos días sin avisos en la consola, pasar
  `Content-Security-Policy-Report-Only` a `Content-Security-Policy` en
  `_headers` (con el sí de Alex). Punto 16 (GoatCounter) descartado por
  ahora: basta la CSP.
- [ ] Paso 9 (Alex, una o dos semanas después del 20-nov): desactivar
  GitHub Pages sin borrar su TXT y activar DNSSEC.
- [ ] DNS del panel de Tabaibi (Entrada del 20-nov, plan
  `projects/tabaibi/code/docs/panel-to-contabo-plan.md`): paso 0, TTL de
  `tabaibi-panel.sanchesque.com` a 60 s una semana antes; paso 6, CNAME
  (hoy a `alex-s8yt.dns.northflank.app`) por A a `89.117.63.57` sin
  proxy. Nada hasta que Tabaibi avise de cada paso
  (local_ebf6f7cf-64b2-4fdc-a05f-04c9d97978f5) y con el sí de Alex aquí.
  Vuelta atrás: el CNAME anterior. 20-nov, a petición de Tabaibi y con
  el sí de Alex: A temporal `tabaibi-panel-new` → `89.117.63.57`, sin
  proxy, TTL 60 (id `330e009f…`); borrarlo al acabar la migración.
  20-nov, tiempo 2 (sí de Alex, aviso de Tabaibi): CNAME borrado y
  `tabaibi-panel` A → `89.117.63.57`, sin proxy, TTL 60. Vuelta atrás:
  borrar el A y crear CNAME
  `tabaibi-panel.sanchesque.com.alex-s8yt.dns.northflank.app`.
- [ ] 23-nov: revisar indexación en Search Console («Páginas», y que no
  haya errores de DNS) y en el Site Explorer de Bing.
- [ ] Cuando GIPHY apruebe el canal de marca (D-07): volver a poner sus
  enlaces en el pie, `sameAs`, la página de Garaticker y el perfil.

## Preguntas abiertas

- Pendiente de Alex desde el 17-nov: volver a activar la protección de
  dominio en IONOS y revocar la clave de su API (Gestión dice que se va
  a revocar; el paso 8 no la necesita; el DS de DNSSEC del paso 9 irá
  por el panel o con una clave nueva).

## Para quien coja el turno

- Nada se sube sin el sí de Alex en el chat de esta sesión; el de otra
  sesión no vale. Push en `master` = publicar.
- Las copias de marca (`styles/brand/`, `img/brand/`, `fonts/`) no se
  editan: se cambian en `brand/` y se traen con `scripts/sync_brand.sh`.
  La ayuda de Garaticker se trae con `scripts/sync_garaticker.sh help`.
- Sin raya larga (U+2014) en ningún texto. Web bilingüe: cada cambio va en `/` y en
  `/en/`. `check_site.py` lo comprueba.
- Reglas fijas: `/tabaibi/` y `/en/tabaibi/` no se mueven; «WhatsApp
  próximamente» se queda en gris; no se publica la privacidad de
  Garaticker; GPTBot y OAI-SearchBot pueden leer la web (sin bloqueo de
  bots de IA en Cloudflare).
- Clave de IONOS: en el llavero (`ionos-dns-api`), se lee solo en línea
  y nunca se imprime. Puede escribir en todas las zonas: no tocar
  `erasmuswork.com`, `fontelabakery.com` ni `novalchem.com`.
- Un archivo público nuevo en la raíz o una carpeta nueva se añade a
  `scripts/build_site.sh`; si no, no se publica, ni en Pages ni en
  Workers (los dos sirven `_site/`).
- `github-profile/`: limpio, `89d9454` en origin, nada en marcha.
