#!/usr/bin/env python3
"""Genera páginas estáticas desde el catálogo. Solo necesita Python 3.9+."""
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import quote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
STUDIO = json.loads((ROOT / 'data/studio.json').read_text(encoding='utf-8'))
CATALOG = json.loads((ROOT / 'data/catalog.json').read_text(encoding='utf-8'))
BASE = STUDIO['base_path']
PUBLIC = STUDIO['site_url']
MAIL = STUDIO['email']
POLICIES = {
    'privacy': ('privacidad', 'Política de privacidad'),
    'cancellation': ('cancelacion', 'Suscripciones, cancelación y reembolsos'),
    'deletion': ('eliminar-datos', 'Eliminar cuenta o datos'),
    'terms': ('terminos', 'Términos del Servicio'),
}


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
    return canonical


def crumb(label, parent=None):
    middle = '' if parent is None else f'<a href="{BASE + parent[0]}">{e(parent[1])}</a><span aria-hidden="true">/</span>'
    return f'<div class="wrap breadcrumbs"><a href="{BASE}">INICIO</a><span aria-hidden="true">/</span>{middle}<span>{e(label)}</span></div>'


def tags(item):
    values = [item['genre'], item['platform']] + ([item['theme']] if item.get('theme') else [])
    return '<div class="tags">' + ''.join(f'<span>{e(value)}</span>' for value in values) + '</div>'


def product_path(item):
    return item['category'] + '/' + item['slug'] + '/'


def product_url(item):
    return BASE + product_path(item)


def policy_url(item, key):
    if key in item.get('documents', {}):
        return product_url(item) + POLICIES[key][0] + '/'
    return item.get(key + '_url')


def resource_list(item):
    resources = [(mail(item['support_subject']), 'Escribir a soporte')]
    resources.extend((policy_url(item, key), label) for key, (_, label) in POLICIES.items())
    links = ''.join(f'<a class="resource-link" href="{e(url)}">{e(label)}<span aria-hidden="true">↗</span></a>'
                    for url, label in resources if url)
    return f'<div class="resource-list">{links}</div>'


def is_https_url(value):
    parts = urlsplit(value)
    return parts.scheme == 'https' and bool(parts.hostname) and parts.username is None


def card(item, featured=False):
    cls = 'featured' if featured else 'catalog-card'
    tag = 'h3' if featured else 'h2'
    words = ' '.join([item['name'], item['genre'], item['platform'], item['description']])
    url = product_url(item)
    if store := item.get('store_url'):
        summary = f'<div class="actions">{button(store, "Descárgalo", True)}</div>'
        badge = item['status']
    else:
        summary = tags(item) + f'<a class="text-link" href="{url}">DESCUBRIR {e(item["name"].upper())}<span aria-hidden="true">↗</span></a>'
        badge = f'{item["status"]} / {item["platform"]}'
    tagline = f'<p class="tagline">{e(item["tagline"])}</p>' if item.get('tagline') else ''
    return f'''<article class="{cls}" data-search-text="{e(words)}"><a class="feature-art" href="{url}" aria-label="Ficha de {e(item['name'])}"><img src="{BASE}assets/{e(item['cover'])}" width="675" height="1200" alt="Portada ilustrada de {e(item['name'])}" loading="lazy"></a><div class="feature-copy"><span class="badge">{e(badge)}</span><{tag}><a href="{url}">{e(item['name'])}</a></{tag}>{tagline}<p>{e(item['description'])}</p>{summary}</div></article>'''


