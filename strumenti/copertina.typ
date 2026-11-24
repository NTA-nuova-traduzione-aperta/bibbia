// Copertina della NTA, nello stile della home del sito (riquadri «Nuova / Traduzione / Aperta»).
// Inclusa da nta.typ; compilata da sola dà il PNG di copertina dell'ePub.
// sys.inputs.copertina: per un'edizione con una scelta di libri, le parole dei riquadri
// (JSON, es. ["Salmi", "Proverbi", "Vangeli e Atti"]); vuoto = «La Sacra Bibbia».
#let foglio = rgb("#edf3f4")
#let riga = rgb("#d0e0e5")
#let inchiostro = rgb("#17191c")
#let rubrica = rgb("#a8241c")
#let blu = rgb("#1d3f7a")
#let sans = "Fira Sans"
#let scelta = json(bytes(sys.inputs.at("copertina", default: "[]")))
#let parole = if scelta.len() > 0 { scelta } else { ("La", "Sacra", "Bibbia") }
#let tessera(x, y, w, h, corpo, radius: 6mm, inset: 0mm) = place(top + left, dx: x, dy: y,
  block(width: w, height: h, stroke: 0.5pt + riga, radius: radius, inset: inset, clip: true, corpo))
// la parola si rimpicciolisce se non sta nel riquadro (spazio utile: larghezza)
#let parola(t, utile, colore: inchiostro) = align(horizon, context {
  let prova = text(font: sans, weight: "light", size: 78pt, tracking: -0.02em, t)
  let w = measure(prova).width
  let s = if w > utile { 78pt * (utile / w) } else { 78pt }
  text(font: sans, weight: "light", size: s, fill: colore, tracking: -0.02em, t)
})

#page(paper: "a5", margin: 0mm, fill: foglio, header: none, footer: none)[
  #tessera(-6mm, 24mm, 92mm, 54mm, pad(left: 18mm, parola(parole.at(0), 64mm)), radius: (right: 6mm))
  #tessera(86mm, 24mm, 50mm, 54mm, align(center + horizon, image("nta-logo-inchiostro.svg", width: 34mm)))
  #tessera(20mm, 78mm, 116mm, 54mm, pad(left: 8mm, parola(parole.at(1), 98mm)))
  #tessera(-6mm, 132mm, 118mm, 54mm, pad(left: 18mm, parola(parole.at(2), 92mm, colore: rubrica)), radius: (right: 6mm))
  #if scelta.len() > 0 {
    place(bottom + center, dy: -9mm, text(font: sans, weight: "regular", size: 10pt, fill: blu, tracking: 0.04em)[Nuova Traduzione Aperta #h(0.4em)·#h(0.4em) Revisione #sys.inputs.at("revisione", default: "")])
  }
]
