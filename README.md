# Veltora Studio

Portal oficial del estudio, con interfaz tecnológica/gamer, categorías Juegos y Aplicaciones y fichas de producto.

Dirección de GitHub Pages: https://frankyx1991.github.io/veltorastudio/

Repositorio principal: https://github.com/Frankyx1991/veltorastudio

## Publicación

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

`infrastructure/domain-root/` contiene únicamente el archivo de anuncios y una redirección al portal. Son los dos archivos preparados para un alojamiento mínimo en la raíz del dominio. El contenido principal y su mantenimiento permanecen en este repositorio **veltorastudio**. No se ha recreado el repositorio anterior ni se presenta la verificación de AdMob como completada.

La política de EvoPuzzle y su página de eliminación siguen en sus direcciones específicas del Site; la privacidad de la web enlaza ambas. Cada nuevo producto necesita sus propios textos legales.
