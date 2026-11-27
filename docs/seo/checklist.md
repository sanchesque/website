# Comprobaciones SEO para `check_site.py`

Propuesta de la subsesión «Sanchesque.com · SEO» (24-nov-2026), de
`audit-2026-11-24.md`. **Implementada el 24-nov-2026 por orden de Alex
(vía Gestión): todas entran en `scripts/check_site.py`**, con estos
ajustes decididos al implementar:

- C-01 a C-14 entran como **errores** salvo la parte de `lastmod` de
  C-07, que entra como **aviso**: `lastmod` solo debe reflejar cambios
  de contenido visible (H-M1) y, con el criterio estricto de `git log`,
  falla hoy en `/legal/` y `/en/legal/` (cambiaron las cabeceras OG el
  24-nov sin tocar el contenido).
- W-01 a W-04 entran como **avisos**.
- L-01 a L-05 entran en el modo **`--live`**:
  `python3 scripts/check_site.py --live` (comprueba la web publicada
  con agente de usuario propio, H-B8; la lanza la madre a mano tras cada
  publicación).

Verificado el 24-nov sobre `_site/` y el repo: 25 páginas, 0 errores y
5 avisos (W-01 en los títulos de la ayuda, que arregla Garaticker, y
C-07 en legal). `--live` contra producción: L-01 a L-05 pasan.

---

Propuesta original (24-nov-2026), sin código. La madre decide cuáles
entran y las escribe.

Hoy `check_site.py` ya comprueba: raya larga, enlaces internos rotos,
gemelo en `/en/` y que cada página propia esté en `sitemap.xml`. Todo lo
de abajo se suma a eso, sin dependencias nuevas (biblioteca estándar,
expresiones regulares como ahora), y corre sobre `_site/` antes de cada
publicación, así que un fallo para el despliegue.

## Qué páginas mira cada comprobación

- **Propias:** las de `_site/` fuera de `GENERATED`, sin `404.html`.
- **Generadas:** la ayuda (`garaticker/help`, `en/garaticker/help`).
  Para ellas solo las marcadas «también generadas»; si fallan, el
  arreglo va a Garaticker, no se editan aquí.

## Errores (paran el despliegue)

| Id | Comprobación | Páginas | Por qué |
|---|---|---|---|
| C-01 | Una sola `<link rel="canonical">`, absoluta, `https://sanchesque.com/…/` con barra final, y igual a la URL de la propia página | propias, también generadas | Canónica mal copiada al duplicar una página es el error más fácil y más caro |
| C-02 | `hreflang` `es`, `en` y `x-default`, absolutos; la página aparece en su propio grupo; el grupo es idéntico en la página gemela (recíproco); `x-default` apunta a la versión en español; el `hreflang` de la propia página coincide con `<html lang>` | propias, también generadas | Sin reciprocidad Google ignora el par |
| C-03 | `<title>` presente, único en todo el sitio, entre 30 y 65 caracteres | propias | Hoy los más largos tienen 65; las generadas, solo aviso (W-01) |
| C-04 | `<meta name="description">` presente, única, entre 50 y 160 caracteres | propias, también generadas | Descripciones repetidas o vacías |
| C-05 | `og:title`, `og:description`, `og:url` (= canónica), `og:image` absoluta y que existe en `_site/`, `og:image:alt`, `og:locale` acorde con `lang`, `twitter:card` | propias, también generadas | Vista previa rota en redes y chats |
| C-06 | Exactamente un `<h1>`; ningún `<img>` sin `alt` (vale `alt=""` para decorativas); `<img>` con `width` y `height` | propias | Encabezados, accesibilidad y CLS |
| C-07 | Cada `<loc>` de `sitemap.xml` existe en `_site/`, tiene su `xhtml:link` con los tres `hreflang` iguales a los de la página, y el contenido visible no ha cambiado desde `lastmod`: se compara el texto de `<main>` (sin etiquetas ni espacios repetidos) de la versión vigente en esa fecha (`git rev-list -1 --before=<lastmod>T23:59 HEAD`) con el actual; cambios solo en `<head>` (Open Graph, JSON-LD, scripts) no cuentan. Si no hay git o no hay versión anterior, se salta | `sitemap.xml` | `lastmod` fiable (H-M1) y sitemap sin URL muertas |
| C-08 | Ninguna página propia ni del sitemap lleva `noindex`; `404.html` (y los de la ayuda) sí lo llevan | todas | Un `noindex` olvidado borra una página de Google |
| C-09 | `robots.txt`: no tiene ningún `Disallow` con ruta (vacío o ausente), lista las tres sitemaps y cada una existe en `_site/`; no hay bloque para GPTBot ni OAI-SearchBot | `robots.txt` | Regla fija: los robots de IA pueden leer la web |
| C-10 | Cada bloque `application/ld+json` es JSON válido; en `/` y `/en/` hay `Organization` con `@id` `https://sanchesque.com/#organization` (y `WebSite` con `#website` si se aprueba H-M2); todo `publisher.@id` apunta a ese `@id`; `logo`, `image` y `url` existen en `_site/` | propias | JSON roto pasa desapercibido |
| C-11 | Los perfiles de `sameAs` son los mismos en `/` y `/en/`; ninguno es de WhatsApp (`wa.me`, `whatsapp.com`; el del estudio es «Solo clientes») y ninguno es de GIPHY mientras D-07 siga abierto (lista de bloqueados en una constante del script) | `/`, `/en/` | Reglas fijas de la web |
| C-12 | Existen `tabaibi/index.html` y `en/tabaibi/index.html`, y su canónica es `/tabaibi/` y `/en/tabaibi/` | `/tabaibi/`, `/en/tabaibi/` | URL fijas que enlaza «powered by tabaibi» |
| C-13 | No se publica nada de `garaticker/artists` ni ninguna página de privacidad de Garaticker | `_site/` | Reglas fijas: guía para artistas y privacidad fuera |
| C-14 | Ningún enlace interno a `index.html` ni a una carpeta sin barra final | propias | Evita 307 y 301 innecesarios (H-B1) |

