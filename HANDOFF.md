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
- **Rama:** `master` para la web publicada; `cloudflare-workers` para el
  paso a Workers.
- **Archivos en uso:** `wrangler.jsonc`, `_headers` y
  `scripts/build_site.sh` en `cloudflare-workers` (paso 8 en marcha).

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
  `/_redirects` da 404.

## Falta

- [ ] Mejoras de `modern-web-review.md` en `master`, en un commit: puntos
  1 a 8 y 10 (el 7 como regla de `site.css`, DESIGN.md §5). Push con el
  sí de Alex.
- [ ] Punto 11: mirar en GoatCounter si `lang.js` cuenta dos visitas al
  redirigir a `/en/`; si se confirma, proponer el arreglo a Gestión.
- [ ] Paso 8 (Workers): Workers Builds (compilación
  `sh scripts/build_site.sh`, despliegue `npx wrangler deploy`) y URL de
  vista previa; comprobar
  307 o 301 y las cabeceras; dominio propio y regla de `www`; página
  legal (es y en); Crawler Hints; puntos 12 a 16 de la revisión (CSP
  primero en modo informe); al final, fusionar la rama y retirar la
  Action de Pages. Cada escritura en Cloudflare, con el sí de Alex.
- [ ] 23-nov: revisar indexación en Search Console («Páginas», y que no
  haya errores de DNS) y en el Site Explorer de Bing.
- [ ] Cuando GIPHY apruebe el canal de marca (D-07): volver a poner sus
  enlaces en el pie, `sameAs`, la página de Garaticker y el perfil.

## Preguntas abiertas

- 2026-11-20, para Alex: conectar el repo en el Worker (Settings →
  Build → Connect, rama `cloudflare-workers`); el sí de Alex está dado.
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