def validate():
    seen = set()
    assert BASE.startswith('/') and BASE.endswith('/')
    assert PUBLIC.startswith('https://') and PUBLIC.endswith('/')
    assert urlsplit(PUBLIC).path == BASE, 'La URL pública y la ruta de publicación deben coincidir'
    for item in CATALOG:
        assert re.fullmatch(r'[a-z0-9-]+', item['slug']), 'Slug no válido'
        assert item['category'] in ['juegos', 'aplicaciones']
        key = item['category'] + '/' + item['slug']
        assert key not in seen, 'Producto duplicado'
        seen.add(key)
        if item.get('store_url'):
            assert is_https_url(item['store_url']), f'{key}: store_url debe usar HTTPS'
        documents = item.get('documents', {})
        assert documents.keys() <= POLICIES.keys(), 'Tipo de documento desconocido'
        assert policy_url(item, 'privacy'), f'Falta la política de privacidad de {key}'
        for policy in POLICIES:
            field = policy + '_url'
            if item.get(field):
                assert is_https_url(item[field]), field
                assert policy not in documents, f'{key}: define una sola fuente para {policy}'
        for policy, sections in documents.items():
            assert sections, f'{key}: documento {policy} vacío'
            for section in sections:
                assert section['title'].strip() and section['paragraphs'], f'{key}: sección incompleta'
                for link in section.get('links', []):
                    assert link['label'].strip() and is_https_url(link['url']), link['url']
        for name in [item['cover']] + [shot['file'] for shot in item.get('screenshots', [])]:
            assert Path(name).name == name and (ROOT / 'assets' / name).is_file(), name


def home():
    game = next(item for item in CATALOG if item['slug'] == STUDIO['featured_product'])
    body = f'''<div class="wrap"><section class="hero" aria-labelledby="hero-title"><div class="hero-copy"><div class="eyebrow">INDEPENDIENTE POR NATURALEZA</div><h1 id="hero-title">CREAMOS<br>TU PRÓXIMO<br><span class="neon">UNIVERSO.</span></h1><p class="lead">Juegos que ponen a prueba tu ingenio. Aplicaciones que simplifican tu día. Una misma forma de crear: Veltora Studio.</p><div class="actions">{button(BASE+'juegos/', 'EXPLORAR JUEGOS', True)}{button(BASE+'aplicaciones/', 'VER APLICACIONES')}</div><div class="subline"><span>JUEGOS + APPS</span><i aria-hidden="true"></i><span>ANDROID</span><i aria-hidden="true"></i><span>IDEAS PROPIAS</span></div></div><div class="hero-art"><img src="{BASE}assets/portal.svg" width="700" height="660" alt="Símbolo V de Veltora en un portal tecnológico con órbitas y fichas de números"><div class="hud" aria-hidden="true">VELTORA / CREATIVE ZONE<strong>PLAY. DISCOVER. EVOLVE.</strong></div><a class="hero-pick" href="{product_url(game)}"><img src="{BASE}assets/{game['cover']}" width="50" height="50" alt=""><div><small>{e(game['status'].upper())}</small><strong>{e(game['name'])}</strong></div><span class="pick-arrow" aria-hidden="true">↗</span></a></div></section>
<div class="routes"><a class="route" href="{BASE}juegos/"><span class="route-code">01 /</span><div><h2>JUEGOS</h2><p>Tu próximo reto empieza aquí.</p></div><span class="arrow" aria-hidden="true">↗</span></a><a class="route" href="{BASE}aplicaciones/"><span class="route-code">02 /</span><div><h2>APLICACIONES</h2><p>Ideas útiles. Menos complicaciones.</p></div><span class="arrow" aria-hidden="true">↗</span></a></div>
<section class="section" aria-labelledby="featured-title"><div class="section-top"><h2 id="featured-title">Juego destacado</h2></div>{card(game, True)}</section>
<section class="manifesto" id="estudio" aria-labelledby="studio-title"><div><div class="eyebrow">ESTO ES VELTORA</div><h2 id="studio-title">Una idea propia.<br>Una experiencia<br><span>que se queda.</span></h2></div><div><p>Nos mueve esa sensación de descubrir algo nuevo: resolver un reto, dar con una buena idea o encontrar una herramienta que te lo pone fácil.</p><p>Somos un estudio independiente que crea juegos y aplicaciones para Android. Cuidamos los detalles y escuchamos a quienes los prueban para seguir mejorando.</p><div class="principles"><span>CURIOSIDAD</span><span>PERSONALIDAD</span><span>EVOLUCIÓN</span></div></div></section>
<section class="support-strip"><div><h2>Tu experiencia también crea.</h2><p>¿Una pregunta, una idea o algo que no funciona? Hablemos.</p></div><div class="actions">{button(BASE+'contacto/', 'CONTACTAR CON EL ESTUDIO')}</div></section></div>'''
    return page('index.html', 'Juegos y aplicaciones para Android', 'Explora Veltora Studio: juegos con personalidad, aplicaciones para Android, EvoPuzzle y próximos lanzamientos.', body)


