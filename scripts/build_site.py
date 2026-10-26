#!/usr/bin/env python3
"""Genera páginas estáticas desde el catálogo. Solo necesita Python 3.9+."""
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
STUDIO = json.loads((ROOT / 'data/studio.json').read_text(encoding='utf-8'))
CATALOG = json.loads((ROOT / 'data/catalog.json').read_text(encoding='utf-8'))
BASE = STUDIO['base_path']
PUBLIC = STUDIO['site_url']
MAIL = STUDIO['email']
PRIVACY = 'https://evopuzzle-privacidad-veltorastudio.franky91-91.chatgpt.site/'


def e(value):
    return escape(str(value), quote=True)


def put(path, text):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.rstrip() + '\n', encoding='utf-8')


def mail(subject):
    return 'mailto:' + MAIL + '?subject=' + quote(subject, safe='')


def button(url, text, primary=False):
    return f'<a class="btn{" primary" if primary else ""}" href="{e(url)}">{e(text)}<span class="arrow" aria-hidden="true">↗</span></a>'


def brand():
    return f'<a class="brand" href="{BASE}" aria-label="Veltora Studio, inicio"><img src="{BASE}assets/veltora.svg" width="41" height="41" alt=""><div><b>VELTORA</b><small>INDEPENDENT STUDIO</small></div></a>'


def page(path, title, description, body, active=''):
    nav = ''.join(f'<a href="{BASE + url}"' + (' aria-current="page"' if active == key else '') + (' class="contact-nav"' if key == 'contacto' else '') + f'>{label}</a>' for url, key, label in [('juegos/', 'juegos', 'Juegos'), ('aplicaciones/', 'aplicaciones', 'Aplicaciones'), ('#estudio', 'estudio', 'El estudio'), ('contacto/', 'contacto', 'Contacto')])
    canonical = PUBLIC + path.removesuffix('index.html')
    html = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(description)}"><meta name="theme-color" content="#080a13"><meta name="veltora-release" content="{e(STUDIO['release'])}"><title>{e(title)} · Veltora Studio</title><link rel="canonical" href="{canonical}"><meta property="og:title" content="{e(title)} · Veltora Studio"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website"><meta property="og:locale" content="es_ES"><meta property="og:url" content="{canonical}"><link rel="icon" type="image/svg+xml" href="{BASE}assets/veltora.svg"><link rel="stylesheet" href="{BASE}assets/site.css"><script src="{BASE}assets/site.js" defer></script></head>