El 24-nov fallaban C-05 (legal sin Open Graph, H-B5), C-07 (`lastmod`,
H-M1) y C-14 si se cuentan los enlaces `./` y `../` como carpetas (no
deben contarse: solo rutas sin barra final). Los tres arreglos se
publicaron en `456ac08` y ya pasan como error, salvo la parte `lastmod`
de C-07, que quedó como aviso (ver arriba).

## Avisos (se imprimen, no paran)

| Id | Comprobación | Páginas |
|---|---|---|
| W-01 | Títulos de 30 a 65 caracteres en las generadas | generadas (H-B3) |
| W-02 | El tamaño de cada página HTML propia con su CSS y JS propios no pasa de 100 KB, y ninguna imagen de `img/` pasa de 300 KB salvo `og-image.png` | propias |
| W-03 | Un `<a target="_blank">` sin `rel="noopener"` | todas |
| W-04 | Una página propia sin enlaces internos entrantes (huérfana) aunque esté en el sitemap | propias |

## Comprobación en vivo, aparte

Lo que solo se ve con la web publicada no cabe en `check_site.py`, que
corre antes de desplegar. Propuesta: un modo opcional
(`check_site.py --live`, o un script hermano) que la madre lance a mano
después de publicar, con `curl` o `urllib` y un agente de usuario propio
(ver H-B8):

- L-01 · `http://`, `www` y carpeta sin barra dan un único 301 a la URL
  canónica.
- L-02 · Una ruta inventada da 404 con `noindex`.
- L-03 · Cada URL de las tres sitemaps da 200 sin redirección.
- L-04 · Ninguna petición que haga una página de la ayuda al cargarse
  da 404 (en concreto, `…/help/*/sitemap.xml`, H-A1). Basta con pedir
  `sitemap.xml` junto a cada URL de la ayuda que aparece en un
  `hreflang`.
- L-05 · Googlebot, Bingbot, GPTBot y OAI-SearchBot (por agente de
  usuario) reciben 200 en `/` y `/robots.txt`.

## Fuera del script, a mano

- PageSpeed Insights (móvil) de `/`, `/en/`, un producto y una página de
  la ayuda después de cambios de CSS, fuentes o imágenes; cifras en el
  informe de auditoría.
- Cada mes, o tras un cambio grande, Alex mira en Search Console
  Indexación › Páginas y Ajustes › Estadísticas de rastreo, y en Bing
  Webmaster Tools › Sitemaps. Si cambia algo, se apunta en
  `docs/seo/` con fecha.
