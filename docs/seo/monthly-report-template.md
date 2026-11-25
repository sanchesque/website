# Plantilla de informe mensual SEO · sanchesque.com

Subsesión «Sanchesque.com · SEO». Una copia por mes, con fecha:
`docs/seo/monthly-AAAA-MM-DD.md`. Cada informe lleva **fecha y, si hubo
despliegue desde el anterior, su hash** (convención en `HANDOFF.md`).

## Cabecera

- Informe: `monthly-AAAA-MM-DD.md` · período: AAAA-MM a AAAA-MM
- Despliegues desde el informe anterior: hash(es) de `master`
- Ejecutado por: <sesión> · fecha: AAAA-MM-DD

## Exportes de consola (guárdalos en `admin/seo/`)

Nombres sugeridos, con fecha delante: `AAAA-MM-DD-google-paginas.zip`,
`AAAA-MM-DD-google-rastreo.zip`, `AAAA-MM-DD-bing-sitemaps.zip`.

- **Search Console › Indexación › Páginas** («Por qué no se indexan las
  páginas»): nº indexadas y nº sin indexar por motivo, con las URL de
  cada motivo si cambian.
- **Search Console › Ajustes › Estadísticas de rastreo**: % de
  respuestas 404 («No se ha encontrado») y su evolución; si sube, abrir
  el informe detallado y listar las URL (P-1).
- **Bing Webmaster Tools › Sitemaps**: estado de las tres sitemaps y
  URL descubiertas; si alguna no se ha releído, reenviarla desde ahí.

## Preguntas del mes (de la auditoría vigente)

- ¿Bajó el % de 404 de Googlebot? (H-A1: desplegado en `<hash>`;
  objetivo 2-3 semanas después). ¿Siguen las `…/help/*/sitemap.xml` en
  la lista de 404 de Search Console? (P-1)
- ¿Las 4 páginas «sin indexar» siguen igual o cambiaron de motivo? (P-2)
- ¿Hay avisos en Mejoras/datos estructurados o en Core Web Vitals? (P-4)
- ¿PageSpeed/Lighthouse ya dio cifras? (H-M4)

## Local y en vivo

- `python3 scripts/check_site.py _site` tras el último build: nº de
  páginas, errores, avisos.
- `scripts/seo_weekly.sh` (salidas en `docs/seo/live-*.txt`): ¿alguna
  alerta de L-03/L-04 durante el mes?

## Acciones

- Lo que se decide cambiar, con id del hallazgo (H-/P-/F-) y a quién
  va (madre, Garaticker, Alex).
