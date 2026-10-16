# NTA — Nuova Traduzione Aperta

Una traduzione italiana della Bibbia con licenza libera **CC BY-SA 4.0**: chiunque può leggerla,
copiarla, stamparla, usarla in app e siti e migliorarla, citando la fonte e pubblicando con la
stessa licenza ciò che ne deriva.

Sito: https://nta-nuova-traduzione-aperta.github.io

La NTA deriva dall'edizione italiana della [Open Translation Bible](https://openbible.uk)
([open-bible](https://github.com/OpenTranslationBible/open-bible)) ed è in revisione libro per
libro sui testi originali.

## Contenuto

| Cartella | Cosa contiene |
|---|---|
| `testo/` | Un file per libro (`41-marco.json`): titoli di sezione e versetti, uno per riga |
| `interlineare/` | Ebraico e greco parola per parola, con numero Strong, gloss inglese e italiana e allineamento al testo NTA |
| `modifiche/` | Elenco mensile delle modifiche al testo, con il motivo di ciascuna |
| `meta.json` | Licenza, attribuzione, conteggi |

### Formato di `testo/`

```json
{"book":41,"name":"Marco","abbr":"Mc","verses":[
{"c":1,"v":1,"t":"Giovanni prepara la via","p":1,"x":"Inizio del vangelo di Gesù Cristo, Figlio di Dio,"},
…
]}
```

- `c`, `v` — capitolo e versetto, nella numerazione delle Bibbie italiane
- `x` — testo del versetto; `\n` separa le righe delle parti poetiche e delle citazioni
- `t` — titolo di sezione che precede il versetto (facoltativo)
- `p` — `1` se il versetto apre un paragrafo (facoltativo)
- `n` — nota per il lettore (facoltativa): varianti dei manoscritti, scelte di traduzione; nelle edizioni stampate va a piè di pagina

### Formato di `interlineare/`

Ogni riga è un versetto: `text` è il testo originale (token separati da spazi), `words[i]` descrive
il token `i` (`s` numero Strong, `en` e `it` gloss), `al[i]` è l'indice della parola del versetto
NTA corrispondente (0 = prima parola, -1 = nessuna).

## Come cambia il testo

1. Le proposte (segnalazioni, revisori, revisione assistita da un modello linguistico confrontando
   ogni versetto con la Berean Standard Bible e con ebraico e greco) passano da una revisione umana.
2. Le modifiche approvate entrano qui con un commit e sono elencate in `modifiche/`.
3. A intervalli regolari esce una versione (`vAAAA.MM`) con il testo e i formati scaricabili.

Hai trovato un errore? [Apri una segnalazione](../../issues) indicando libro, capitolo e versetto.

## Licenza

Testo, titoli e interlineare: [CC BY-SA 4.0](LICENSE). Attribuzione suggerita:

> NTA — Nuova Traduzione Aperta, derivata dalla Open Translation Bible (edizione italiana), CC BY-SA 4.0.

Fonti e crediti: [CREDITS.md](CREDITS.md).
