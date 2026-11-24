#!/usr/bin/env python3
"""Pacchetti JSON della release: nta.json (tutta la Bibbia in un file, con meta), nta-libri.zip
(i file di testo/ per libro) e interlineare.zip (i file di interlineare/).

Uso: python strumenti/pacchetti.py --revisione 26.11 --dir dist
"""
import argparse
import glob
import json
import os
import zipfile

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--revisione", required=True)
    ap.add_argument("--dir", required=True)
    a = ap.parse_args()
    os.makedirs(a.dir, exist_ok=True)
    meta = json.load(open(os.path.join(RADICE, "meta.json"), encoding="utf-8"))
    meta["revisione"] = a.revisione
    testo = sorted(glob.glob(os.path.join(RADICE, "testo", "*.json")))
    libri = [json.load(open(f, encoding="utf-8")) for f in testo]
    with open(os.path.join(a.dir, "nta.json"), "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "books": libri}, fh, ensure_ascii=False, separators=(",", ":"))
    for nome, cartella in (("nta-libri.zip", "testo"), ("interlineare.zip", "interlineare")):
        with zipfile.ZipFile(os.path.join(a.dir, nome), "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(glob.glob(os.path.join(RADICE, cartella, "*.json"))):
                z.write(f, os.path.join(cartella, os.path.basename(f)))
            z.write(os.path.join(RADICE, "LICENSE"), "LICENSE")
    print("nta.json, nta-libri.zip, interlineare.zip →", a.dir)


if __name__ == "__main__":
    main()
