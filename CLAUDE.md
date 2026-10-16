# CLAUDE.md — repo `bibbia` della NTA

Testo pubblico della **NTA (Nuova Traduzione Aperta)**, CC BY-SA 4.0. Struttura e formati: `README.md`.

- I file in `testo/`, `interlineare/`, `modifiche/` e `meta.json` sono **generati** dal CMS
  (repo privato `chemickypes/bibbia-interlineare-project`, comando `npm run export:nta-repo` in
  `packages/server`). Non modificarli a mano: le correzioni passano dal CMS, che tiene lo storico
  (`verse_edits`) da cui nasce `modifiche/`.
- Stato del progetto, prossimi passi e procedura di revisione dei libri:
  `packages/server/docs/piano-nta.md` nel repo del CMS (branch `feature/revisione-nta`).
- Un commit per libro rivisto, con il numero di versetti e titoli cambiati nel messaggio.
- Mai testo di traduzioni protette da copyright (NR, CEI, ND…): la NTA deve restare CC BY-SA.
