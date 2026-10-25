# Análisis técnico: lifemaxdistribuidora.cl

Fecha: 25-10-2026. Método: REA (captura de navegador con red, consola y workers: home → colección → producto → agregar al carrito → búsqueda → carrito), descarga y lectura del JS del tema, endpoints públicos de Shopify y capturas de pantalla.

Etiquetas: **[Obs]** = observado en el tráfico o en el código. **[Inf]** = deducción. **[?]** = no verificado.

---

## 1. Resumen

| Capa | Qué usa |
|---|---|
| Plataforma | **Shopify** (Online Store 2.0). Tienda `lifemax-distribuidora.myshopify.com` [Obs] |
| Tema | **Ecomus 1.9.0**, de The4 / HDT. No viene de la tienda de temas de Shopify (`theme_store_id: null`). Copia llamada "Mayorista Plantilla final con cambios LifeMax-20" [Obs] |
| CDN / borde | **Cloudflare** delante de Shopify (`server: cloudflare`, `cf-ray`, HTTP/3) [Obs] |
| Backend | El de Shopify. **No tienen servidor propio**: no apareció ninguna API propia en el tráfico [Obs]. Lo personalizado vive en Liquid (secciones del tema), JS del navegador y apps de Shopify |
| Catálogo | 3.123 productos publicados, 231 colecciones, moneda CLP, envío solo a Chile [Obs `/meta.json`] |
| Checkout | Checkout de Shopify (se precarga desde la home) + Mercado Pago, Flow, transferencia y efectivo [Obs iconos y scripts] |
| Despacho | App **Blue Express** (puntos PUDO, región/comuna en el carrito) + lógica propia "Flash / Express" [Obs] |

---

## 2. Infraestructura y hosting

- Dominio → Cloudflare → Shopify (`powered-by: Shopify`, `server-timing` con `theme;desc="164084121850"`) [Obs].
- Archivos estáticos del tema: `lifemaxdistribuidora.cl/cdn/shop/t/21/assets/*` (CDN de Shopify detrás del mismo dominio) [Obs].
- Imágenes: `cdn.shopify.com/s/files/1/0607/7231/9482/...` [Obs].
- CSP mínima: `frame-ancestors 'none'; upgrade-insecure-requests` [Obs].
- Mapa del sitio de Shopify: productos (4 archivos), colecciones, páginas, blogs y `sitemap_agentic_discovery.xml` [Obs].
- JS del tema: módulos ES con importmap (`vendor`, `global`, `photoswipe`, `dayjs`) y polyfill `es-modules-shim` [Obs].
- Un script de carga diferida (`_spt_delay_keywords`) retrasa gtag, fbq, TikTok, Hotjar y otros para mejorar la velocidad [Obs].

---

## 3. Páginas (plantillas)

| Ruta | Plantilla | Secciones principales |
|---|---|---|
| `/` | index | carrusel de banners, 2 cintas animadas (marcas y mensajes), banner hero, 5 productos destacados, colección con descuento y cuenta regresiva, pestañas de colecciones, imagen con texto, beneficios ("Somos tienda física"), stories en video (Storista), mapa de tienda |
| `/collections/:handle` | collection | banner, título, filtros, ordenar, selector de 1 a 6 columnas, grilla, paginación o "cargar más" |
| `/products/:handle` | product | migas, galería con miniaturas y zoom (PhotoSwipe), etiquetas, SKU, precio, marca, variantes, barra de stock, "X vendidos" (falso, ver §8), aviso Flash/Express, cantidad, agregar al carrito, comprar ahora, favoritos, garantía extendida, cotización corporativa, recomendado, medios de pago, Blue Express, compartir, devoluciones/garantía, pestañas, relacionados, vistos recientemente, botón fijo de compra |
| `/cart` | cart | envío a domicilio o Retiro Punto Blue, recomendados, cuenta regresiva (ver §8), líneas, nota, región/comuna, boleta/factura, pagar, relacionados, vistos |
| `/search` | search | resultados con los mismos filtros; también la usan comparar, vistos y vista rápida (`?view=`) |
| `/pages/*` | page | 15 páginas: contacto, términos, partners, distribuidores oficiales (Hikvision, Master G, Maxell, Apple), servicio técnico, trabaja con nosotros, catálogos, bundles, lista de colecciones, data-sale-opt-out |
| `/blogs/*` | blog | 2 blogs con poco contenido |
| Mi Cuenta | — | `customer_authentication/redirect` → **cuentas de cliente nuevas de Shopify** (login sin contraseña, alojado por Shopify) [Obs] |

