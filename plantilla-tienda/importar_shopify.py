#!/usr/bin/env python3
"""Importa colecciones de Shopify a la plantilla de catálogo.

Uso:
  python3 importar_shopify.py URL_COLECCION [URL_COLECCION ...] [-p plantilla.html] [-o salida.html] [--reemplazar]

Ej:
  python3 importar_shopify.py https://tienda.cl/collections/kit-super-vigilancia -o mi-catalogo.html
"""
import argparse, html, json, re, sys, urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (catalogo-importador)"}
BLOCK = re.compile(r'(<script id="catdata" type="application/json">)(.*?)(</script>)', re.S)


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def texto(h):
    h = re.sub(r"<(br|/p|/li|/h\d)\s*/?>", "\n", h or "", flags=re.I)
    t = html.unescape(re.sub(r"<[^>]+>", "", h)).replace("\xa0", " ")
    return re.sub(r"\s*\n\s*", "\n", re.sub(r"[ \t]+", " ", t)).strip()[:1500]


def coleccion(url):
    base = url.split("?")[0].rstrip("/")
    if "/collections/" not in base:
        sys.exit(f"URL sin /collections/: {url}")
    handle = base.rsplit("/", 1)[-1]
    try:
        nombre = get(base + ".json")["collection"]["title"]
    except Exception:
        nombre = handle.replace("-", " ").title()
    prods, page = [], 1
    while True:
        lote = get(f"{base}/products.json?limit=250&page={page}").get("products", [])
        prods += lote
        if len(lote) < 250:
            break
        page += 1
    out = []
    for i, p in enumerate(prods):
        vs = p.get("variants") or [{}]
        v = next((x for x in vs if x.get("available")), vs[0])
        price, old = float(v.get("price") or 0), float(v.get("compare_at_price") or 0)
        av = any(x.get("available") for x in vs)
        ims = [im["src"] for im in p.get("images", [])][:8]
        out.append({"id": f"s{p['id']}", "title": p["title"], "vendor": p.get("vendor", ""),
                    "price": price, "old": old if old > price else 0, "img": ims[0] if ims else "",
                    "imgs": ims[1:], "badge": "" if av else "Bajo Pedido", "stock": av,
                    "pills": [], "desc": texto(p.get("body_html"))})
    print(f"{nombre}: {len(out)} productos", file=sys.stderr)
    return {"id": f"c{handle[:20]}", "name": nombre, "desc": "", "hero": "", "heroM": "", "products": out}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="+")
    ap.add_argument("-p", "--plantilla", default=str(Path(__file__).with_name("index.html")))
    ap.add_argument("-o", "--salida", default="catalogo.html")
    ap.add_argument("--reemplazar", action="store_true", help="borra las colecciones de ejemplo")
    a = ap.parse_args()
    src = Path(a.plantilla).read_text(encoding="utf-8")
    m = BLOCK.search(src) or sys.exit("La plantilla no tiene <script id=\"catdata\">")
    d = json.loads(m.group(2))
    cats = [coleccion(u) for u in a.urls]
    d["cats"] = cats if a.reemplazar else d.get("cats", []) + cats
    d["stamp"] = "imp" + str(abs(hash(json.dumps(cats))))[:8]
    data = json.dumps(d, ensure_ascii=False).replace("<", "\\u003c")
    Path(a.salida).write_text(src[:m.start(2)] + data + src[m.end(2):], encoding="utf-8")
    print(f"Listo: {a.salida}", file=sys.stderr)


if __name__ == "__main__":
    main()
