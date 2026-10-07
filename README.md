# website — Sanchesque Studios

Web de sanchesque studios, servida por GitHub Pages en
[sanchesque.com](https://sanchesque.com/).

## Estructura

- `DESIGN.md` — manual de identidad (fuente de verdad del diseño)
- `index.html` — home
- `styles/tokens.css` — tokens derivados del manual (monocromo + Manrope)
- `img/` — logotipo y favicon originales del estudio

## Cómo se aplica el manual

- **Paleta (§4):** solo negro/blanco/gris carbón/gris claro, sin acentos
  de color.
- **Tipografía (§5):** una familia (Manrope), jerarquía por pesos.
- **Logo (§3):** versión principal (símbolo + nombre) en el hero, nunca
  por debajo de 160 px de ancho; versión tipográfica en header y footer.
- **Acentos (§6):** el símbolo real es el único acento visual del hero.

## Despliegue

GitHub Actions (`.github/workflows/pages.yml`) publica en Pages con cada
push a `master`.