Elementos globales: barra de aviso, header fijo con buscador, menú con submenús diferidos (`hdt-lazy-submenu`), carrito lateral, comparar lateral, barra inferior móvil, volver arriba, chat Wizybot.

---

## 4. Componentes del tema (Web Components)

El tema no usa React: son **Custom Elements nativos** [Obs]:
- `global.min.js` define 82 (`hdt-*`, `wrapp-*`).
- `custom.js` define 32.
- `facets.min.js` define 6.

| Componente | Función |
|---|---|
| `hdt-sticky-header`, `hdt-header-menu`, `hdt-lazy-submenu` | header fijo; los submenús se cargan al abrirse |
| `hdt-predictive-search` | buscador con sugerencias |
| `hdt-marquee` | cintas animadas |
| `hdt-slider`, `hdt-slideshow`, `hdt-scrollsnap`, `hdt-slider-thumb/sync/lazy` | carruseles |
| `hdt-card-product`, `hdt-badge`, `hdt-price`, `hdt-compare-at-price` | tarjeta de producto |
| `hdt-tmp-quick` | vista rápida |
| `hdt-product-media`, `wrapp-open-pswp-*`, `hdt-gallery-modal` | galería y zoom |
| `hdt-variant-picker`, `hdt-variant-live`, `hdt-variant-inventory`, `hdt-unit-price` | variantes, stock y precio unitario |
| `wrapp-hdt-pr-frm`, `hdt-buy-buttons`, `hdt-qty-price`, `hdt-quantity-wrapp` | formulario de compra |
| `hdt-sticky-btn-atc` | barra fija "Agregar al carrito" |
| `hdt-cart-drawer`, `wrapp-hdt-cart-form`, `hdt-cart-count`, `hdt-cart-note`, `wrapp-remove-item-oncart` | carrito lateral |
| `hdt-shipping-calculator`, `hdt-country-province-selector` | estimador de envío |
| `hdt-facet-filters-form`, `hdt-price-range`, `hdt-popover-sorting` | filtros y orden |
| `hdt-wishlist*`, `hdt-compare*`, `offcanvas-compare` | favoritos y comparar |
| `product-recommendations`, `product-recently` | relacionados y vistos recientemente |
| `hdt-countdown*`, `countdown-timer`, `cart-countdown` | cuentas regresivas |
| `flash-sold`, `number-random`, `order-delivery` | "X vendidos", número aleatorio, fecha estimada |
| `hdt-pickup-availability` | retiro en tienda por variante |
| `sys-newsletter`, `sys-cookies`, `sys-exit` | popups de newsletter, cookies y salida |
| `ins-feed-api` | feed de Instagram (Graph API) |

---

## 5. Qué hace cada botón

Todo pasa por la **Ajax API** y la **Section Rendering API** de Shopify: el servidor devuelve HTML de la sección ya renderizado y el JS lo inserta en la página.

