"""EPUB 3 della NTA, scritto direttamente (senza Pandoc): copertina, frontespizio, crediti con QR,
ringraziamento, un file per libro con indice per capitoli, note come note a comparsa (epub:type)."""
import datetime
import html
import uuid
import zipfile

NS = 'xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="it" xml:lang="it"'

CSS = """
body { font-family: serif; line-height: 1.5; margin: 0 4%; }
h1 { text-align: center; font-weight: normal; color: #1d3f7a; margin: 1.2em 0 1em; }
h2.cap { font-size: 1.6em; color: #1d3f7a; margin: 1em 0 .2em; line-height: 1; }
h2.salmo { text-align: center; font-size: 1.05em; font-variant: small-caps; color: #1d3f7a; font-weight: normal; margin: 1.4em 0 .3em; }
h3 { text-align: center; font-size: 1em; margin: 1.1em 0 .4em; }
p { margin: 0 0 .5em; text-align: justify; }
p.poesia { text-align: left; margin: 0 0 .3em; padding-left: 1.6em; text-indent: -1.6em; }
span.riga { display: block; padding-left: 2.4em; text-indent: -1.6em; }
span.riga.prima { padding-left: 1.6em; }
sup.v { font-size: .62em; font-weight: bold; font-family: sans-serif; }
a.nota { font-size: .7em; vertical-align: super; text-decoration: none; }
aside.nota { font-size: .85em; }
.centro { text-align: center; }
.dedica { text-align: center; font-style: italic; margin-top: 35%; }
.piccolo { font-size: .85em; text-align: left; }
img.qr { width: 6em; }
nav ol { list-style: none; padding-left: 1em; }
"""


def e(s):
    return html.escape(s, quote=False)


def pagina(titolo, corpo, extra_head=""):
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html {NS}><head><meta charset="utf-8"/>'
            f'<title>{e(titolo)}</title><link rel="stylesheet" href="nta.css"/>{extra_head}</head>'
            f'<body>{corpo}</body></html>')


def libro_xhtml(lib, contatore):
    sal = lib["book"] == 19
    out = [f'<section epub:type="chapter" role="doc-chapter"><h1>{e(lib["name"])}</h1>']
    note = []
    prosa = []
    cap = 0

    def chiudi():
        if prosa:
            out.append("<p>" + "".join(prosa) + "</p>")
            prosa.clear()

    for v in lib["verses"]:
        nuovo = v["c"] != cap
        poesia = "\n" in v["x"]
        if prosa and (nuovo or "t" in v or "p" in v or poesia):
            chiudi()
        if nuovo:
            cap = v["c"]
            if sal:
                out.append(f'<h2 class="salmo" id="c{cap}">Salmo {cap}</h2>')
            else:
                out.append(f'<h2 class="cap" id="c{cap}">{cap}</h2>')
        if "t" in v:
            out.append(f"<h3>{e(v['t'])}</h3>")
        num = f'<sup class="v" id="v{v["c"]}-{v["v"]}">{v["v"]}</sup> '
        rif = ""
        if "n" in v:
            contatore[0] += 1
            k = contatore[0]
            rif = f'<a class="nota" epub:type="noteref" role="doc-noteref" href="#n{k}" id="r{k}">{k}</a>'
            note.append(f'<aside class="nota" epub:type="footnote" role="doc-footnote" id="n{k}"><p>'
                        f'<a href="#r{k}">{k}</a> {e(v["n"])}</p></aside>')
        if poesia:
            righe = v["x"].split("\n")
            spans = "".join(f'<span class="riga{" prima" if i == 0 else ""}">{num if i == 0 else ""}{e(r)}'
                            f'{rif if i == len(righe) - 1 else ""}</span>' for i, r in enumerate(righe))
            out.append(f'<p class="poesia">{spans}</p>')
        else:
            prosa.append(f"{num}{e(v['x'])}{rif} ")
    chiudi()
    out.append("</section>")
    out.extend(note)
    return pagina(lib["name"], "".join(out))


