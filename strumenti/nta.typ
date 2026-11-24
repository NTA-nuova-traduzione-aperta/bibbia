// Impaginazione della NTA (PDF). Legge dati.json, scritto da genera.py.
// Formati: "stampa" (A5, due colonne, economica) e "lettura" (A5, una colonna).

#let D = json("dati.json")
#let F = D.formato
#let stampa = F == "stampa"
#let blu = rgb("#1d3f7a")
#let rosso = rgb("#a6231d")

#let corpo = if stampa { 8.4pt } else { 10.5pt }
#let colonne = if stampa { 2 } else { 1 }

#set document(title: "La Sacra Bibbia · Nuova Traduzione Aperta · " + D.revisione, author: "NTA — Nuova Traduzione Aperta")
#set text(font: ("Libertinus Serif", "Noto Serif Hebrew"), lang: "it", size: corpo, hyphenate: true)
// le parole ebraiche non vanno spezzate a fine riga
#show regex("[\u{0590}-\u{05FF}]+( [\u{0590}-\u{05FF}]+)*"): it => box(it)
#set par(justify: true, leading: if stampa { 0.5em } else { 0.62em }, spacing: if stampa { 0.5em } else { 0.7em })

// ---------- Pagine iniziali, senza intestazione ----------
#set page(paper: "a5", margin: 18mm, header: none, footer: none)

#include "copertina.typ"
#if stampa { page[] }

// Frontespizio
#page[
  #set align(center)
  #v(38mm)
  #text(size: 20pt, fill: blu)[La Sacra Bibbia]
  #v(4mm)
  #text(size: 12pt)[Nuova Traduzione Aperta]
  #v(2mm)
  #text(size: 9.5pt, fill: luma(90))[Revisione #D.revisione]
  #v(1fr)
  #image("nta-logo.svg", width: 18mm)
]

// Colophon
#page[
  #set text(size: 8pt)
  #set par(justify: false)
  #set par(spacing: 1.1em)
  #v(1fr)
  *NTA — Nuova Traduzione Aperta*, revisione #D.revisione. \
  #D.attribuzione

  Il testo è distribuito con licenza Creative Commons Attribuzione – Condividi allo stesso modo 4.0
  (CC BY-SA 4.0): puoi copiarlo, stamparlo, distribuirlo e modificarlo, anche per fini commerciali,
  citando la fonte e distribuendo le opere derivate con la stessa licenza.
  #link(D.licenza_url)

  Testo, storico delle modifiche e segnalazioni: \
  #link("https://github.com/NTA-nuova-traduzione-aperta/bibbia") \
  #link("https://nta-nuova-traduzione-aperta.github.io")

  #grid(columns: (auto, 1fr), gutter: 3mm, align: horizon,
    image("qr-sito.svg", width: 20mm),
    text(size: 7pt, fill: luma(90), hyphenate: false)[Inquadra il codice per aprire il sito della NTA: testo aggiornato, download e segnalazioni.])

  #D.numerazione
]

// Ringraziamento
#page[
  #set align(center + horizon)
  #set par(justify: false)
  #text(size: 12pt, style: "italic")[Al Signore.]
  #v(3mm)
  #text(size: 11pt, style: "italic")[La gloria, l'onore e la lode, tutte a Lui]
]
#if stampa { page[] }

// Indice dei libri
#page[
  #text(size: 13pt, fill: blu)[Libri della Bibbia]
  #v(4mm)
  #set text(size: if stampa { 8pt } else { 9.5pt })
  #columns(2, gutter: 6mm)[
    #context {
      for hd in query(heading.where(level: 1)) {
        let p = counter(page).at(hd.location()).first()
        link(hd.location())[#hd.body #box(width: 1fr, repeat[.#h(2pt)]) #p]
        linebreak()
      }
    }
  ]
]
#if stampa { context if calc.odd(here().page()) { page[] } }

// ---------- Testo ----------
#let marca-cap(libro, c) = [#metadata((libro: libro, c: c)) <cap>]

#let intestazione = context {
  let p = here().page()
  let tutte = query(<cap>)
  let qui = tutte.filter(m => m.location().page() == p)
  let prima = tutte.filter(m => m.location().page() < p)
  let inizio = if qui.len() > 0 and (prima.len() == 0 or qui.first().value.libro != prima.last().value.libro or qui.first().location().position().y < 30mm) { qui.first() } else if prima.len() > 0 { prima.last() } else { none }
  let fine = if qui.len() > 0 { qui.last() } else { inizio }
  if inizio == none { return }
  let a = inizio.value
  let b = fine.value
  // c = 0: pagine della presentazione del libro
  if a.c == 0 and b.c == 0 { a = (libro: a.libro, c: -1); b = a }
  else if a.c == 0 { a = (libro: b.libro, c: 1) }
  else if b.c == 0 { b = a }
  let rif = if a.c == -1 { a.libro + " · presentazione" } else if a.libro != b.libro { a.libro + " " + str(a.c) + " – " + b.libro + " " + str(b.c) } else if a.c == b.c { a.libro + " " + str(a.c) } else { a.libro + " " + str(a.c) + "–" + str(b.c) }
  set text(size: 7.5pt)
  let n = counter(page).display()
  if calc.even(p) { [#n #h(1fr) #smallcaps(rif)] } else { [#smallcaps(rif) #h(1fr) #n] }
}

#set page(
  margin: if stampa { (inside: 14mm, outside: 11mm, top: 15mm, bottom: 13mm) } else { (inside: 16mm, outside: 14mm, top: 17mm, bottom: 15mm) },
  columns: colonne,
  header: intestazione,
  header-ascent: 35%,
)
#set columns(gutter: 4.5mm)
#set footnote.entry(separator: line(length: 25%, stroke: 0.3pt), gap: 0.3em)
#show footnote.entry: set text(size: corpo * 0.85)
#show footnote.entry: set par(justify: false)

