// Copertina della NTA, nello stile della home del sito (riquadri «Nuova / Traduzione / Aperta»).
// Inclusa da nta.typ; compilata da sola dà il PNG di copertina dell'ePub.
#let foglio = rgb("#edf3f4")
#let riga = rgb("#d0e0e5")
#let inchiostro = rgb("#17191c")
#let rubrica = rgb("#a8241c")
#let sans = "Fira Sans"
#let tessera(x, y, w, h, corpo, radius: 6mm, inset: 0mm) = place(top + left, dx: x, dy: y,
  block(width: w, height: h, stroke: 0.5pt + riga, radius: radius, inset: inset, clip: true, corpo))
#let parola(t, colore: inchiostro) = align(horizon, text(font: sans, weight: "light", size: 78pt, fill: colore, tracking: -0.02em, t))

#page(paper: "a5", margin: 0mm, fill: foglio, header: none, footer: none)[
  #tessera(-6mm, 24mm, 92mm, 54mm, pad(left: 18mm, parola[La]), radius: (right: 6mm))
  #tessera(86mm, 24mm, 50mm, 54mm, align(center + horizon, image("nta-logo-inchiostro.svg", width: 34mm)))
  #tessera(20mm, 78mm, 116mm, 54mm, pad(left: 8mm, parola[Sacra]))
  #tessera(-6mm, 132mm, 118mm, 54mm, pad(left: 18mm, parola(colore: rubrica)[Bibbia]), radius: (right: 6mm))
]
