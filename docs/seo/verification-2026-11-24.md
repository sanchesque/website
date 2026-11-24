# Verificación en vivo tras el despliegue del 24-nov-2026

Subsesión «Sanchesque.com · SEO». Despliegue publicado el 2026-11-24
como squash `456ac0864ba2e464ef685b80b41c7a6de6d10db8` (fusión de
`f278f0b`, `4d6c1b1`, `67287e8`, `a16f457` según la decisión 0003, con el
sí de Alex vía Gestión). Workers Builds ya lo sirve en
https://sanchesque.com. Comprobaciones hechas con `curl` contra la web
publicada el 24-nov (esta subsesión) y las de la sesión madre.

## H-A1 · Confirmado

- Las 12 subpáginas de la ayuda (6 en `/garaticker/help/*/` y 6 en
  `/en/garaticker/help/*/`, listadas desde sus dos sitemaps) piden
  `…/sitemap.xml` y **todas responden 301** a la sitemap raíz de su ayuda:
  `/garaticker/help/sitemap.xml` y `/en/garaticker/help/sitemap.xml`.
- Las dos sitemaps raíz de la ayuda responden **200**.
- Comprobado también por la madre: `/garaticker/help/faq/sitemap.xml` y
  `/en/garaticker/help/faq/sitemap.xml` dan 301.
- Sigue pendiente el arreglo en origen (que el tema deje de pedir esos
  `sitemap.xml`): va a Garaticker por su Entrada. Y, a las 2 o 3 semanas,
  ver en Search Console › Estadísticas de rastreo si baja el 21 % de 404
  (P-1, lista de URL de los 404, puede confirmarlo antes).

## H-B1 · Confirmado

- `/index.html` responde **301** a `https://sanchesque.com/` (antes 307 de
  Workers). `/404.html` da 307 a `/404` (comprobado por la madre).

## Resto del despliegue · Confirmado por la madre

- `/tabaibi/` y `/en/tabaibi/` en 200; `/` y `/garaticker/` en 200; ruta
  inexistente en 404.
- La home lleva GitHub en `sameAs`; `sitemap.xml` con `lastmod`
  2026-11-24; cabecera CSP real activa.

## Sin novedad

- H-M3 sigue pendiente del visto bueno de Garaticker; H-M4 (PageSpeed y
  LCP de la ayuda) sigue sin medir; P-1 a P-4 siguen para Alex.