#show heading.where(level: 1): it => {
  set align(center)
  set text(size: if stampa { 15pt } else { 18pt }, weight: "regular", fill: blu)
  block(above: 2mm, below: if stampa { 5mm } else { 7mm }, it.body)
}

#let num-v(v) = box(text(size: 0.62em, weight: "bold", baseline: -0.38em)[#v])
#let num-cap(c) = box(text(size: if stampa { 14pt } else { 17pt }, weight: "bold", fill: blu, baseline: 0pt)[#c]) + "\u{2060}\u{2002}\u{2060}"
#let titolo(t) = block(above: if stampa { 0.9em } else { 1.2em }, below: 0.45em, sticky: true,
  align(center, text(weight: "bold", size: 0.95em, t)))
#let salmo(c) = block(above: 1.1em, below: 0.3em, sticky: true, align(center, text(size: 1.05em, fill: blu, smallcaps[Salmo #c])))

#let nota(v) = if "n" in v { footnote(v.n) } else { [] }

// ---------- Presentazione del libro (la scheda dell'app) ----------
#let etichetta(t) = block(above: 0.95em, below: 0.35em, sticky: true,
  text(size: 0.82em, fill: blu, tracking: 0.06em, weight: "bold", upper(t)))
#let paragrafi(t) = for p in t.split("\n\n") { par(p.trim()) }
#let presentazione(lib) = {
  let i = lib.intro
  marca-cap(lib.name, 0)
  set text(size: corpo * 0.94)
  set par(justify: true)
  if "theme" in i {
    block(below: 0.9em, align(center, text(style: "italic", size: 1.06em, i.theme)))
  }
  for (k, nome) in (("author", "Scrittore"), ("period", "Periodo di scrittura"), ("context", "Contesto"), ("summary", "Riassunto")) {
    if k in i { etichetta(nome); paragrafi(i.at(k)) }
  }
  if "keyVerseText" in i {
    etichetta("Versetto chiave")
    block(fill: rgb("#edf3f4"), inset: (x: 0.8em, y: 0.6em), radius: 2pt, width: 100%, {
      set par(justify: false)
      text(style: "italic", i.keyVerseText.replace("\n", " / "))
      linebreak()
      align(right, text(size: 0.9em, fill: luma(80), i.keyVerseRef))
    })
    if "keyVerseNote" in i { paragrafi(i.keyVerseNote) }
  }
  if "characters" in i {
    etichetta("Personaggi importanti")
    set par(justify: false, hanging-indent: 1em, spacing: 0.35em)
    for riga in i.characters.split("\n").filter(x => x.trim() != "") {
      let parti = riga.split(" — ")
      if parti.len() > 1 { par[*#parti.first()* — #parti.slice(1).join(" — ")] } else { par(riga) }
    }
  }
  if "christocentric" in i { etichetta("Visione cristocentrica"); paragrafi(i.christocentric) }
  if "outline" in i {
    etichetta("Struttura")
    set par(justify: false, spacing: 0.3em)
    grid(columns: (auto, 1fr), column-gutter: 0.8em, row-gutter: 0.35em,
      ..i.outline.split("\n").filter(x => x.trim() != "").map(riga => {
        let m = riga.match(regex("^([0-9][0-9,:–\\-]*)\\s+(.*)$"))
        if m != none { (text(weight: "bold", m.captures.at(0)), m.captures.at(1)) } else { ([], riga) }
      }).flatten())
  }
  if stampa {
    block(width: 100%, above: 1.2em, below: 1.2em, align(center, text(fill: blu, size: 1.1em)[✦]))
  } else {
    pagebreak(weak: true)
  }
}

#for lib in D.libri {
  pagebreak(weak: true, to: if stampa { none } else { none })
  let sal = lib.book == 19
  place(top + center, scope: "parent", float: true, clearance: 2mm, heading(level: 1, lib.name))
  if "intro" in lib { presentazione(lib) }
  let pezzi = ()        // paragrafo in prosa in costruzione
  let cap = 0
  for v in lib.verses {
    let nuovo-cap = v.c != cap
    let poesia = v.x.contains("\n")
    let righe = v.x.split("\n")
    // chiudi il paragrafo se serve
    if pezzi.len() > 0 and (nuovo-cap or "t" in v or "p" in v or poesia) {
      par(pezzi.join())
      pezzi = ()
    }
    if nuovo-cap {
      cap = v.c
      marca-cap(lib.name, v.c)
      if sal { salmo(v.c) }
    }
    if "t" in v { titolo(v.t) }
    let segno = if nuovo-cap and not sal { num-cap(v.c) } else { num-v(v.v) + "\u{2060}\u{202F}\u{2060}" }
    if poesia {
      block(above: 0.55em, below: 0.55em, {
        set par(justify: false, hanging-indent: 1.8em, spacing: if stampa { 0.5em } else { 0.62em })
        for (i, r) in righe.enumerate() {
          par([#h(if i == 0 { 0em } else { 0.8em })#if i == 0 { segno }#r#if i == righe.len() - 1 { nota(v) }])
        }
      })
    } else {
      pezzi.push([#segno#v.x#nota(v) ])
    }
  }
  if pezzi.len() > 0 { par(pezzi.join()) }
}
