# website — Sanchesque Studios

Web de Sanchesque Studios, en español e inglés al mismo nivel, servida
por GitHub Pages en [sanchesque.com](https://sanchesque.com/) y
[sanchesque.com/en/](https://sanchesque.com/en/).

## Identidad visual

Fuente de verdad: el repo `sanchesque/brand` (`DESIGN.md`, tokens y
logos). Esta web solo sirve copias generadas. Resumen operativo:

- **Marca:** Sanchesque Studios — estudio creativo digital con base en
  las Islas Canarias. Voz: creativa, clara, cercana y segura.
- **Idea central:** creatividad con carácter propio.
- **Logotipo:** símbolo orgánico que recuerda a una chola, o un skate
  saltando (el «skatechola» de la historia del nombre)
  + nombre en minúsculas. En esta web se usan:
  - `img/brand/sanchesque-primary-black.svg` — **versión principal** (símbolo sobre el
    nombre), vectorial, como acento del hero. Nunca por debajo de 160 px
    de ancho en pantalla y sin alterar proporciones.
  - Versión **tipográfica** ("sanchesque" + "studios") en header y
    footer, la única permitida sin el símbolo.
  - `img/brand/favicon.svg` / `favicon.ico` / `apple-touch-icon.png` — favicons.
- **Paleta (monocroma):** negro `#000000`, blanco `#FFFFFF`, gris
  carbón `#222222`, gris claro `#F2F2F2`. Sin acentos de color salvo
  decisión deliberada posterior.
- **Tipografía:** una familia, **Manrope** (700 titulares, 600
  subtítulos, 400 cuerpo). Máximo dos familias en cualquier pieza.
- **Reglas rápidas:** no estirar, girar, separar ni recolorear el logo;
  área de seguridad alrededor del logotipo equivalente a la altura de la
  "s"; contraste alto siempre; el símbolo aparece una vez como acento,
  no como patrón.

**Copia maestra del logo:** repo `sanchesque/brand`, carpeta
`logos/sanchesque/` (SVG en contornos, PNG a 250/500/1000 px, favicons
y los originales de 2022 en CDR, EPS, PDF y Sketch). Para cualquier uso
nuevo, partir de ahí — no redibujar el símbolo.

## Estructura

- `index.html` — home en español (`/`)
- `en/index.html` — home en inglés (`/en/`); se escribe pensando en quien
  lo lee en inglés, no se traduce palabra por palabra (brand DESIGN.md §13)
- `scripts/lang.js` — selector de idioma: recuerda la elección del
  visitante y, si eligió inglés, lo lleva a `/en/` al volver a `/`
- `styles/brand/sanchesque.css` — tokens de la marca (copia de `brand/dist/`, no editar)
- `styles/site.css` — capa propia de la web: escala editorial y componentes
- `img/brand/` — logo y favicons (copias de `brand/logos/`, no editar)
- `scripts/sync_brand.sh` — refresca las copias desde `../brand`

## Despliegue

GitHub Actions (`.github/workflows/pages.yml`) publica en Pages con cada
push a `master`.