def catalog(category, title, heading, intro):
    entries = [item for item in CATALOG if item['category'] == category]
    if entries:
        singular = 'juego' if category == 'juegos' else 'aplicación'
        plural = 'juegos' if category == 'juegos' else 'aplicaciones'
        listing = f'''<div class="catalog-toolbar"><label class="search" for="buscar">Buscar {e(title.lower())}<input id="buscar" data-search data-kind="{category}" type="search" maxlength="100" placeholder="Nombre o tipo de experiencia" autocomplete="off"></label><span class="count" data-count aria-live="polite" aria-atomic="true">{len(entries)} {singular if len(entries) == 1 else plural}</span></div><div class="catalog-grid">{''.join(card(item) for item in entries)}</div><p class="no-results" data-empty role="status" hidden>No hay resultados. Prueba otro nombre o borra la búsqueda.</p>'''
    else:
        listing = f'''<div class="empty-state"><div class="empty-art" aria-hidden="true">+</div><div><span class="badge">NUEVAS IDEAS EN CAMINO</span><h2>Lo siguiente empieza<br>con una buena idea.</h2><p>Todavía no hay aplicaciones publicadas en este catálogo. Aquí aparecerán cuando estén listas, con su ficha, soporte y privacidad.</p><div class="actions">{button(BASE+'contacto/', 'CONTACTAR CON EL ESTUDIO')}</div></div></div>'''
    body = crumb(title) + f'<div class="wrap"><section class="page-intro"><div class="eyebrow">EXPLORA / {e(title.upper())}</div><h1>{heading}</h1><p class="lead">{intro}</p></section><section class="catalog-area" aria-label="Catálogo de {e(title.lower())}">{listing}</section></div>'
    return page(category+'/index.html', title, intro, body, category)


def product(item):
    if store := item.get('store_url'):
        action = button(store, 'Descárgalo', True)
        badge = item['status']
        product_tags = ''
        notice = item.get('store_notice', '')
    else:
        action = button(mail(item.get('test_subject', item['support_subject'])), 'SOLICITAR ACCESO A LAS PRUEBAS' if item.get('test_subject') else 'CONSULTAR DISPONIBILIDAD', True)
        badge = f'{item["status"]} / {item["platform"]}'
        product_tags = tags(item)
        notice = item.get('access_notice', 'Consulta en esta ficha el estado y las condiciones de acceso.')
    tagline = f'<p class="tagline">{e(item["tagline"])}</p>' if item.get('tagline') else ''
    notice_html = f'<p class="fine">{e(notice)}</p>' if notice else ''
    features = ''.join(f'<li><span>0{index+1} /</span><h3>{e(feature["title"])}</h3><p>{e(feature["text"])}</p></li>' for index, feature in enumerate(item.get('features', [])))
    shots = ''.join(f'<figure><img src="{BASE}assets/{e(shot["file"])}" alt="{e(shot["alt"])}" loading="lazy"><figcaption>{e(shot["caption"])}</figcaption></figure>' for shot in item.get('screenshots', []))
    faq_html = ''.join(f'<details><summary>{e(entry["question"])}</summary><p>{e(entry["answer"])}</p></details>' for entry in item.get('faq', []))
    experience = ''
    if features or shots:
        experience_title = 'Capturas' if not features else 'Descubre la experiencia'
        feature_list = f'<ul class="feature-list">{features}</ul>' if features else ''
        gallery = f'<div class="gallery">{shots}</div>' if shots else ''
        experience = f'<section class="section" style="padding-top:0" aria-labelledby="experience-title"><h2 id="experience-title">{experience_title}</h2>{feature_list}{gallery}</section>'
    faq_section = f'<div><h2>Antes de empezar</h2>{faq_html}</div>' if faq_html else ''
    body = crumb(item['name'], (item['category']+'/', item['category'].capitalize())) + f'''<div class="wrap">
<section class="product-hero"><div><span class="badge">{e(badge)}</span><h1>{e(item['name'])}</h1>{tagline}<p class="lead">{e(item['description'])}</p>{product_tags}<div class="actions">{action}</div>{notice_html}</div><div class="product-visual"><img src="{BASE}assets/{e(item['cover'])}" width="675" height="1200" alt="Portada de {e(item['name'])}"></div></section>
{experience}
<section class="help-grid" id="soporte">{faq_section}<div><h2>Soporte y políticas</h2>{resource_list(item)}</div></section></div>'''
    return page(product_path(item) + 'index.html', item['name'], item['description'], body, item['category'])


