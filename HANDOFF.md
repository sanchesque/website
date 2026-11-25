# Traspaso: sanchesque.com y perfil de GitHub

Área de la sesión «Sanchesque.com» (decisión 0015): `website/` (repo
`sanchesque/website`, rama `master`) y `github-profile/` (repo
`sanchesque/.github`, rama `main`). El backlog completo está en
`admin/web-backlog.md`; aquí solo lo que está en marcha.

- **Objetivo:** web en Cloudflare Workers (D-05) estable y cerrar
  lo que queda del plan de dominios. Se comprueba con
  `python3 scripts/check_site.py _site` y mirando la web publicada.
- **Turno:** Claude (desde 2026-11-20). El 24-nov Vibe ejecutó la orden
  de Alex vía Gestión (squash y push) y la sincronización de brand
  pedida por Marca; ver «Hecho».
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
- 23-nov · Claude, a petición de Marca: `og:image` propio de Garaticker
  en `/garaticker/` y `/en/garaticker/` (`img/brand/garaticker/og-image.png`,
  copiado por `sync_brand.sh`). La ayuda lo cambia en su tema
  (`docs-theme/main.html`); Garaticker lo hizo y el 24-nov se trajo
  con `sync_garaticker.sh help` (14 páginas, solo imagen y alt).
- 24-nov · Vibe, con el sí de Alex vía Gestión: los 4 commits locales
  (f278f0b, 4d6c1b1, 67287e8, a16f457) aplastados en uno según la 0003
  conservando el trailer de Claude y publicados en `456ac08` (push a
  origin/master; Workers Builds desplegó). Comprobado en vivo con
  curl: `/tabaibi/` y `/en/tabaibi/` 200, `/index.html` 301 a `/`,
  `/404.html` 307 a `/404`, `/garaticker/help/faq/sitemap.xml` y la
  versión `/en/` 301 a `/garaticker/help/sitemap.xml` (H-A1), sitemap
  de la ayuda 200, home con GitHub en `sameAs`, `lastmod` 2026-11-24
  en el sitemap y CSP real activa. Subsesión «Sanchesque.com · SEO»
  avisada con el hash `456ac08`.
- 24-nov · Vibe, orden de Alex vía Gestión (local, sin push):
  `scripts/publish.sh` (check_site del repo con C-15, build, check de
  `_site`, push, espera del run «Push on master» del commit vía `gh`,
  luego `check_site.py --live`; salida archivada en `logs/`, gitignored
  y no publicada); Action `.github/workflows/post-deploy.yml` que corre
  `check_site.py --live` tras «Push on master» en master (y a mano con
  workflow_dispatch) y falla si L-01..L-05 no pasan; C-15 en
  `check_site.py` (copias de brand al día con `brand/`, solo en local);
  sección «Vigilancias con fecha» en `admin/web-backlog.md`.
- 24-nov · Vibe, a petición de Marca (brand `55764e4`, planes P-1 a P-8
  aprobados): `sync_brand.sh` copia ya los avatares
  `logos/*/social/*-avatar-1080.png` a `img/brand/*/social/` y los PNG
  de email `tabaibi-horizontal-color-1000.png` (firma P-1 de tabaibi@)
  y `garaticker-horizontal-black-1000.png` (boletín P-6) a
  `img/brand/email/`. Publicado por Claude el 24-nov en `9e823ec`
  (squash con el sí de Alex vía Gestión); comprobado en vivo.
- 23-nov · Alex: revisión de indexación (exportes en `admin/seo/`).
  Google, 18 indexadas y 4 sin indexar (1 redirección, 3 rastreadas sin
  indexar); sitemaps y host bien. Bing, 2 indexadas; aún no ha vuelto a
  rastrear tras el cambio a Cloudflare. Sin errores de DNS ni servidor.

## Falta

- [ ] **`/social/`:** plan en `docs/social-page-plan.md` (24-nov), en
  espera de la Fase 1; preguntas abiertas en su §5.
- [ ] **SEO:** informe de la subsesión en `docs/seo/audit-2026-11-24.md`
  (24-nov): 1 alta (H-A1, `sitemap.xml` por subpágina de la ayuda da
  404, confirmado en vivo), 4 medias, 9 bajas y P-1 a P-4 para Alex.
  Propuestas para `check_site.py` en `docs/seo/checklist.md`.
  Aprobado por Alex y hecho en local el 24-nov: H-A1 (301 por subpágina
  en `build_site.sh`), H-M1, H-M2 (`WebSite`), H-M3 (pendiente del visto
  bueno de Garaticker), H-B1 (301 de `index.html`), H-B4 y H-B5, y GitHub
  en `sameAs`. H-B2 sin cambio (lleva `noindex`). Lo de la ayuda, en la
  Entrada de Garaticker. P-1 a P-4: Alex, más adelante (hacia el 7-dic).
- [ ] **Commit local sin subir (25-nov):** la automatización de
  publicación de esta orden (`scripts/publish.sh`, Action
  `.github/workflows/post-deploy.yml`, C-15 en `check_site.py`,
  `logs/` en `.gitignore`) más el re-sync de `img/brand/garaticker/og-image.png`
  con brand `a85b3e2`. Publicar solo con el sí de Alex en este chat,
  con `scripts/publish.sh`.
- [ ] **Favicon con la G en `/garaticker/help/`** (petición de Marca,
  23-nov): la ayuda se genera en el repo de Garaticker y se copia con
  `sync_garaticker.sh help`. La sesión Garaticker investigó el 24-nov
  (turno allí: Claude): el cambio es en sus `zensical.help-es/en.toml`
  (`favicon` y `logo` a `assets/brand-garaticker/`) más el mapeo de su
  `scripts/sync_brand.py`; el favicon propio está en
  `brand/logos/garaticker/favicon/`. Cuando Garaticker lo publique,
  re-sincronizar aquí con `scripts/sync_garaticker.sh help` y subir con
  el sí de Alex.
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
- Publicar: con el sí de Alex, `scripts/publish.sh` (cadena completa con
  checks en vivo); `scripts/publish.sh --no-push` solo comprueba y
  construye. La Action «Post-deploy live checks» repite L-01..L-05 tras
  cada «Push on master».
- Las copias de marca (`styles/brand/`, `img/brand/`, `fonts/`) no se
  editan: se cambian en `brand/` y se traen con `scripts/sync_brand.sh`.
  La ayuda de Garaticker se trae con `scripts/sync_garaticker.sh help`.
- Sin raya larga (U+2014) en ningún texto. Web bilingüe: cada cambio va
  en `/` y en `/en/`. `check_site.py` lo comprueba.
- Reglas fijas: `/tabaibi/` y `/en/tabaibi/` no se mueven; WhatsApp
  Business del estudio es «Solo clientes»: no se publica ni se enlaza; no se publica la privacidad de
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
