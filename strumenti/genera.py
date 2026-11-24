#!/usr/bin/env python3
"""Genera PDF ed ePub della NTA dai file in testo/ e da meta.json.

Uso (dalla radice del repo, con `pip install -r strumenti/requisiti.txt`):
  python strumenti/genera.py --formato lettura --revisione 26.11 --out nta.pdf
  python strumenti/genera.py --formato stampa  --revisione 26.11 --out nta-stampa.pdf
  python strumenti/genera.py --formato epub    --revisione 26.11 --out nta.epub
  python strumenti/genera.py --formato stampa  --revisione 26.11 --solo "1:1-3,19:23" --out prova.pdf

Formati: "lettura" (PDF A5, una colonna), "stampa" (PDF A5, due colonne, edizione economica, con le
presentazioni dei libri: non va nella release pubblica), "epub" (EPUB 3, copertina e indice per libri e capitoli). --solo limita a libro:capitoli (prove).
"""
import argparse
import glob
import json
import os
import re
import shutil
import sys
import tempfile

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)
SITO = "https://nta-nuova-traduzione-aperta.github.io"
REPO = "https://github.com/NTA-nuova-traduzione-aperta/bibbia"
FONT = os.path.join(QUI, "font")
FILE_TYPST = ("nta.typ", "copertina.typ", "nta-logo.svg", "nta-logo-inchiostro.svg")


def filtro(spec):
    """'1:1-3,19:23,24' -> {1: {1,2,3}, 19: {23}, 24: None}"""
    if not spec:
        return None
    out = {}
    for parte in spec.split(","):
        libro, _, caps = parte.strip().partition(":")
        libro = int(libro)
        if not caps:
            out[libro] = None
            continue
        a, _, b = caps.partition("-")
        out.setdefault(libro, set()).update(range(int(a), int(b or a) + 1))
    return out


def presentazione(file_testo, d):
    """presentazioni/NN-libro.json (la scheda dell'app), con il testo NTA del versetto chiave."""
    p = os.path.join(RADICE, "presentazioni", os.path.basename(file_testo))
    if not os.path.exists(p):
        return None
    intro = json.load(open(p, encoding="utf-8"))
    m = re.search(r"(\d+):(\d+)(?:-(\d+))?$", intro.get("keyVerse", ""))
    if m:
        c, a = int(m.group(1)), int(m.group(2))
        b = int(m.group(3) or a)
        testo = [v["x"] for v in d["verses"] if v["c"] == c and a <= v["v"] <= b]
        if testo:
            intro["keyVerseText"] = " ".join(testo)
            intro["keyVerseRef"] = f"{d['name']} {c},{a}" + (f"-{b}" if b != a else "")
    return intro


def carica(solo, senza_presentazioni=False):
    sel = filtro(solo)
    libri = []
    for f in sorted(glob.glob(os.path.join(RADICE, "testo", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if sel is not None:
            if d["book"] not in sel:
                continue
            caps = sel[d["book"]]
            if caps is not None:
                d["verses"] = [v for v in d["verses"] if v["c"] in caps]
        lib = {"book": d["book"], "name": d["name"], "abbr": d["abbr"], "verses": d["verses"]}
        intro = presentazione(f, d)
        if intro and not senza_presentazioni:
            lib["intro"] = intro
        libri.append(lib)
    return libri


def qr_svg(percorso):
    import segno

    segno.make(SITO, error="m").save(percorso, scale=1, border=0, dark="#17191c")


def prepara_typst(tmp, dati):
    for nome in FILE_TYPST:
        shutil.copy(os.path.join(QUI, nome), tmp)
    qr_svg(os.path.join(tmp, "qr-sito.svg"))
    with open(os.path.join(tmp, "dati.json"), "w", encoding="utf-8") as fh:
        json.dump(dati, fh, ensure_ascii=False)


def pdf(dati):
    import typst

    with tempfile.TemporaryDirectory() as tmp:
        prepara_typst(tmp, dati)
        return typst.compile(os.path.join(tmp, "nta.typ"), root=tmp, font_paths=[FONT])


def copertina_png():
    import typst

    with tempfile.TemporaryDirectory() as tmp:
        for nome in FILE_TYPST:
            shutil.copy(os.path.join(QUI, nome), tmp)
        return typst.compile(os.path.join(tmp, "copertina.typ"), root=tmp, font_paths=[FONT], format="png", ppi=220)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--formato", choices=["stampa", "lettura", "epub"], default="lettura")
    ap.add_argument("--revisione", required=True, help="es. 26.11")
    ap.add_argument("--out", required=True)
    ap.add_argument("--solo", help="libro:capitoli, per le prove")
    ap.add_argument("--senza-presentazioni", action="store_true", help="stampa: solo il testo biblico")
    a = ap.parse_args()

    meta = json.load(open(os.path.join(RADICE, "meta.json"), encoding="utf-8"))
    # le presentazioni dei libri per ora vanno solo nell'edizione per la stampa
    libri = carica(a.solo, a.senza_presentazioni or a.formato != "stampa")
    dati = {
        "formato": a.formato,
        "revisione": a.revisione,
        "attribuzione": meta["attribution"],
        "licenza_url": meta["license_url"],
        "numerazione": meta["numbering"],
        "libri": libri,
    }
    if a.formato == "epub":
        from epub import scrivi_epub

        with tempfile.TemporaryDirectory() as tmp:
            qr = os.path.join(tmp, "qr.svg")
            qr_svg(qr)
            scrivi_epub(a.out, dati, copertina_png(), open(qr, encoding="utf-8").read(), SITO, REPO)
    else:
        with open(a.out, "wb") as fh:
            fh.write(pdf(dati))
    n = sum(len(l["verses"]) for l in libri)
    print(f"{a.out}: {a.formato}, {len(libri)} libri, {n} versetti", file=sys.stderr)


if __name__ == "__main__":
    sys.path.insert(0, QUI)
    main()
