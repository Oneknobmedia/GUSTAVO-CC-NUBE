# Plantilla tienda (estilo colección Shopify / Ecomus)

Réplica de la UI de colección analizada con REA (`lifemaxdistribuidora.cl/collections/kit-super-vigilancia`, tema Ecomus 1.9.0) como plantilla de catálogo de un solo archivo.

## Uso
- Abrir `index.html` → botón **Editar catálogo**: tienda, productos, colores, importar/exportar.
- **Descargar versión final** = HTML sin editor, listo para publicar.
- Importar colección Shopify por línea de comandos:
  ```
  python3 importar_shopify.py https://TIENDA/collections/NOMBRE --reemplazar -o catalogo.html
  ```

## Incluye
Barra de aviso · cabecera con buscador · menú de colecciones · cinta animada · banner desktop/móvil · Filtrar (marca, disponibilidad, precio) · vista lista/2–6 columnas · orden · tarjeta con insignia circular, precio tachado y etiquetas · vista rápida · favoritos · carrito → pedido por WhatsApp · footer 4 columnas · barra inferior móvil.

Datos en `<script id="catdata">` (JSON). Borrador se guarda en el navegador.