| Acción | Qué hace | Endpoint |
|---|---|---|
| Escribir en el buscador | sugerencias en vivo; guarda en caché por término y cancela la petición anterior | `GET /search/suggest?q=…&section_id=…` [Obs código]; versión JSON: `/search/suggest.json` [Obs] |
| Enviar búsqueda | resultados | `GET /search?q=` |
| Mi Cuenta | redirige al login de Shopify | `/customer_authentication/redirect` |
| ♡ Favoritos (visitante) | guarda IDs en `localStorage["theme4:wishlist:id"]`, máximo 50 | — [Obs código] |
| ♡ Favoritos (con sesión) | guarda en la cuenta, máximo 100 | `POST/DELETE /apps/ecomrise/wishlist` (proxy de app) [Obs código] |
| ⇄ Comparar | `localStorage["theme4:compare:id"]`, máximo 6; abre un panel lateral | `GET /search?view=compare&q=id:…&section_id=compare-offcanvas`; con sesión `/apps/ecomrise/compare` |
| Icono carrito | abre el carrito lateral | refresco: `GET /?section_id=<cart-drawer>` |
| **Agregar al carrito** | envía el formulario y pide en la misma respuesta las secciones a actualizar (carrito lateral, contador); emite el evento `cart:change` | `POST /cart/add.js` con `sections=` [Obs red + código] |
| +/− cantidad o Eliminar | cambia la línea | `POST /cart/change.js {line, quantity, sections}` |
| Nota de pedido | se guarda al escribir | `POST /cart/update.js {note}` |
| Comprar ahora | checkout dinámico de Shopify | `shopify-accelerated-checkout` → `/checkouts/…` |
| Vista rápida | descarga la configuración del producto una vez y la guarda en `sessionStorage` | `GET /products/:handle?view=only_config`, `GET /products/:handle.js` |
| Cambiar variante | cambia `?variant=`, precio, stock y botón | disponibilidad de retiro: `GET /variants/:id?section_id=pickup-availability` |
| Filtrar (marca, disponibilidad, precio) | parámetros nativos de Search & Discovery | `filter.p.vendor`, `filter.v.availability`, `filter.v.price.gte/lte`, `sort_by` + `section_id` |
| Selector de columnas | **guarda la preferencia como atributo del carrito** | `POST /cart/update.js {attributes:{products_items_per_row}}` [Obs código] |
| Cargar más / paginar | agrega la página siguiente a la grilla | `GET ?page=n&section_id=` |
| Relacionados | se cargan al hacer scroll | `GET /recommendations/products?section_id&product_id&limit=10` |
| Vistos recientemente | IDs en `localStorage["theme4:recently:id"]` | `GET /search?q=id:A OR id:B&section_id=recently` |
| Estimar envío | | `POST /cart/prepare_shipping_rates.json` → `GET /cart/async_shipping_rates.json` |
| Envío a domicilio / Retiro Punto Blue / Región-Comuna | app Blue Express; guarda atributos `blue_app_block_present`, `bx_widget_mode` | `widget-pudo.blue.cl`, `sho-plugin-customers.blue.cl` [Obs] |
| Boleta / Factura | casillas en el carrito | [Inf] se guarda como atributo del carrito; el nombre del atributo no está verificado [?] |
| Garantía extendida → Agregar | agrega un producto oculto "garantía": 15% del precio, redondeado a tramos de $10.000 (30+ variantes) | `/cart/add.js` [Obs script en línea] |
| Cotizaciones corporativas | formulario con nombre, RUT, teléfono, correo, cantidad y observaciones, enviado **desde el navegador con EmailJS** (sin backend) | EmailJS [Obs]. Muestra "ENVIADA CON ÉXITO" antes de recibir respuesta |
| Burbuja de chat | asistente de IA Wizybot | `api.wizybot.com/shops/…/widgetconfig`, `/shopifywidgetrest/outboundmessage` [Obs] |
| Compartir | WhatsApp, Twitter, Facebook, copiar enlace | `wrapp-hdt-share-btn`, `wrapp-hdt-copy-btn` |

---

## 6. Lógica Flash / Express (personalizada)

Archivos: `sameday-delivery.js` y `delivery-scheduling-manager.js`. La configuración va en JSON dentro del HTML (`#delivery-scheduling-config`), editable desde el editor del tema [Obs].

- **Express** (servicio 1): corte a las 15:00 (domingo 14:00). Mensaje: "LLEGA MAÑANA <DÍA> DURANTE EL DÍA".
- **Flash** (servicio 2): corte a las 17:00. Mensaje: "LLEGA HOY / MAÑANA ANTES DE LAS 12:30".
- Cada día tiene su propio horario de corte y mensaje. También hay feriados fijos (25/12, 01/01, 01/05) y fechas especiales.
- Feriados chilenos: consulta `api.boostr.cl/holidays.json` y, si falla, `apis.digital.gob.cl/fl/feriados/AAAA/MM/DD` [Obs].
- Muestra una cuenta regresiva hasta el corte y modales informativos (`showFlashModal`, `showExpressModal`).
- En las tarjetas de colección se ven etiquetas tipo "ENVÍO FLASH ⓘ" con explicación. [Inf] Salen de las etiquetas (tags) del producto.
- Otro componente, `order-delivery`, da una fecha estimada de 10 a 15 días para productos bajo pedido.

---

## 7. Apps y servicios externos