def policy_page(item, key, sections):
    slug, label = POLICIES[key]
    title = f'{label} de {item["name"]}'
    body = crumb(label, (product_path(item), item['name'])) + f'''<div class="wrap"><section class="page-intro"><div class="eyebrow">{e(item['name'])}</div><h1>{e(label)}</h1></section><article class="prose">'''
    for section in sections:
        body += f'<h2>{e(section["title"])}</h2>'
        body += ''.join(f'<p>{e(paragraph)}</p>' for paragraph in section['paragraphs'])
        body += ''.join(f'<p><a href="{e(link["url"])}">{e(link["label"])}</a></p>'
                        for link in section.get('links', []))
    body += f'<div class="actions">{button(product_url(item) + "#soporte", "VOLVER AL SOPORTE DE " + item["name"].upper())}</div></article></div>'
    return page(product_path(item) + slug + '/index.html', title, title + ' · Veltora Studio', body, item['category'])


def contact():
    product_cards = ''.join(
        f'<article class="contact-card"><div class="section-id">{e(item["category"].upper())} / {e(item["platform"])}</div>'
        f'<h2><a href="{product_url(item)}">{e(item["name"])}</a></h2>{resource_list(item)}</article>'
        for item in CATALOG
    )
    body = crumb('Contacto y soporte') + f'''<div class="wrap"><section class="page-intro"><div class="eyebrow">VELTORA STUDIO</div><h1>SOPORTE Y<br>POLÍTICAS.</h1><p class="lead">Elige un juego o una aplicación para encontrar su ayuda, sus opciones de privacidad y la información sobre compras cuando corresponda.</p></section><section class="contact-grid" aria-label="Soporte y políticas por producto">{product_cards}<article class="contact-card"><div class="section-id">EL ESTUDIO</div><h2>Contacto general</h2><p>Para consultas sobre Veltora Studio y sus próximos lanzamientos.</p><div class="actions">{button(mail('Consulta para Veltora Studio'), 'ESCRIBIR AL ESTUDIO', True)}</div><a class="contact-email" href="mailto:{MAIL}">{MAIL}</a></article></section></div>'''
    return page('contacto/index.html', 'Soporte y políticas', 'Soporte, privacidad, suscripciones y condiciones de los juegos y aplicaciones de Veltora Studio.', body, 'contacto')


