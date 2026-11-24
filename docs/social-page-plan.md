# Plan: página `/social/` y enlaces a GIPHY

- **Estado:** borrador del 24-nov-2026. No se construye todavía: espera
  a la Fase 1, los pasos 5 a 10 de `brand/social/plan-2026-11-24.md`,
  que hace Alex (miniaturas de Telegram, Instagram, LinkedIn y colección
  de GIPHY). Arranca cuando Alex abra LinkedIn: Marca ·
  Social pasa la URL y los textos a Marca, y Marca avisa aquí. No espera
  a GIPHY, que se añade después.
- **Origen:** dos peticiones de Marca · Social en `admin/web-backlog.md`
  (24-nov). Textos de cada red en `brand/social/copy-2026-11-24.md`; borrador de
  la página en `brand/social/social-page-2026-11-24.md`.
- **No es público:** `docs/` no está en `scripts/build_site.sh`.

## 1. Qué es

Una página bilingüe (`/social/` y `/en/social/`) con el índice de los
perfiles públicos del estudio. Es el
enlace que irá en la bio de Instagram (copy de Marca · Social).

## 2. Decidido por Alex (24-nov)

1. **Perfiles del estudio:** Instagram, Telegram y LinkedIn. WhatsApp
   Business queda fuera: Alex decidió después, en Gestión, que es «Solo
   clientes» (el número no se publica ni se enlaza; aviso de Marca).
2. **Productos sin cuentas propias:** todo va desde las cuentas del
   estudio (Alex, 24-nov). `@garaticker_bot` es solo interno y no se
   enlaza en ningún sitio; Garaticker usa el Telegram de `@sanchesque`,
   cuya línea en la página dice que trae sus paquetes. Tabaibi no tiene
   canal. Los dos salen en Instagram como destacados de `@sanchesque`.
3. **GIPHY:** entra en `/social/` el mismo día que en el pie, el
   `sameAs`, la página de Garaticker y el perfil de GitHub (D-07).
4. **Acceso:** solo desde el pie (un enlace en la fila de canales).
   No va en el menú.
5. **Textos de la página** (título, intro, una línea por perfil, es/en):
   los escribe Marca · Social y los aprueba Alex.

## 3. Lo que bloquea cada pieza

| Pieza | Estado | Desbloquea |
|---|---|---|
| La página entera | Espera a la Fase 1 | Que Alex abra LinkedIn; avisa Marca con URL y textos |
| Instagram | `https://www.instagram.com/sanchesque` (ya en el pie) | Nada |
| Telegram | `https://t.me/sanchesque` (ya en el pie) | Nada |
| LinkedIn | La página de empresa aún no existe | Que exista y su URL |
| GIPHY | Canal de marca sin aprobar | D-07 y su URL |
| Textos | Sin escribir | Marca · Social y el sí de Alex |

## 4. Cómo se construiría

- Archivos `social/index.html` y `en/social/index.html`, con la misma
  cabecera, pie, `hreflang`, canónica, Open Graph y GoatCounter que el
  resto. Carpeta nueva: añadirla a `scripts/build_site.sh` (si no, no
  se publica) y a los dos sitemaps.
- Enlaces en texto, sin iconos de terceros, con la regla monocroma de
  la marca (website-plan §4). `rel="me"` en los perfiles del estudio.
- Lo que se enlace aquí se enlaza también en el `sameAs` de la portada
  (solo perfiles del estudio) y, si encaja, en el pie.
- `check_site.py` en verde; la subsesión «Sanchesque.com · SEO» revisa
  la página antes de subirla.
- Se sube aplastado con el sí de Alex en el chat de esta sesión, y se
  comprueba en vivo.

## 5. Preguntas abiertas

1. ¿Se enlazan las tiendas de Garaticker (App Store, Google Play) en
   `/social/` cuando existan, o solo en su página?
2. Orden de los perfiles en la página.
3. ¿La página se indexa (sitemap) o lleva `noindex` por ser solo un
   índice de enlaces? Lo valora la subsesión de SEO.

Resueltas el 24-nov (Marca): qué es la Fase 1 y qué canales de producto
entran (arriba, en «Estado» y §2).