def scrivi_epub(percorso, dati, copertina_png, qr_svg, sito, repo):
    rev = dati["revisione"]
    libri = dati["libri"]
    ident = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, sito + '/nta/' + rev)}"
    oggi = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    titolo = f"La Sacra Bibbia · Nuova Traduzione Aperta (revisione {rev})"

    file = {}  # nome -> (contenuto, media-type, proprietà)
    file["nta.css"] = (CSS, "text/css", None)
    file["copertina.png"] = (copertina_png, "image/png", "cover-image")
    file["qr-sito.svg"] = (qr_svg, "image/svg+xml", None)
    file["copertina.xhtml"] = (pagina("Copertina", '<div class="centro"><img src="copertina.png" alt="La Sacra Bibbia" style="max-width:100%;max-height:100%"/></div>'), "application/xhtml+xml", None)
    file["frontespizio.xhtml"] = (pagina("Frontespizio",
        f'<div class="centro" style="margin-top:30%"><h1>La Sacra Bibbia</h1><p class="centro">Nuova Traduzione Aperta</p>'
        f'<p class="centro"><small>Revisione {e(rev)}</small></p></div>'), "application/xhtml+xml", None)
    file["crediti.xhtml"] = (pagina("Crediti",
        f'<div class="piccolo"><p><b>NTA — Nuova Traduzione Aperta</b>, revisione {e(rev)}.<br/>{e(dati["attribuzione"])}</p>'
        f'<p>Il testo è distribuito con licenza Creative Commons Attribuzione – Condividi allo stesso modo 4.0 (CC BY-SA 4.0): '
        f'puoi copiarlo, stamparlo, distribuirlo e modificarlo, anche per fini commerciali, citando la fonte e distribuendo le '
        f'opere derivate con la stessa licenza. <a href="{dati["licenza_url"]}">{dati["licenza_url"]}</a></p>'
        f'<p>Testo, storico delle modifiche e segnalazioni:<br/><a href="{repo}">{repo}</a><br/><a href="{sito}">{sito}</a></p>'
        f'<p><img class="qr" src="qr-sito.svg" alt="QR code del sito della NTA"/><br/>Inquadra il codice per aprire il sito '
        f'della NTA: testo aggiornato, download e segnalazioni.</p><p>{e(dati["numerazione"])}</p></div>'),
        "application/xhtml+xml", None)
    file["dedica.xhtml"] = (pagina("Ringraziamento",
        '<div class="dedica"><p class="centro">Al Signore.</p><p class="centro">La gloria, l\'onore e la lode, tutte a Lui</p></div>'),
        "application/xhtml+xml", None)

    contatore = [0]
    nav_libri = []
    for lib in libri:
        nome = f"libro-{lib['book']:02d}.xhtml"
        file[nome] = (libro_xhtml(lib, contatore), "application/xhtml+xml", None)
        caps = sorted({v["c"] for v in lib["verses"]})
        etich = "Salmo " if lib["book"] == 19 else ""
        sotto = "".join(f'<li><a href="{nome}#c{c}">{etich}{c}</a></li>' for c in caps)
        nav_libri.append(f'<li><a href="{nome}">{e(lib["name"])}</a><ol>{sotto}</ol></li>')

    nav = pagina("Indice",
        '<nav epub:type="toc" id="toc" role="doc-toc"><h1>Indice</h1><ol>'
        '<li><a href="frontespizio.xhtml">Frontespizio</a></li><li><a href="crediti.xhtml">Crediti</a></li>'
        '<li><a href="dedica.xhtml">Ringraziamento</a></li>' + "".join(nav_libri) + "</ol></nav>"
        '<nav epub:type="landmarks" hidden=""><ol><li><a epub:type="cover" href="copertina.xhtml">Copertina</a></li>'
        f'<li><a epub:type="bodymatter" href="libro-{libri[0]["book"]:02d}.xhtml">Testo</a></li></ol></nav>')
    file["nav.xhtml"] = (nav, "application/xhtml+xml", "nav")

    ordine = ["copertina.xhtml", "frontespizio.xhtml", "crediti.xhtml", "dedica.xhtml", "nav.xhtml"] + \
             [f"libro-{l['book']:02d}.xhtml" for l in libri]
    ids = {n: "f" + str(i) for i, n in enumerate(file)}
    manifest = "".join(
        f'<item id="{ids[n]}" href="{n}" media-type="{mt}"{f" properties=\"{pr}\"" if pr else ""}/>'
        for n, (_, mt, pr) in file.items())
    spine = "".join(f'<itemref idref="{ids[n]}"{" linear=\"no\"" if n == "nav.xhtml" else ""}/>' for n in ordine)
    opf = (f'<?xml version="1.0" encoding="utf-8"?>\n<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
           f'unique-identifier="id" xml:lang="it"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
           f'<dc:identifier id="id">{ident}</dc:identifier><dc:title>{e(titolo)}</dc:title><dc:language>it</dc:language>'
           f'<dc:creator>NTA — Nuova Traduzione Aperta</dc:creator><dc:rights>CC BY-SA 4.0</dc:rights>'
           f'<dc:source>{sito}</dc:source><meta property="dcterms:modified">{oggi}</meta>'
           f'<meta name="cover" content="{ids["copertina.png"]}"/></metadata>'
           f'<manifest>{manifest}</manifest><spine>{spine}</spine></package>')

    with zipfile.ZipFile(percorso, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
                   '</rootfiles></container>', compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        for n, (c, _, _) in file.items():
            z.writestr("OEBPS/" + n, c, compress_type=zipfile.ZIP_DEFLATED)