<body><a class="skip" href="#contenido">Saltar al contenido</a><header class="topbar"><div class="wrap header-row">{brand()}<nav class="nav" aria-label="Navegación principal">{nav}</nav></div></header><main id="contenido">{body}</main><footer class="footer"><div class="wrap"><div class="footer-row"><div>{brand()}<p>Juegos que despiertan tu curiosidad.<br>Aplicaciones que van contigo.</p></div><div class="footer-links"><div><strong>EXPLORA / 01</strong><a href="{BASE}juegos/">Juegos</a><a href="{BASE}aplicaciones/">Aplicaciones</a><a href="{BASE}#estudio">El estudio</a></div><div><strong>ESTAMOS CERCA / 02</strong><a href="{BASE}contacto/">Contacto y soporte</a><a href="{BASE}privacidad/">Privacidad de la web</a><a href="{BASE}juegos/evopuzzle/#soporte">Ayuda con EvoPuzzle</a></div></div></div><div class="footer-bottom"><span>© 2026 VELTORA STUDIO</span><span>HECHO PARA JUGAR. CREADO PARA EXPLORAR.</span></div></div></footer></body></html>'''
    put(path, html)


def crumb(label, parent=None):
    middle = '' if parent is None else f'<a href="{BASE + parent[0]}">{e(parent[1])}</a><span aria-hidden="true">/</span>'
    return f'<div class="wrap breadcrumbs"><a href="{BASE}">INICIO</a><span aria-hidden="true">/</span>{middle}<span>{e(label)}</span></div>'


def tags(item):
    values = [item['genre'], item['platform']] + ([item['theme']] if item.get('theme') else [])
    return '<div class="tags">' + ''.join(f'<span>{e(value)}</span>' for value in values) + '</div>'


def product_url(item):
    return BASE + item['category'] + '/' + item['slug'] + '/'


def card(item, featured=False):
    cls = 'featured' if featured else 'catalog-card'
    tag = 'h3' if featured else 'h2'
    words = ' '.join([item['name'], item['genre'], item['platform'], item['description']])
    return f'''<article class="{cls}" data-search-text="{e(words)}"><a class="feature-art" href="{product_url(item)}" aria-label="Descubrir {e(item['name'])}"><img src="{BASE}assets/{e(item['cover'])}" width="675" height="1200" alt="Portada ilustrada de {e(item['name'])}" loading="lazy"></a><div class="feature-copy"><span class="badge">{e(item['status'])} / {e(item['platform'])}</span><{tag}>{e(item['name'])}</{tag}><p class="tagline">{e(item['tagline'])}</p><p>{e(item['description'])}</p>{tags(item)}<a class="text-link" href="{product_url(item)}">DESCUBRIR {e(item['name'].upper())}<span aria-hidden="true">↗</span></a></div></article>'''


def validate():
    seen = set()
    assert BASE.startswith('/') and BASE.endswith('/')
    assert PUBLIC.startswith('https://') and PUBLIC.endswith('/')
    for item in CATALOG:
        assert re.fullmatch(r'[a-z0-9-]+', item['slug']), 'Slug no válido'
        assert item['category'] in ['juegos', 'aplicaciones']
        key = item['category'] + '/' + item['slug']
        assert key not in seen, 'Producto duplicado'
        seen.add(key)
        for field in ['privacy_url', 'deletion_url']:
            if item.get(field):
                assert urlsplit(item[field]).scheme == 'https', field
        for name in [item['cover']] + [shot['file'] for shot in item.get('screenshots', [])]:
            assert Path(name).name == name and (ROOT / 'assets' / name).is_file(), name


def home():
    game = next(item for item in CATALOG if item['slug'] == STUDIO['featured_product'])
    body = f'''<div class="wrap"><section class="hero" aria-labelledby="hero-title"><div class="hero-copy"><div class="eyebrow">INDEPENDIENTE POR NATURALEZA</div><h1 id="hero-title">CREAMOS<br>TU PRÓXIMO<br><span class="neon">UNIVERSO.</span></h1><p class="lead">Juegos que ponen a prueba tu ingenio. Aplicaciones que simplifican tu día. Una misma forma de crear: Veltora Studio.</p><div class="actions">{button(BASE+'juegos/', 'EXPLORAR JUEGOS', True)}{button(BASE+'aplicaciones/', 'VER APLICACIONES')}</div><div class="subline"><span>JUEGOS + APPS</span><i aria-hidden="true"></i><span>ANDROID</span><i aria-hidden="true"></i><span>IDEAS PROPIAS</span></div></div><div class="hero-art"><img src="{BASE}assets/portal.svg" width="700" height="660" alt="Símbolo V de Veltora en un portal tecnológico con órbitas y fichas de números"><div class="hud" aria-hidden="true">VELTORA / CREATIVE ZONE<strong>PLAY. DISCOVER. EVOLVE.</strong></div><a class="hero-pick" href="{product_url(game)}"><img src="{BASE}assets/{game['cover']}" width="50" height="50" alt=""><div><small>ACTUALMENTE EN PRUEBAS</small><strong>{e(game['name'])}</strong></div><span class="pick-arrow" aria-hidden="true">↗</span></a></div></section>
