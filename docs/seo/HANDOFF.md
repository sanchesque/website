# Traspaso: subsesión «Sanchesque.com · SEO»

De la tabla de sesiones (decisión 0015), hija de «Sanchesque.com».
Escribe solo en `website/docs/seo/` y, por orden expresa de Alex, en
`website/scripts/check_site.py` (sin push). Sin commits ni despliegues.
Entrada de la madre: `admin/web-backlog.md`.

- **Turno:** Vibe (desde 2026-11-24, orden de Alex vía Gestión)
- **Archivos propios:** `audit-2026-11-24.md`, `checklist.md`,
  `verification-2026-11-24.md`, este HANDOFF.

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
- El script nuevo aún no está subido: va con el siguiente push de la
  madre (por ahora, local; `git status` lo muestra modificado).

## Reglas

- Nada se publica sin el sí de Alex en el chat de la sesión madre.
- Sin raya larga (U+2014) en ningún texto; `check_site.py` lo comprueba.
- Los informes y verificaciones llevan fecha y, tras un despliegue, el
  hash (ver `verification-2026-11-24.md`).
