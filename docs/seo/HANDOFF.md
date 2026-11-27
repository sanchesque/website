# Traspaso: subsesión «Sanchesque.com · SEO»

De la tabla de sesiones (decisión 0015), hija de «Sanchesque.com».
Escribe solo en `website/docs/seo/` y, por orden expresa de Alex, en
`website/scripts/check_site.py` (sin push). Sin commits ni despliegues.
Entrada de la madre: `admin/web-backlog.md`.

- **Turno:** Vibe (desde 2026-11-24, orden de Alex vía Gestión)
- **Archivos propios:** `audit-2026-11-24.md`, `checklist.md`,
  `verification-2026-11-24.md`, `monthly-report-template.md`,
  `live-*.txt`, este HANDOFF.

## Convenciones

- **Fecha + hash:** cada auditoría y cada verificación llevan fecha
  (AAAA-MM-DD) y, si hubo despliegue desde la anterior, el hash de
  `master` que se publicó (p. ej. `456ac08`). Las salidas del rastreo
  semanal son `live-AAAA-MM-DD.txt` (UTC).
- Los informes mensuales se copian de `monthly-report-template.md` como
  `monthly-AAAA-MM-DD.md`; los exports de consola van a `admin/seo/` con
  la fecha delante del nombre.
- Sin raya larga (U+2014) en ningún texto; `check_site.py` lo comprueba.

## Hecho

- 24-nov · Auditoría de la web publicada y del código (`audit-2026-11-24.md`):
  1 alta (H-A1), 4 medias, 9 bajas, P-1 a P-4 para Alex. La madre aplicó
  los fixes aprobados y se publicaron en el squash `456ac08`.
- 24-nov · `verification-2026-11-24.md`: H-A1 y H-B1 comprobados en vivo
  tras el despliegue (12 subpáginas de la ayuda con 301 a la sitemap raíz,
  `/index.html` con 301).
- 24-nov · Por orden de Alex: `scripts/check_site.py` ampliado con
  C-01 a C-14 (errores; la parte `lastmod` de C-07 como aviso), W-01 a
  W-04 (avisos) y el modo `--live` (L-01 a L-05) para lanzar a mano tras
  cada publicación. Verificado sobre `_site/` y el repo (25 páginas, 0
  errores, 5 avisos) y en vivo (L-01 a L-05 pasan). Detalle en
  `checklist.md`.
- 24-nov · PageSpeed Insights reintentado (API sin clave, móvil, las 5
  URL de H-M4): 429, cuota diaria del proyecto anónimo agotada. Anotado
  en la auditoría; H-M4 sigue abierto.
- 25-nov · **Search Console API funcionando** (P-2/P-4 parcial): SA en
  `~/.secrets/gsc-sa.json` (600), añadida como propietaria de la
  propiedad de dominio `sc-domain:sanchesque.com`; primer fetch OK en
  `gsc-2026-11-25.md` + JSON en `gsc-2026-11-25/` (3 sitemaps sin
  errores, 39 impresiones y 1 clic en nov, `/` indexada PASS). La lista
  de 404 (P-1) solo sale de la web de SC y ya se exportó aparte.
- 25-nov · **Search Console API preparada:** librerías instaladas con
  el sí de Alex en `~/.venvs/gsc` (venv fuera del repo;
  `google-api-python-client` 2.202.0 + auth) y helper
  `docs/seo/gsc_fetch.py`, que lee la cuenta de servicio del llavero
  (`gsc-service-account`) o de `GSC_SA_FILE` y guarda sitemaps,
  searchanalytics y urlInspection en `gsc-AAAA-MM-DD/`. Sin credencial
  todavía: falta crear la cuenta de servicio en Cloud Console y añadirla
  como propietaria en Search Console.
- 25-nov · **Bing Webmaster Tools vía API** (P-3 resuelto): sitio
  verificado; 3 sitemaps en Success con 22 URL (8+7+7), el principal
  releído el 22-nov y los de la ayuda desde el 15-nov; 1 impresión
  (13-nov), 0 clics; rastreo en ritmo normal. Informe en
  `bing-2026-11-25.md` con los JSON brutos en `bing-2026-11-25/`. La key
  se leyó del llavero en variable, sin imprimirla ni guardarla.
- 25-nov · Por orden de Alex (24-nov, vía Gestión): plantilla de informe
  mensual `monthly-report-template.md`; script de rastreo semanal
  `scripts/seo_weekly.sh` (corre `check_site.py --live`, guarda
  `docs/seo/live-AAAA-MM-DD.txt` y alerta con exit 2 si fallan L-03/L-04);
  convención fecha+hash documentada aquí y en cada auditoría. Probado
  `seo_weekly.sh` a mano: `live-2026-11-25.txt`, exit 0, L-01 a L-05
  pasan. Subido con el push `766b9cd` (aviso de Gestión, 24-nov), junto
  con la plantilla mensual; `check_site.py` ya entró en `9e823ec`.
- 26-nov · Claude, a petición de Sanchesque.com: C-07 de `checklist.md` propone comparar el texto de `<main>` en la fecha de `lastmod` con el actual (los cambios solo en `<head>` no cuentan). Recomendado no publicar los JSON brutos de GSC y Bing en el repo público (`b_GetUserSites.json` lleva los códigos de verificación de Bing); lo decide Alex. Sin commit.

## Falta

- **H-M4:** PageSpeed o Lighthouse otro día (o `npx lighthouse` con el
  sí de Alex); si la ayuda pasa de 2,5 s de LCP, llevarlo a Garaticker.
- **P-4:** Alex, en Search Console (mejoras/datos estructurados y CWV).
  **P-1 ya está hecho** (25-nov): la lista de 404 confirma H-A1 (los 12
  `…/help/*/sitemap.xml`, últimos 404 el 21-nov) más favicons de la
  época Pages; ver `crawl-404-2026-11-25.md`. **P-2 ya está hecho** (18
  indexadas, 1 redirección normal, 3 de la ayuda rastreadas sin indexar;
  `coverage-2026-11-25.md`). **P-3 (Bing) ya está hecho** vía API:
  `bing-2026-11-25.md`. **P-1 a P-3 cerrados.**
- **F-404 (hacia el 7-dic):** vigilar si baja el 21 % de 404 de
  Googlebot; F-HA1, unas 2-3 semanas tras `456ac08`.
- **H-M3, H-B3, H-B6, H-B7 y el origen de H-A1:** a Garaticker por su
  Entrada.
- **D-07 (GIPHY) y `/social/`:** bloqueados en la madre (Fase 1).
- **Cron del rastreo semanal:** pendiente de programar; los
  recordatorios de fechas clave (7-dic, etc.) ya están programados
  desde Gestión (aviso de Gestión, 24-nov).

## Reglas

- Nada se publica sin el sí de Alex en el chat de la sesión madre.
- Convenciones de fecha+hash, arriba.
- **Aviso en cascada de Gestión (2026-11-27, cambio de AGENTS.md por
  Alex), confirmado:** (1) nunca tocar ramas `claude/*` ni
  `.claude/worktrees/`; (2) nada de push/despliegue sin el sí de Alex
  escrito en la conversación de la sesión madre; (3) los
  `Co-Authored-By` van solos en el último párrafo del commit, tras una
  línea en blanco; (4) los avisos en cascada se confirman respondiendo
  «confirmado».
