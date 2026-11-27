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

- 27-nov · Claude: ayuda de Garaticker re-sincronizada desde su
  `f887128` (`sync_garaticker.sh help`): la G como favicon y logo de
  cabecera, títulos más largos (H-B3, ya sin avisos W-01) y su arreglo
  del sitemap en el tema (H-A1). `check_site.py` sin avisos. Local,
  falta push con el sí de Alex.
- 27-nov · Claude, con el sí de Alex: publicado `0a1623b` (C-07 sobre
  texto visible y traspasos del 27-nov); Workers Builds bien,
  `check_site.py --live` en verde. Brand `bd1c0f7` sincronizado con
  `sync_brand.sh` a petición de Marca: copias ya al día, sin cambios.
- 27-nov · Claude: C-07 de `check_site.py` mira solo el texto visible
  de `<main>` (propuesta de SEO, H-M1); un cambio de cabeceras ya no
  pide subir `lastmod`. Quedan 3 avisos W-01, de la ayuda (Garaticker).
- 27-nov · Claude, con el sí de Alex: **historial reescrito.** `0443345`
  (llevaba 17 JSON crudos de Search Console y Bing) sustituido por
  `e53e39b`, mismo árbol sin los JSON; `push --force-with-lease`. Copia
  local en la rama `backup/pre-rewrite-2026-11-27` (sin subir). GitHub
  aún sirve `0443345` por su SHA hasta que lo purgue GitHub Support.
  Comprobado en vivo: 200, 301 y 404 como antes; `check_site.py --live`
  en verde. Cualquier clon con `0443345` (también el de Vibe) hace
  `git fetch && git reset --hard origin/master`.
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
- [ ] **SEO:** correcciones aprobadas de la auditoría del 24-nov
  publicadas en `456ac08` (Vibe aplastó y subió los cuatro commits
  locales con el sí de Alex vía Gestión). Comprobado en vivo el 26-nov:
  12 `…/help/*/sitemap.xml` y los `index.html` dan 301, `/tabaibi/` 200,
  `WebSite` en la portada, `docs/` y `scripts/publish.sh` dan 404.
  Pendiente: H-M3, visto bueno de Garaticker; lo de la ayuda (H-B3,
  H-B6, H-B7 y el tema), en su Entrada. P-1 cerrado (H-A1 confirmado,
  `docs/seo/crawl-404-2026-11-25.md`). C-07 ya compara solo el texto visible de
  `<main>` (27-nov): legal sin aviso.
- [ ] **Nada pendiente de push (25-nov):** la automatización de
  publicación quedó publicada con el push de Alex `766b9cd`
  (`publish.sh`, Action post-deploy, C-15, `seo_weekly.sh`). Brand
  `43fb808` sincronizado el 25-nov con `sync_brand.sh`: copias ya al
  día, sin cambios (C-15 ok).
- [ ] **Action post-deploy, limitación conocida (25-nov):** el trigger
  `workflow_run` no se disparó para los runs «dynamic» de Workers
  Builds (comprobado con `766b9cd`: 0 runs de «Post-deploy live
  checks»); de momento se lanza a mano con `workflow_dispatch` y el
  post-deploy queda cubierto por `publish.sh` en el push. Valorar
  añadir un `schedule` como red de seguridad.
- [ ] **Favicon con la G en `/garaticker/help/`** (petición de Marca,
  23-nov): la ayuda se genera en el repo de Garaticker y se copia con
  `sync_garaticker.sh help`. La sesión Garaticker investigó el 24-nov
  (turno allí: Claude): el cambio es en sus `zensical.help-es/en.toml`
  (`favicon` y `logo` a `assets/brand-garaticker/`) más el mapeo de su
  `scripts/sync_brand.py`; el favicon propio está en
  `brand/logos/garaticker/favicon/`. Cuando Garaticker lo publique,
  re-sincronizar aquí con `scripts/sync_garaticker.sh help` y subir con
  el sí de Alex.
- [ ] **Panel de Tabaibi:** Tabaibi avisó el 25-nov (vía Gestión):
  promote stable `9ca6005` hecho y verificado, panel en producción.
  Borrar el A temporal `tabaibi-panel-new` cuando Tabaibi cierre los
  pasos 9-11 de la VPS, con el sí de Alex en este chat (ratificado por
  Gestión el 27-nov-2026). Vuelta atrás si Tabaibi la pide:
  borrar el A de `tabaibi-panel` y crear el CNAME
  `tabaibi-panel.sanchesque.com.alex-s8yt.dns.northflank.app` (sin
  proxy, TTL 60).
- [ ] **Paso 9 (Alex), ventana abierta el 27-nov, hasta el 4-dic:**
  desactivar GitHub Pages sin borrar su TXT y activar DNSSEC (el DS se
  pone en IONOS con la clave de su API). Después, revocar la clave de
  IONOS y `npx wrangler logout`. Lo ejecuta Alex en el chat de esta
  sesión, con su sí por paso (aviso de Gestión, 27-nov-2026).
- [ ] **Hacia el 7-dic, 404 de Googlebot:** la causa era H-A1 (los 12
  `…/help/*/sitemap.xml`, último 404 el 21-nov), resuelta en `456ac08`.
  Comprobar en el informe de diciembre que el porcentaje baja.
- [ ] **GIPHY (D-07):** cuando apruebe el canal de marca, volver a poner
  sus enlaces en el pie, `sameAs`, la página de Garaticker y el perfil.

## Preguntas abiertas

Ninguna. La protección de dominio de IONOS no hace falta (Alex,
22-nov).

## Para quien coja el turno

- **Aviso en cascada confirmado el 27-nov-2026** (cambio de AGENTS.md
  por Alex, vía Gestión): (1) nunca ramas `claude/*` ni
  `.claude/worktrees/`; worktree propio `vibe/<tarea>` desde la rama
  principal y comprobar `git branch --show-current` antes de escribir;
  (2) push, despliegue, Cloudflare o IONOS solo con el sí de Alex
  escrito en la conversación de esta sesión, no vía Gestión; (3) los
  `Co-Authored-By` van solos en el último párrafo, tras línea en
  blanco; (4) los avisos en cascada se confirman.
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
