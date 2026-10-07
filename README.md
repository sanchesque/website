# website — Sanchesque Studios

Web de sanchesque studios, servida por GitHub Pages en
[sanchesque.com](https://sanchesque.com/).

## Identidad visual

Fuente de verdad: [`DESIGN.md`](DESIGN.md). Resumen operativo:

- **Marca:** sanchesque studios — estudio creativo digital con base en
  las Islas Canarias. Voz: creativa, clara, cercana y segura.
- **Idea central:** creatividad con carácter propio.
- **Logotipo:** símbolo orgánico (pluma / pincelada / forma en movimiento)
  + nombre en minúsculas. En esta web se usan:
  - `img/sanchesque.svg` — **versión principal** (símbolo sobre el
    nombre), vectorial, como acento del hero. Nunca por debajo de 160 px
    de ancho en pantalla y sin alterar proporciones.
  - Versión **tipográfica** ("sanchesque" + "studios") en header y
    footer, la única permitida sin el símbolo.
  - `img/sanchesque_ico.ico` / `sanchesque_ico.png` — favicon / avatar.
- **Paleta (monocroma):** negro `#000000`, blanco `#FFFFFF`, gris
  carbón `#222222`, gris claro `#F2F2F2`. Sin acentos de color salvo
  decisión deliberada posterior.
- **Tipografía:** una familia, **Manrope** (700 titulares, 600
  subtítulos, 400 cuerpo). Máximo dos familias en cualquier pieza.
- **Reglas rápidas:** no estirar, girar, separar ni recolorear el logo;
  área de seguridad alrededor del logotipo equivalente a la altura de la
  "s"; contraste alto siempre; el símbolo aparece una vez como acento,
  no como patrón.

**Copia maestra del logo:** carpeta `sanchesque-logos` (fuera de este
repo) con todos los formatos: SVG, PNG (250/500 px), JPG, PDF, EPS,
CorelDRAW, Sketch e iconos. Para cualquier uso nuevo, partir de ahí —
no redibujar el símbolo.

## Estructura

- `DESIGN.md` — manual de identidad (fuente de verdad del diseño)
- `index.html` — home
- `styles/tokens.css` — tokens derivados del manual (monocromo + Manrope)
- `img/` — logotipo vectorial, PNG de respaldo y favicon

## Despliegue

GitHub Actions (`.github/workflows/pages.yml`) publica en Pages con cada
push a `master`.