| Servicio | Para qué |
|---|---|
| Blue Express | despacho y puntos de retiro |
| Mercado Pago (+ huella de MercadoLibre) | pagos y antifraude |
| Wizybot | chatbot con IA |
| Omnisend | email marketing y captura de contactos |
| Shopify Forms | formularios de suscripción |
| Revie | reseñas por WhatsApp |
| Storista | stories y videos de producto en la home |
| Essential Announcement Bar | barra de aviso |
| Essential Upsell / Post-purchase | venta cruzada en carrito y después de la compra |
| Ecomrise | favoritos y comparar guardados en la cuenta (proxy `/apps/ecomrise`) |
| Tapita | SEO |
| Good Apps (product icons) | iconos o insignias en productos |
| EmailJS | envío del formulario de cotización |
| Instagram Graph API | feed de Instagram |
| Sentry | errores de JS. [Inf] Lo usa alguna app, no el tema |

**Medición:** GA4 + Google Ads (conversiones y remarketing), Google Merchant Center, Meta Pixel, TikTok Pixel, Bing UET, Ahrefs, Cloudflare Insights, y los web pixels y telemetría de Shopify (monorail, otlp) [Obs].

---

## 8. Cosas que hacen y que NO conviene copiar

1. **"🔥 X vendidos en las últimas Y horas" es falso** [Obs código `flash-sold`]: son números aleatorios (5–25 unidades, 3–24 horas) que suben solos cada 2 minutos y se guardan en `sessionStorage`. No vienen de ventas reales.
2. **La cuenta regresiva del carrito vacía el carrito** [Obs código]: "Este producto es limitado, cómpralo antes de 9m:51s". Al llegar a cero llama `cart/clear.js` y redirige al carrito.
3. La "Garantía extendida" muestra un temporizador de urgencia (15:00). [Inf] Es urgencia artificial.
4. El tema envía una verificación de licencia al proveedor (dominio, email de la tienda, código de compra) desde `custom.js` [Obs].
5. La cotización confirma "éxito" antes de saber si el correo salió, y no queda registro en un backend.

Los puntos 1 a 3 pueden considerarse publicidad engañosa frente al consumidor (en Chile, SERNAC). Recomiendo no replicarlos o usar datos reales.

---

## 9. Cómo replicarlo: opciones

| Opción | Qué es | Pros | Contras |
|---|---|---|---|
| **A. Shopify + tema propio** | tienda Shopify con tema Liquid propio (o comprar Ecomus con licencia) + apps equivalentes | igual a lo que ellos tienen; checkout, pagos y stock resueltos | mensualidad de Shopify y apps; copiar su tema modificado no corresponde: hay que construir o licenciar el propio |
| **B. Headless** | Next.js + Shopify Storefront API (o Medusa / WooCommerce como backend) en Vercel | máximo control y velocidad; ya tienes Vercel conectado | más desarrollo; integrar pagos y despacho a mano |
| **C. Catálogo estático + WhatsApp** | evolución de `plantilla-tienda/`: sin checkout, pedido por WhatsApp | barato, rápido, ya empezado | sin pago en línea, stock manual |

**Recomendación:** depende de si necesitas cobrar en línea.
- Si sí: **A** para salir rápido, o **B** si quieres un producto propio reutilizable.
- Si es para distribuidores o mayoristas que piden por WhatsApp: **C**, sumando lo útil de este análisis:
  1. Buscador con sugerencias.
  2. Filtros por marca, disponibilidad y precio.
  3. Favoritos y comparar en localStorage.
  4. Vistos recientemente.
  5. Lógica real Flash/Express con horarios de corte y feriados (`apis.digital.gob.cl`).
  6. Barra fija de compra.
  7. Cotización corporativa enviada a un endpoint real.
  8. Vista rápida.

---

## 10. Lo que no se pudo ver

- Código del servidor de Shopify, base de datos, panel de administración, reglas de inventario o precios B2B: no son accesibles desde afuera.
- El checkout por dentro: no avancé con datos personales.
- Login y cuenta de cliente.
- El flujo completo de Blue Express y del nombre del atributo boleta/factura.
- La configuración interna de las apps (Omnisend, Wizybot, Upsell).

Cobertura de la captura REA: quedaron 1.767 peticiones y 3.721 mensajes de consola. Se descartaron 1.099 eventos por el límite de memoria del capturador, entre ellos unas 257 peticiones. La lista de endpoints de §5 combina ese tráfico con la lectura del código del tema, así que puede faltar alguna llamada de apps de terceros.
