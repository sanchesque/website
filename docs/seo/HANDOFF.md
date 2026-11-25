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
- 25-nov · Por orden de Alex (24-nov, vía Gestión): plantilla de informe
  mensual `monthly-report-template.md`; script de rastreo semanal
  `scripts/seo_weekly.sh` (corre `check_site.py --live`, guarda
  `docs/seo/live-AAAA-MM-DD.txt` y alerta con exit 2 si fallan L-03/L-04);
  convención fecha+hash documentada aquí y en cada auditoría. Probado
  `seo_weekly.sh` a mano: `live-2026-11-25.txt`, exit 0, L-01 a L-05
  pasan. La programación semanal (cron del sistema o de la sesión) la
  pone la madre; el script vale también a mano tras cada despliegue.

## Falta

- **H-M4:** PageSpeed o Lighthouse otro día (o `npx lighthouse` con el
  sí de Alex); si la ayuda pasa de 2,5 s de LCP, llevarlo a Garaticker.
- **P-1 a P-4:** Alex, en Search Console y Bing Webmaster Tools (hacia
  el 7-dic; P-1 se puede hacer ya).
- **F-404 (hacia el 7-dic):** vigilar si baja el 21 % de 404 de
  Googlebot; F-HA1, unas 2-3 semanas tras `456ac08`.
- **H-M3, H-B3, H-B6, H-B7 y el origen de H-A1:** a Garaticker por su
  Entrada.
- **D-07 (GIPHY) y `/social/`:** bloqueados en la madre (Fase 1).
- `scripts/seo_weekly.sh` aún no está subido: va con el siguiente push
  de la madre (local; `check_site.py` ya entró en `9e823ec`).
- Programar el rastreo semanal (cron) es de la madre.

## Reglas

- Nada se publica sin el sí de Alex en el chat de la sesión madre.
- Convenciones de fecha+hash, arriba.
