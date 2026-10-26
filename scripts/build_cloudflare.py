#!/usr/bin/env python3
"""Publica el mismo catálogo en la raíz de Cloudflare Pages; Python 3.9+."""
import argparse
from pathlib import Path
import shutil
import tempfile
from urllib.parse import urlsplit

import build_site

SOURCE = Path(__file__).resolve().parents[1]
DEFAULT_URL = 'https://veltorastudio.pages.dev/'
BUILD_MARKER = 'Veltora Studio: salida estática de Cloudflare\n'


def public_url(value):
    parsed = urlsplit(value)
    if (parsed.scheme != 'https' or not parsed.hostname
            or parsed.username or parsed.password or parsed.port
            or parsed.path not in ('', '/') or parsed.query or parsed.fragment):
        raise argparse.ArgumentTypeError('Indica una URL HTTPS en la raíz del dominio.')
    return 'https://' + parsed.hostname.encode('idna').decode('ascii') + '/'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-url', type=public_url, default=DEFAULT_URL)
    args = parser.parse_args()
    output = SOURCE / 'dist'
    marker = output / '.veltora-build'
    if output.is_symlink() or (output.exists() and not output.is_dir()):
        raise SystemExit('dist debe ser una carpeta de salida de este proyecto.')
    if output.exists() and (not marker.is_file()
                            or marker.read_text(encoding='utf-8') != BUILD_MARKER):
        raise SystemExit('dist contiene archivos ajenos: usa una carpeta de proyecto limpia.')

    # El catálogo y los recursos originales se conservan en el repositorio.
    with tempfile.TemporaryDirectory(prefix='veltora-cloudflare-') as folder:
        staging = Path(folder)
        shutil.copytree(SOURCE / 'assets', staging / 'assets')
        build_site.STUDIO = dict(build_site.STUDIO, base_path='/',
                                 site_url=args.site_url, hosting='cloudflare')
        build_site.BASE = '/'
        build_site.PUBLIC = args.site_url
        build_site.ROOT = staging
        build_site.main()
        (staging / '.veltora-build').write_text(BUILD_MARKER, encoding='utf-8')
        # La salida anterior solo se sustituye cuando la nueva se ha generado.
        if output.exists():
            shutil.rmtree(output)
        shutil.copytree(staging, output)
    print(f'Cloudflare: {output}; web {args.site_url}; app-ads.txt en la raíz.')


if __name__ == '__main__':
    main()