def privacy():
    hosting = ('<p>El alojamiento de esta web utiliza Cloudflare Pages. Puedes consultar la '
               '<a href="https://www.cloudflare.com/privacypolicy/">política de privacidad de Cloudflare</a> '
               'para conocer el tratamiento de datos técnicos por parte del proveedor.</p>'
               if STUDIO.get('hosting') == 'cloudflare' else
               '<p>El alojamiento utiliza GitHub Pages. GitHub puede registrar información técnica, '
               'incluida la dirección IP, para proteger su servicio. Consulta su '
               '<a href="https://docs.github.com/es/site-policy/privacy-policies/github-general-privacy-statement">'
               'declaración de privacidad</a>.</p>')
    policy_links = ''
    for item in CATALOG:
        links = ' · '.join(f'<a href="{e(url)}">{e(POLICIES[key][1].lower())}</a>'
                           for key in ('privacy', 'deletion') if (url := policy_url(item, key)))
        policy_links += f'<p><strong>{e(item["name"])}</strong>: {links}.</p>'
    body = crumb('Privacidad') + f'''<div class="wrap"><section class="page-intro"><div class="eyebrow">INFORMACIÓN CLARA</div><h1>TU PRIVACIDAD<br>TIENE SU ESPACIO.</h1><p class="lead">Cada juego y aplicación tiene sus propios enlaces legales. Aquí te explicamos el uso de la web de Veltora Studio.</p></section><article class="prose"><h2>La web del estudio</h2><p>Esta web es informativa. No incorpora cuentas, compras, formularios para recoger datos, anuncios, herramientas de analítica ni cookies propias. Los recursos y tipografías se sirven desde el mismo sitio, sin proveedores externos de fuentes.</p>{hosting}<h2>Si nos escribes</h2><p>Los botones de contacto abren tu aplicación de correo. Tú decides si envías el mensaje. Utilizamos la dirección y el contenido que facilites para atender tu consulta. Evita enviar contraseñas, datos de pago u otra información innecesaria.</p><p>Responsable: Francisco Javier Ruiz Vidal, Veltora Studio, España. Contacto: <a href="mailto:{MAIL}">{MAIL}</a>.</p><h2>Juegos y aplicaciones</h2>{policy_links}<p>La política de cada producto describe sus funciones y servicios, incluidos anuncios, compras y cuentas cuando corresponda. La información de la web no sustituye esas políticas.</p><h2>Próximos lanzamientos</h2><p>Cada nuevo producto incluirá sus propios enlaces de soporte, privacidad y eliminación de datos en su ficha.</p><p>Última actualización: 26 de octubre de 2026.</p></article></div>'''
    return page('privacidad/index.html', 'Privacidad', 'Privacidad de la web de Veltora Studio y enlaces de datos de sus juegos y aplicaciones.', body)


def main():
    validate()
    urls = [
        home(),
        catalog('juegos', 'Juegos', 'JUEGOS DE<br>VELTORA STUDIO.', 'Descubre nuestros juegos para Android.'),
        catalog('aplicaciones', 'Aplicaciones', 'BUENAS IDEAS.<br>MENOS COMPLICACIONES.', 'Un espacio para las herramientas de Veltora Studio. Descubre nuestros lanzamientos y encuentra toda su información en un mismo lugar.'),
        contact(),
        privacy(),
    ]
    for item in CATALOG:
        urls.append(product(item))
        for key, sections in item.get('documents', {}).items():
            urls.append(policy_page(item, key, sections))
    page('404.html', 'Página no encontrada', 'Vuelve a explorar los juegos y aplicaciones de Veltora Studio.', f'<div class="wrap"><section class="page-intro"><div class="eyebrow">ERROR / 404</div><h1>ESTA RUTA<br>NO ESTÁ EN EL MAPA.</h1><p class="lead">Vuelve al inicio para descubrir nuestros juegos y aplicaciones.</p><div class="actions">{button(BASE, "VOLVER AL INICIO", True)}</div></section></div>')
    sitemap = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for url in urls:
        ET.SubElement(ET.SubElement(sitemap, 'url'), 'loc').text = url
    ET.indent(sitemap)
    put('sitemap.xml', ET.tostring(sitemap, encoding='utf-8', xml_declaration=True).decode('utf-8'))
    put('robots.txt', 'User-agent: *\nAllow: /\nSitemap: '+PUBLIC+'sitemap.xml')
    put('app-ads.txt', 'google.com, pub-1246957925783081, DIRECT, f08c47fec0942fa0')
    put('.nojekyll', '')
    print(f'Generadas {len(urls)} páginas del catálogo y 404; {len(CATALOG)} producto(s).')


if __name__ == '__main__':
    main()