<div class="routes"><a class="route" href="{BASE}juegos/"><span class="route-code">01 /</span><div><h2>JUEGOS</h2><p>Tu próximo reto empieza aquí.</p></div><span class="arrow" aria-hidden="true">↗</span></a><a class="route" href="{BASE}aplicaciones/"><span class="route-code">02 /</span><div><h2>APLICACIONES</h2><p>Ideas útiles. Menos complicaciones.</p></div><span class="arrow" aria-hidden="true">↗</span></a></div>
<section class="section" aria-labelledby="featured-title"><div class="section-top"><div><div class="section-id">EN EL RADAR / EVOPUZZLE</div><h2 id="featured-title">Entra en la aventura.</h2></div><p>Conoce nuestro juego de puzles y descubre cómo participar en sus pruebas.</p></div>{card(game, True)}</section>
<section class="manifesto" id="estudio" aria-labelledby="studio-title"><div><div class="eyebrow">ESTO ES VELTORA</div><h2 id="studio-title">Una idea propia.<br>Una experiencia<br><span>que se queda.</span></h2></div><div><p>Nos mueve esa sensación de descubrir algo nuevo: resolver un reto, dar con una buena idea o encontrar una herramienta que te lo pone fácil.</p><p>Somos un estudio independiente que crea juegos y aplicaciones para Android. Cuidamos los detalles y escuchamos a quienes los prueban para seguir mejorando.</p><div class="principles"><span>CURIOSIDAD</span><span>PERSONALIDAD</span><span>EVOLUCIÓN</span></div></div></section>
<section class="support-strip"><div><h2>Tu experiencia también crea.</h2><p>¿Una pregunta, una idea o algo que no funciona? Hablemos.</p></div><div class="actions">{button(BASE+'contacto/', 'CONTACTAR CON EL ESTUDIO')}</div></section></div>'''
    page('index.html', 'Juegos y aplicaciones para Android', 'Explora Veltora Studio: juegos con personalidad, aplicaciones para Android, EvoPuzzle y próximos lanzamientos.', body)


def catalog(category, title, heading, intro):
    entries = [item for item in CATALOG if item['category'] == category]
    if entries:
        singular = 'juego' if category == 'juegos' else 'aplicación'
        plural = 'juegos' if category == 'juegos' else 'aplicaciones'
        listing = f'''<div class="catalog-toolbar"><label class="search" for="buscar">Buscar {e(title.lower())}<input id="buscar" data-search data-kind="{category}" type="search" maxlength="100" placeholder="Nombre o tipo de experiencia" autocomplete="off"></label><span class="count" data-count aria-live="polite" aria-atomic="true">{len(entries)} {singular if len(entries) == 1 else plural}</span></div><div class="catalog-grid">{''.join(card(item) for item in entries)}</div><p class="no-results" data-empty role="status" hidden>No hay resultados. Prueba otro nombre o borra la búsqueda.</p>'''
    else:
        listing = f'''<div class="empty-state"><div class="empty-art" aria-hidden="true">+</div><div><span class="badge">NUEVAS IDEAS EN CAMINO</span><h2>Lo siguiente empieza<br>con una buena idea.</h2><p>Todavía no hay aplicaciones publicadas en este catálogo. Aquí aparecerán cuando estén listas, con su ficha, soporte y privacidad.</p><div class="actions">{button(BASE+'contacto/', 'CONTACTAR CON EL ESTUDIO')}</div></div></div>'''
    body = crumb(title) + f'<div class="wrap"><section class="page-intro"><div class="eyebrow">EXPLORA / {e(title.upper())}</div><h1>{heading}</h1><p class="lead">{intro}</p></section><section class="catalog-area" aria-label="Catálogo de {e(title.lower())}">{listing}</section></div>'
    page(category+'/index.html', title, intro, body, category)


def product(item):
    action = button(mail(item.get('test_subject', item['support_subject'])), 'SOLICITAR ACCESO A LAS PRUEBAS' if item.get('test_subject') else 'CONSULTAR DISPONIBILIDAD', True)
    notice = item.get('access_notice', 'Consulta en esta ficha el estado y las condiciones de acceso.')
    if item.get('store_url'):
        assert urlsplit(item['store_url']).scheme == 'https'
        action = button(item['store_url'], 'VER EN GOOGLE PLAY', True)
        notice = item.get('store_notice', 'Consulta los requisitos y condiciones en su ficha de Google Play.')
    features = ''.join(f'<li><span>0{index+1} /</span><h3>{e(feature["title"])}</h3><p>{e(feature["text"])}</p></li>' for index, feature in enumerate(item.get('features', [])))
    shots = ''.join(f'<figure><img src="{BASE}assets/{e(shot["file"])}" alt="{e(shot["alt"])}" loading="lazy"><figcaption>{e(shot["caption"])}</figcaption></figure>' for shot in item.get('screenshots', []))
    faq_html = ''.join(f'<details><summary>{e(entry["question"])}</summary><p>{e(entry["answer"])}</p></details>' for entry in item.get('faq', []))
    resources = [(mail(item['support_subject']), 'Escribir a soporte'), (item['privacy_url'], 'Política de privacidad'), (item['deletion_url'], 'Eliminar cuenta o datos')]
    links = ''.join(f'<a class="resource-link" href="{e(url)}">{e(text)}<span aria-hidden="true">↗</span></a>' for url, text in resources if url)
    experience_title = "Descubre cómo se juega." if item["category"] == "juegos" else "Descubre qué puedes hacer."
    body = crumb(item['name'], (item['category']+'/', item['category'].capitalize())) + f'''<div class="wrap"><section class="product-hero"><div><span class="badge">{e(item['status'])} / {e(item['platform'])}</span><h1>{e(item['name'])}</h1><p class="tagline">{e(item['tagline'])}</p><p class="lead">{e(item['description'])}</p>{tags(item)}<div class="actions">{action}</div><p class="fine">{e(notice)}</p></div><div class="product-visual"><img src="{BASE}assets/{e(item['cover'])}" width="675" height="1200" alt="Portada de {e(item['name'])}"></div></section><section class="section" style="padding-top:0" aria-labelledby="experience-title"><div class="eyebrow">DENTRO DE LA EXPERIENCIA</div><h2 id="experience-title">{experience_title}</h2><ul class="feature-list">{features}</ul><div class="gallery">{shots}</div></section><section class="help-grid" id="soporte"><div><h2>Antes de empezar.</h2>{faq_html}</div><div><h2>Estamos en tu equipo.</h2><p>Utiliza su apartado de asistencia o cuéntanos qué ha pasado. También puedes consultar su política y solicitar la eliminación de tus datos.</p><div class="resource-list">{links}</div></div></section></div>'''
    page(item['category']+'/'+item['slug']+'/index.html', item['name'], item['description'], body, item['category'])


def contact():
    body = crumb('Contacto') + f'''<div class="wrap"><section class="page-intro"><div class="eyebrow">ABRIMOS CONVERSACIÓN</div><h1>HAY UNA PERSONA<br>AL OTRO LADO.</h1><p class="lead">Una idea, una consulta o una partida que se ha quedado a medias. Elige el motivo y abrimos tu correo con la dirección preparada.</p></section><section class="contact-grid" aria-label="Opciones de contacto"><article class="contact-card"><div class="section-id">01 / EL ESTUDIO</div><h2>¿Qué tienes en mente?</h2><p>Para consultas generales sobre Veltora Studio, sus juegos y sus próximas aplicaciones.</p><div class="actions">{button(mail('Consulta para Veltora Studio'), 'ESCRIBIR AL ESTUDIO', True)}</div></article><article class="contact-card"><div class="section-id">02 / SOPORTE EVOPUZZLE</div><h2>Vamos a resolverlo.</h2><p>Indica qué ocurrió y qué versión del juego utilizas. También tienes asistencia dentro de EvoPuzzle.</p><div class="actions">{button(mail('Asistencia EvoPuzzle'), 'PEDIR AYUDA CON EL JUEGO')}</div></article><div><p class="fine">Puedes copiar nuestra dirección:</p><a class="contact-email" href="mailto:{MAIL}">{MAIL}</a></div></section></div>'''
    page('contacto/index.html', 'Contacto y soporte', 'Contacta con Veltora Studio y solicita ayuda o acceso a las pruebas de EvoPuzzle.', body, 'contacto')


def privacy():
    hosting = ('<p>El alojamiento de esta web utiliza Cloudflare Pages. Puedes consultar la '
               '<a href="https://www.cloudflare.com/privacypolicy/">política de privacidad de Cloudflare</a> '
               'para conocer el tratamiento de datos técnicos por parte del proveedor.</p>'
               if STUDIO.get('hosting') == 'cloudflare' else
               '<p>El alojamiento utiliza GitHub Pages. GitHub puede registrar información técnica, '
               'incluida la dirección IP, para proteger su servicio. Consulta su '
               '<a href="https://docs.github.com/es/site-policy/privacy-policies/github-general-privacy-statement">'
               'declaración de privacidad</a>.</p>')
    policy_links = ''.join(f'<p><strong>{e(item["name"])}</strong>: <a href="{e(item["privacy_url"])}">política de privacidad</a> · <a href="{e(item["deletion_url"])}">eliminar cuenta o datos</a>.</p>' for item in CATALOG)
    body = crumb('Privacidad') + f'''<div class="wrap"><section class="page-intro"><div class="eyebrow">INFORMACIÓN CLARA</div><h1>TU PRIVACIDAD<br>TIENE SU ESPACIO.</h1><p class="lead">Cada juego y aplicación tiene sus propios enlaces legales. Aquí te explicamos el uso de la web de Veltora Studio.</p></section><article class="prose"><h2>La web del estudio</h2><p>Esta web es informativa. No incorpora cuentas, compras, formularios para recoger datos, anuncios, herramientas de analítica ni cookies propias. Los recursos y tipografías se sirven desde el mismo sitio, sin proveedores externos de fuentes.</p>{hosting}<h2>Si nos escribes</h2><p>Los botones de contacto abren tu aplicación de correo. Tú decides si envías el mensaje. Utilizamos la dirección y el contenido que facilites para atender tu consulta. Evita enviar contraseñas, datos de pago u otra información innecesaria.</p><p>Responsable: Francisco Javier Ruiz Vidal, Veltora Studio, España. Contacto: <a href="mailto:{MAIL}">{MAIL}</a>.</p><h2>Juegos y aplicaciones</h2>{policy_links}<p>La política de cada producto describe sus funciones y servicios, incluidos anuncios, compras y cuentas cuando corresponda. La información de la web no sustituye esas políticas.</p><h2>Próximos lanzamientos</h2><p>Cada nuevo producto incluirá sus propios enlaces de soporte, privacidad y eliminación de datos en su ficha.</p><p>Última actualización: 26 de octubre de 2026.</p></article></div>'''
    page('privacidad/index.html', 'Privacidad', 'Privacidad de la web de Veltora Studio y enlaces de datos de sus juegos y aplicaciones.', body)


def main():
    validate()
    home()
    catalog('juegos', 'Juegos', 'EL SIGUIENTE RETO<br>TE ESTÁ ESPERANDO.', 'Explora nuestros juegos. Cada ficha reúne la experiencia, su estado actual, las capturas y la ayuda que necesitas.')
    catalog('aplicaciones', 'Aplicaciones', 'BUENAS IDEAS.<br>MENOS COMPLICACIONES.', 'Un espacio para las herramientas de Veltora Studio. Descubre nuestros lanzamientos y encuentra toda su información en un mismo lugar.')
    for item in CATALOG:
        product(item)
    contact()
    privacy()
    page('404.html', 'Página no encontrada', 'Vuelve a explorar los juegos y aplicaciones de Veltora Studio.', f'<div class="wrap"><section class="page-intro"><div class="eyebrow">ERROR / 404</div><h1>ESTA RUTA<br>NO ESTÁ EN EL MAPA.</h1><p class="lead">Vuelve al inicio para descubrir nuestros juegos y aplicaciones.</p><div class="actions">{button(BASE, "VOLVER AL INICIO", True)}</div></section></div>')
    urls = ['', 'juegos/', 'aplicaciones/', 'contacto/', 'privacidad/'] + [item['category']+'/'+item['slug']+'/' for item in CATALOG]
    put('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+PUBLIC+url+'</loc></url>' for url in urls)+'</urlset>')
    put('robots.txt', 'User-agent: *\nAllow: /\nSitemap: '+PUBLIC+'sitemap.xml')
    put('app-ads.txt', 'google.com, pub-1246957925783081, DIRECT, f08c47fec0942fa0')
    put('.nojekyll', '')
    print(f'Generadas {len(urls)} páginas del catálogo y 404; {len(CATALOG)} producto(s).')


if __name__ == '__main__':
    main()
