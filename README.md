# Veltora Studio

Portal oficial del estudio, con interfaz tecnológica/gamer, categorías Juegos y Aplicaciones y fichas de producto.

Dirección de GitHub Pages: https://frankyx1991.github.io/veltorastudio/

Repositorio principal: https://github.com/Frankyx1991/veltorastudio

## Publicación en Cloudflare Pages

Se utiliza exclusivamente este repositorio, `Frankyx1991/veltorastudio`.

| Ajuste | Valor |
| --- | --- |
| Project name | `veltorastudio` |
| Production branch | `main` |
| Framework preset | `None` |
| Build command | `python scripts/build_cloudflare.py` |
| Build output directory | `dist` |
| Root directory | Vacío: raíz del repositorio |

El proyecto publicará en `https://veltorastudio.pages.dev/` después de guardar y completar el despliegue en Cloudflare. La disponibilidad no se da por confirmada hasta comprobar su resultado. Si Cloudflare asigna un nombre distinto, utilizar `python scripts/build_cloudflare.py --site-url https://NOMBRE-ASIGNADO.pages.dev/` con la dirección real del proyecto.

El constructor genera una carpeta `dist` independiente, con las rutas de recursos, enlaces, sitemap y privacidad adecuados para Cloudflare. Solo se incluyen documentos públicos y recursos del catálogo. Se conserva la configuración y el contenido de GitHub Pages en el repositorio. No se necesitan dependencias de terceros, otro repositorio ni comprar un dominio.

## Publicación en GitHub Pages

En Settings → Pages elegir **Deploy from a branch**, rama **main**, carpeta **/ (root)** y Save. El contenido está directamente en la raíz del repositorio; no hay que crear otra carpeta veltorastudio dentro. Las siguientes actualizaciones de main se publican con esa configuración. La existencia de los archivos en GitHub no acredita por sí sola que Pages esté activado.

`scripts/Configurar-Web-VeltoraStudio.ps1` es un bloque completo para Windows PowerShell 5.1: descarga una copia local, verifica la identidad del repositorio, abre los ajustes si la web aún no está publicada y comprueba el marcador de la versión. No necesita Git, tokens ni contraseñas dentro del código. La elección inicial de la rama se realiza en el navegador del propietario.

## Estructura y mantenimiento

- `data/studio.json`: identidad, dirección, contacto y producto destacado.
- `data/catalog.json`: catálogo, estado real, capturas, soporte y enlaces legales de cada producto.
- `scripts/build_site.py`: generador sin dependencias, Python 3.9 o posterior.
- `assets/site.css`, `assets/site.js`: diseño responsive y búsqueda local.
- `assets/fonts/`: Oxanium, alojada localmente, con su licencia OFL.
- `juegos/`, `aplicaciones/`: catálogos y fichas.
- `contacto/`, `privacidad/`: contacto y privacidad de la web.

Para añadir un juego o una aplicación, añadir su registro al catálogo con slug único, categoría, imágenes, estado y políticas propias; después ejecutar `python scripts/build_site.py` y guardar también los HTML generados. Ninguna descarga, estado de publicación o política se inventa a partir de proyectos privados.

EvoPuzzle figura en prueba cerrada. Aplicaciones muestra un estado vacío honesto hasta disponer de un lanzamiento. La web usa recursos locales, sin analítica, anuncios, formularios de recogida de datos ni librerías de terceros en ejecución. La búsqueda funciona en el navegador y el catálogo sigue siendo accesible sin JavaScript. Los efectos respetan la preferencia de movimiento reducido.

## AdMob y raíz del dominio

Al eliminar el antiguo repositorio de usuario se ha perdido también `https://frankyx1991.github.io/app-ads.txt`. El archivo `app-ads.txt` incluido aquí se sirve en `/veltorastudio/app-ads.txt`; esa ruta de proyecto no sustituye la raíz del dominio que necesita la detección de AdMob.

La solución elegida es publicar este mismo repositorio en Cloudflare Pages. El constructor incluye `app-ads.txt` en la raíz de `dist`, accesible en `https://veltorastudio.pages.dev/app-ads.txt` cuando termine el despliegue. Después hay que indicar la web de Cloudflare como sitio del desarrollador en la ficha de Google Play y solicitar la comprobación en AdMob.

`scripts/Restaurar-AppAds.ps1` comprueba el archivo de Cloudflare sin crear repositorios. El material antiguo de `infrastructure/domain-root/` queda como referencia histórica y no se utiliza en esta publicación. La disponibilidad del archivo y su verificación por Google son comprobaciones distintas; no se presenta AdMob como verificado sin revisar su estado.

La política de EvoPuzzle y su página de eliminación siguen en sus direcciones específicas del Site; la privacidad de la web enlaza ambas. Cada nuevo producto necesita sus propios textos legales.
