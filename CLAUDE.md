# CLAUDE.md — Studio Gregorio Manèra
## Istruzioni operative per la produzione della newsletter Substack

---

## 1. Onboarding — Come iniziare ogni nuovo articolo

**Quando l'utente richiede la creazione di un nuovo articolo**, prima di qualsiasi altra operazione poni questa domanda:

> "Vuoi descrivere brevemente la casistica o il tema che intendi trattare, oppure preferisci che valuti autonomamente il prossimo argomento in base alla strategia editoriale?"

**Percorso A — l'utente fornisce una descrizione:**
- Usa la descrizione come input principale per il tema, il caso reale e l'angolatura
- Verifica la coerenza con `strategia_contenuti.md` e con gli articoli già pubblicati (evita sovrapposizioni)
- Proponi brevemente come intendi strutturarlo e attendi conferma prima di procedere

**Percorso B — l'utente delega la scelta all'agente:**
- Leggi `strategia_contenuti.md` e l'elenco degli articoli già prodotti
- Identifica il prossimo tema non ancora coperto con il miglior rapporto tra rilevanza normativa attuale e utilità per il target (micro-PMI, condomini, privati con situazioni stratificate)
- Proponi il tema con una motivazione in 3–4 righe (perché adesso, quale caso reale disponibile, quale metodo epistemologico applicabile) e attendi conferma prima di procedere

---

## 2. Struttura standard di ogni articolo

Ogni articolo deve seguire questa struttura nell'ordine indicato:

```
# [Titolo]
*Gregorio Manèra | Dottore Commercialista · Revisore Legale · Docente*
---
> **Perché questo tema adesso** [box con 3 segnali convergenti + fonti verificate]
---
[Corpo: 4–6 sezioni con titolo ##, 150–300 parole ciascuna]
---
### Caso reale e caso simulato
  **Caso reale** [+ metodo epistemologico esplicito + ragionamento controfattuale + verifica del pattern]
  **Caso simulato** [+ metodo epistemologico esplicito + motivazione + DIAGRAMMA DI FLUSSO ASCII]
---
### Note [riferimenti numerati con fonte verificabile]
---
### Per approfondire [3 sezioni tematiche con link]
---
[Disclaimer professionale + disclosure AI (L. 132/2025)]
---
### Report di revisione accademica [vedere §4]
---
### Checklist di revisione pre-pubblicazione [vedere §5]
```

---

## 3. Requisiti epistemologici — obbligatori in ogni articolo

### 3a. Caso reale
Inserire sempre un blocco `*Metodo epistemologico applicato: [Nome] (motivazione).*` prima del ragionamento controfattuale.

- Scegliere il metodo in base al tipo di domanda analitica:
  - Domanda di attribuzione causale ex post → **Ragionamento controfattuale sistematico**
  - Domanda con output AI da validare → **Falsificazionismo applicato (Popper)**
  - Domanda di rilevazione struttura incentivi → **Analysis of Competing Hypotheses (ACH)**
- Motivare perché quel metodo è preferibile alle alternative per il caso specifico
- Non nominare un metodo senza giustificarne la scelta rispetto agli altri disponibili

### 3b. Caso simulato — TESTO + DIAGRAMMA DI FLUSSO

La verifica epistemologica del caso simulato deve essere rappresentata:
1. **Testualmente**: blocco `*Metodo epistemologico applicato: [Nome] (motivazione).*` con motivazione della scelta
2. **Visivamente**: diagramma di flusso ASCII in blocco di codice ` ``` ` immediatamente dopo il testo

**Struttura del diagramma** (adattare al metodo):

Per **Backward Induction**:
```
ESITO [AVVERSO o DESIDERATO] — punto di partenza della risalita
└─ [descrizione esito]
        ↑ si risale la catena causale ↑
CHECKPOINT N → ... → CHECKPOINT 1
        ↓ ESITO DEL CONTROLLO ↓
┌───────────────┐     ┌────────────────────────┐
│  Tutti SÌ     │     │  Anche un solo NO       │
└───────┬───────┘     └───────────┬────────────┘
        ▼                         ▼
