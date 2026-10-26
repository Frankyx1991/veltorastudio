# Verificación — Veltora Studio Gamer

26/10/2026. Repositorio de destino: Frankyx1991/veltorastudio, ID 1434680925. Fuente inicial: README en main, commit 2d19652a658d9cdbfd75eda1ef3835639026ab2d.

## Implementación

Portal estático en la raíz del repositorio, preparado para la ruta /veltorastudio/. Portada tecnológica/gamer, Juegos con búsqueda local, Aplicaciones, ficha de EvoPuzzle, Contacto y privacidad de la web. Datos en JSON y generador Python sin dependencias; fuentes e imágenes locales. Oxanium conserva su licencia OFL. Se respetan las preferencias de movimiento reducido.

EvoPuzzle figura en prueba cerrada y la sección de aplicaciones informa de que todavía no hay lanzamientos en el catálogo. No se inventan descargas, clientes, estadísticas ni productos publicados. Los botones de contacto abren el correo y no envían mensajes automáticamente.

## Comprobaciones

- Siete documentos HTML, con enlaces, imágenes, anclas, un H1 e identificadores únicos validados.
- JavaScript comprobado con node --check; sitemap XML válido; archivo app-ads.txt con el editor correcto.
- Script PowerShell completo: sintaxis comprobada con PowerShell 7.5.4/Linux; no ejecutado en Windows ni se han abierto ventanas del PC del usuario.
- Navegador de escritorio: portada, catálogo, búsqueda sin resultados y con mayúsculas/acentos, ficha, preguntas frecuentes y enlaces de soporte.
- Navegador en iframe de 390 px (contenido útil 375 px): portada, Aplicaciones y Contacto, sin desbordamiento horizontal.
- Iframe de 320 px (contenido útil 305 px): portada y Aplicaciones. Se reproduce y corrige un título demasiado ancho y se ajusta la navegación; scrollWidth igual a clientWidth tras la corrección.

## Publicación y límites

Al iniciar el trabajo, el nuevo repositorio contenía solo README y GitHub Pages devolvía 404. Tras subir el portal a main, la comprobación final del 26/10/2026 devuelve HTTP 200 en https://frankyx1991.github.io/veltorastudio/ y confirma el marcador gamer-20261026-1. La página pública se abre y se verifica visualmente en el navegador. No ha sido necesario completar el inicio de sesión del navegador para esta comprobación pública.

El script scripts/Configurar-Web-VeltoraStudio.ps1 guarda una copia en el PC, comprueba la identidad del repositorio, abre Settings/Pages si hace falta y verifica el marcador del sitio. La elección inicial de main y / (root) se hace en la interfaz de GitHub. El script no modifica el juego ni requiere claves incrustadas.

El archivo de AdMob en la raíz del dominio devuelve 404 tras eliminar el repositorio anterior. El nuevo proyecto contiene app-ads.txt en su propia ruta y los dos archivos mínimos de infrastructure/domain-root/ para restaurar la raíz. No se presenta el archivo de proyecto como sustituto de https://frankyx1991.github.io/app-ads.txt ni se afirma que AdMob esté verificado.

No se modifica EvoPuzzle, no se exporta un AAB y no se prueba Android en esta tarea de web.
