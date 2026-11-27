# Verificación de Bing · 27-nov-2026

Subsesión «Sanchesque.com · SEO», a petición de Alex vía Gestión y
Sanchesque.com: ¿se pueden regenerar con la API el `AuthenticationCode` y
el `DnsVerificationCode` que salieron en el historial público
(`0443345`, `docs/seo/bing-2026-11-25/b_GetUserSites.json`)?

Solo investigación. No se ha llamado a la API, ni para leer ni para
escribir: la lista de sitios sale del `GetUserSites` del 25-nov que hay
en local. Los códigos no se copian aquí.

## 1. ¿La API permite regenerar los códigos?

**No.** En la documentación oficial de `IWebmasterApi` no hay ningún
método que regenere, reinicie o cambie los códigos de verificación.
Los únicos métodos relacionados son:

| Método | Descripción oficial | Enlace |
|---|---|---|
| `VerifySite(String)` | «Try to verify user site» | https://learn.microsoft.com/en-us/dotnet/api/microsoft.bing.webmaster.api.interfaces.iwebmasterapi.verifysite?view=bing-webmaster-dotnet |
| `AddSite(String)` | «Add new user site» | https://learn.microsoft.com/en-us/dotnet/api/microsoft.bing.webmaster.api.interfaces.iwebmasterapi.addsite?view=bing-webmaster-dotnet |
| `RemoveSite(String)` | «Remove user site» | https://learn.microsoft.com/en-us/dotnet/api/microsoft.bing.webmaster.api.interfaces.iwebmasterapi.removesite?view=bing-webmaster-dotnet |
| `GetUserSites()` | «Get user sites» | https://learn.microsoft.com/en-us/dotnet/api/microsoft.bing.webmaster.api.interfaces.iwebmasterapi.getusersites?view=bing-webmaster-dotnet |

Índice: https://learn.microsoft.com/en-us/dotnet/api/microsoft.bing.webmaster.api.interfaces.iwebmasterapi?view=bing-webmaster-dotnet

- La clase `Site`
  (https://learn.microsoft.com/en-us/dotnet/api/microsoft.bing.webmaster.api.interfaces.site?view=bing-webmaster-dotnet)
  incluye `AuthenticationCode` y `DnsVerificationCode`, pero la
  documentación no explica qué son, cómo se generan ni si pueden cambiar.
- Con `RemoveSite` y `AddSite` se puede quitar el sitio y volver a
  añadirlo. La documentación no dice que eso genere códigos nuevos, y se
  perderían el historial y los datos del sitio en Bing. No se recomienda
  sin una fuente oficial que lo confirme.
- Panel de Bing Webmaster Tools: no he encontrado ninguna página de
  ayuda oficial que explique cómo regenerar el código. La ayuda
  (https://www.bing.com/webmasters/help) se genera en el navegador y no
  se pudo leer. **No hay ruta de menú confirmada.** Alex tendría que
  mirar en el panel, en la configuración del sitio o la de verificación,
  si se ofrece esa opción.

## 2. Cómo está verificado cada sitio

`GetUserSites` devuelve **un solo sitio**: `https://sanchesque.com/`,
con `IsVerified: true`. La cuenta no tiene otros sitios.

Lecturas públicas del 27-nov (se ha comparado con los códigos sin
mostrarlos):

| Método de Bing | Qué se ha mirado | Resultado |
|---|---|---|
| Etiqueta meta | `<meta name="msvalidate.01">` en `https://sanchesque.com/` | no está |
| Archivo XML | `https://sanchesque.com/BingSiteAuth.xml` | 404 |
| DNS CNAME | `<código>.sanchesque.com` → `verify.bing.com` (`dig`) | no existe |
| DNS TXT | TXT de `sanchesque.com` | no contiene ninguno de los dos códigos |

En el historial de `website` nunca ha habido `msvalidate` ni
`BingSiteAuth`.

**Conclusión:** hoy no hay en público ningún rastro de los tres métodos
de Bing. La explicación más probable, **sin confirmar**, es que el sitio
se verificó importándolo de Google Search Console, porque el TXT de
Google sí está. Otra posibilidad es un registro DNS en IONOS que no se
trajo al pasar a Cloudflare el 17-nov. Lo confirma Alex en el panel de
Bing, en la configuración del sitio o la de usuarios, donde aparezca el
método de verificación.

## 3. Riesgo real y qué cambiar después

- Los códigos no dan acceso a la cuenta. Solo sirven para demostrar el
  control de un dominio, poniéndolos **en** ese dominio. Quien los vea
  no puede verificar `sanchesque.com` sin poder escribir en su web o su
  DNS. Si los pusiera en un dominio suyo, como mucho lo añadiría a
  nuestra cuenta. El riesgo es bajo.
- Los JSON ya no se siguen en git (`.gitignore`, `docs/seo/bing-*/`).
  Los códigos siguen en el historial de `0443345` y no aparecen en
  ningún `.md`.
- **Si un día se regeneran** (por el panel, porque la API no lo permite):
  - **Web:** ahora mismo no habría nada que cambiar, porque no hay meta
    ni `BingSiteAuth.xml`. Solo haría falta si se pasa a verificar por
    meta o XML (lo haría Sanchesque.com).
  - **DNS en Cloudflare:** tampoco, porque no hay CNAME ni TXT de Bing.
    Solo si se pasa a verificar por DNS (Gestión, con el sí de Alex).
  - Si la verificación es por importación de Search Console, depende
    del TXT de Google: **no se borra** `google-site-verification` del
    DNS.

## Preguntas para Alex

- **B-1.** En el panel de Bing, ¿qué método de verificación consta para
  `sanchesque.com`? ¿Hay alguna opción para regenerar el código?
- **B-2.** Con el riesgo tan bajo, ¿hace falta regenerar? Si se quiere
  borrar del historial público, la alternativa es reescribir `master`
  (lo decide Alex con Sanchesque.com).