[ESITO SICURO]           [AZIONE CORRETTIVA]
```

Per **Sensitivity Analysis + Backward Induction**:
```
ESITO DESIDERATO
        ↑ backward induction ↑
NODO N → ... → NODO 1 — VARIABILE CRITICA ◄── sensitivity
        ↓ sensitivity: la variabile cambia l'esito ↓
┌──────────────────┐     ┌──────────────────────────┐
│  Timing corretto │     │  Timing sbagliato         │
└────────┬─────────┘     └─────────────┬────────────┘
         ▼                             ▼
   SCENARIO B                    SCENARIO A
```

Per **Falsification Check (Popper)**:
```
OUTPUT AI — [contenuto]
        ↓ FALSIFICATION TEST ↓
   Non: "sembra giusto?" → bias di conferma
   Ma:  "esiste UNA SOLA prova contraria?"
DOMANDA DIAGNOSTICA → [domanda binaria specifica]
        ↓ ricerca [N minuti] ↓
┌──────────────────────┐     ┌────────────────────────────┐
│  Nessuna prova       │     │  Trovata                   │
│  contraria trovata   │     │  [riferimento specifico]   │
└──────────┬───────────┘     └───────────┬────────────────┘
           ▼                             ▼
  IPOTESI NON FALSIFICATA       IPOTESI FALSIFICATA
  Output utilizzabile           → correggere prima dell'uso
```

Regole per i diagrammi:
- Sempre in blocco di codice ` ``` ` (compatibilità Substack)
- Intestazione: `DIAGRAMMA — [Metodo]: [Nome caso simulato]`
- Dati numerici concreti del caso (valori, percentuali, tempi) — niente generico
- Rami di esito quantificati dove possibile (costi, tempi, probabilità)

---

## 4. Report di revisione accademica

Da inserire dopo la disclosure e prima della checklist. Struttura fissa in 10 sezioni:

1. Mappa logica (tesi principale + sotto-tesi + evidenze)
2. Valutazione solidità prove (tabella: affermazione / tipo fonte / solidità)
3. Punti di forza
4. Vulnerabilità logiche
5. Ipotesi alternative plausibili — ACH (tabella)
6. Stress test (premesse implicite + sensitivity analysis)
7. Valutazione falsificabilità (tabella)
8. Red-team critique (critica massima, 1 paragrafo)
9. Punteggi /100 (5 dimensioni + media ponderata)
10. Classificazione finale (A/B/C con motivazione)

---

## 5. Checklist pre-pubblicazione

4 sezioni obbligatorie: Verifica fattuale / Verifica normativa / Verifica voce / Verifica struttura e link + Valutazione soggettiva.

Ogni dato quantitativo citato nel corpo deve avere una voce di verifica corrispondente.

---

## 6. Vincoli di voce (da `voce_gregorio.md`)

- Apertura nel merito al primo periodo — zero riscaldamento
- Nessun AI marker: "fondamentale", "panorama attuale", "sfide molteplici", "approccio integrato", "in conclusione"
- Meccanismo causale esplicitato, non solo correlazione
- Nessun riferimento diretto a categorie generazionali (es. "millennial") — sostituire con fascia d'età specifica (es. "fascia 28–43 anni")
- Chiusura con domanda aperta o implicazione d'azione — mai morale conclusiva
- Liste gerarchiche, non piatte

---

## 7. File di riferimento del progetto

| File | Contenuto |
|------|-----------|
| `voce_gregorio.md` | Profilo vocale e marcatori AI da eliminare |
| `strategia_contenuti.md` | Posizionamento, target, piano editoriale |
| `substack_articolo_NN_finale.md` | Articoli prodotti (01–08) |

Leggere `voce_gregorio.md` e `strategia_contenuti.md` prima di ogni nuovo articolo.

---

## 8. Numerazione e naming

- Articoli: `substack_articolo_NN_finale.md` (NN = numero progressivo a due cifre)
- Commit: formato descrittivo in italiano con riferimento all'articolo e alle modifiche principali
- Branch attivo: `claude/positioning-agent-Hdi7e`
