"""
Generatore Articoli Substack — Gregorio Manèra
===============================================
Lancia il sistema multi-agente per ricercare e scrivere
gli articoli 06, 07, 08 del piano editoriale.
"""

import anyio
import os
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AgentDefinition,
    ResultMessage,
)


# ─── Profilo vocale Gregorio (estratto da voce_gregorio.md) ──────────────────

VOICE_RULES = """
REGOLE VOCALI OBBLIGATORIE (profilo Gregorio Manèra):

ELIMINARE SEMPRE:
- "Nel panorama attuale...", "È fondamentale sottolineare che...", "Come abbiamo visto..."
- "Potrebbe essere interessante considerare...", "Solo il tempo ci dirà..."
- "Le sfide sono molteplici", "Un approccio integrato", "In conclusione, possiamo affermare..."
- Liste piatte senza gerarchia logica
- Transizioni ovvie tipo "Detto questo, passiamo a..."

COSTRUIRE COSÌ:
- Apertura: entra nel merito al primo periodo, zero riscaldamento
- Argomentazione: esplicita il meccanismo causale, non solo la correlazione
- Lessico: termini tecnici precisi > perifrasi generiche
- Paragrafi: 3-5 righe max, ogni paragrafo ha una funzione
- Chiusura: apre una domanda o pone un'implicazione diretta, mai con fiocco retorico

STRUTTURA ARTICOLO SUBSTACK:
- Titolo + byline autore
- Separatore ---
- Corpo articolo con sezioni H3 (###)
- Separatore ---
- ### Note (footnotes numerati ¹²³...)
- Separatore ---
- ### Per approfondire (categorie con bullet)
- Separatore ---
- Nota disclosure (2 paragrafi in corsivo - vedi sotto)
- Nome autore e qualifica in grassetto

NOTA DISCLOSURE STANDARD (usare esattamente questo):
*Questo articolo è redatto a scopo informativo e non costituisce consulenza professionale. Prima di adottare qualsiasi decisione, è consigliabile confrontarsi con il proprio professionista di fiducia. Il Dott. Gregorio Manèra è disponibile per richieste di chiarimento e approfondimento.*

*Contenuto redatto con il supporto di strumenti di intelligenza artificiale per le fasi di ricerca e sintesi documentale. Analisi, valutazioni e posizioni espresse sono dell'autore, che ne assume la piena responsabilità professionale ai sensi della L. 132/2025.*

**Gregorio Manèra**
Dottore Commercialista · Revisore Legale · Docente di Economia, Diritto e Amministrazione Aziendale
"""


# ─── Agente ricercatore ───────────────────────────────────────────────────────

RESEARCHER = AgentDefinition(
    description=(
        "Ricercatore specializzato in normativa italiana, dati di mercato e "
        "giurisprudenza. Trova dati aggiornati, normative vigenti e fonti "
        "verificabili per supportare articoli professionali."
    ),
    prompt=(
        "Sei un ricercatore senior specializzato in diritto tributario, "
        "normativa civilistica e analisi di mercato italiana.\n\n"
        "Per ogni topic assegnato:\n"
        "1. Cerca dati quantitativi recenti con fonte citabile\n"
        "2. Identifica le normative vigenti con riferimenti precisi (articolo, legge, GU)\n"
        "3. Trova casi pratici o esempi concreti\n"
        "4. Raccogli URL e riferimenti per la sezione 'Per approfondire'\n\n"
        "Output: lista strutturata di fatti, dati e fonti, pronta per il redattore."
    ),
    tools=["WebSearch", "WebFetch"],
)


# ─── Agente redattore ────────────────────────────────────────────────────────

WRITER = AgentDefinition(
    description=(
        "Redattore esperto in contenuti professionali per Substack italiano. "
        "Scrive articoli analitici in voce Gregorio Manèra: densi, causali, "
        "con dati verificati e zero retorica. Pubblica per millennials imprenditori."
    ),
    prompt=(
        "Sei il redattore ufficiale della newsletter di Gregorio Manèra "
        "(Dottore Commercialista, Revisore Legale, Docente).\n\n"
        "Scrivi articoli Substack per imprenditori millennial italiani "
        "con imprese 1-10 dipendenti, condomini, associazioni, privati con "
        "situazioni patrimoniali complesse.\n\n"
        "Approccio: non tutorial, non profetico, non accademico. "
        "Analitico, basato su dati, orientato alla decisione.\n\n"
        "Lunghezza target: 800-1100 parole corpo articolo.\n\n"
        + VOICE_RULES
    ),
    tools=["WebSearch", "WebFetch"],
)


# ─── Sistema prompt orchestratore ────────────────────────────────────────────

ORCHESTRATOR_PROMPT = (
    "Sei il coordinatore editoriale della newsletter Substack di Gregorio Manèra.\n\n"
    "Workflow per ogni articolo:\n"
    "1. Usa 'ricercatore' per raccogliere dati, normative e fonti sul topic\n"
    "2. Passa tutto al 'redattore' con istruzione: scrivere l'articolo completo "
    "in markdown, rispettando TUTTE le regole vocali e la struttura standard\n"
    "3. Restituisci il testo markdown completo come output finale\n\n"
    "Il risultato finale deve essere SOLO il testo markdown dell'articolo, "
    "pronto per copia-incolla su Substack. Nessun commento, nessuna nota a margine."
)


# ─── Lista articoli da generare ───────────────────────────────────────────────

ARTICLES = [
    {
        "numero": "06",
        "topic": (
            "ARTICOLO 06 — Il condominio davanti alla riforma\n\n"
            "Topic: l'amministratore di condominio è oggi sotto pressione normativa "
            "crescente. Il D.Lgs. 145/2023 (riforma del codice civile condominio) e "
            "le normative sul Superbonus hanno trasformato un ruolo formalmente "
            "semplice in una posizione ad alta responsabilità. "
            "I condomini italiani sono circa 1,2 milioni, con oltre 14 milioni di "
            "unità abitative.\n\n"
            "Angolo: il bilancio condominiale che nessuno capisce davvero — struttura, "
            "errori frequenti, responsabilità dell'amministratore, cosa può fare un "
            "revisore/commercialista per portare chiarezza dove oggi regna ambiguità.\n\n"
            "Includi: dati sul settore, normativa vigente con riferimenti precisi, "
            "3 profili di rischio distinti, processo decisionale pratico per i "
            "condòmini, almeno 5 footnote con fonti verificabili, sezione "
            "'Per approfondire' con 3-4 categorie di risorse."
        ),
        "output_file": "substack_articolo_06_finale.md",
    },
    {
        "numero": "07",
        "topic": (
            "ARTICOLO 07 — Quanto vale la tua impresa? La domanda che le micro-PMI "
            "non si fanno finché è troppo tardi\n\n"
            "Topic: la stragrande maggioranza delle micro-PMI italiane non ha mai "
            "fatto una valutazione d'azienda. Il momento in cui la necessità emerge "
            "è spesso il peggiore per farlo: passaggio generazionale, cessione "
            "d'urgenza, ingresso di un socio, separazione coniugale con quote societarie, "
            "accesso al credito.\n\n"
            "Angolo: non un tutorial sulla valutazione (DCF, multipli ecc.) ma "
            "l'analisi di QUANDO serve, PERCHÉ farlo prima, e cosa succede quando "
            "non è stato fatto. Metodi valutativi semplificati per PMI (OIV 2023, "
            "Principi italiani di valutazione). Costo-opportunità della non-valutazione.\n\n"
            "Includi: dati sul tessuto PMI italiano, normativa rilevante (OIV, "
            "D.Lgs. 139/2024 su successioni), 3 scenari tipici dove la valutazione "
            "manca, processo in 4 fasi, almeno 5 footnote con fonti, sezione "
            "'Per approfondire'."
        ),
        "output_file": "substack_articolo_07_finale.md",
    },
    {
        "numero": "08",
        "topic": (
            "ARTICOLO 08 — L'errore che l'AI non può correggere (e il professionista sì)\n\n"
            "Topic: identificare con precisione il limite strutturale dell'AI nei "
            "contesti professionali ad alta dipendenza contestuale — non per essere "
            "anti-AI, ma per posizionare l'expertise umana come irreplaceable proprio "
            "là dove l'AI è più convincente ma più rischiosa.\n\n"
            "Angolo: esistono categorie di errori che l'AI produce sistematicamente "
            "in ambito fiscale/legale/strategico che un professionista esperto rileva "
            "in 30 secondi. Non sono errori di calcolo — sono errori di contesto "
            "(normativa abrogata, sentenza superata, clausola inapplicabile al caso). "
            "Il pericolo non è l'AI che sbaglia, è l'AI che sbaglia in modo fluente.\n\n"
            "Includi: caso Mata v. Avianca (SDNY 2023) come riferimento internazionale, "
            "esempi specifici dal diritto tributario italiano, Legge 132/2025, "
            "EU AI Act (full application agosto 2026), il concetto di 'hallucination' "
            "con fonte accademica, 3 categorie di errori AI per tipo di impatto, "
            "almeno 5 footnote, sezione 'Per approfondire'. "
            "Concludere con implicazione per chi usa AI senza supervisione qualificata."
        ),
        "output_file": "substack_articolo_08_finale.md",
    },
]


# ─── Runner ───────────────────────────────────────────────────────────────────

async def genera_articolo(articolo: dict) -> str:
    """Genera un singolo articolo usando il sistema multi-agente."""
    print(f"\n{'=' * 60}")
    print(f"  Generazione articolo #{articolo['numero']}")
    print(f"  Output: {articolo['output_file']}")
    print(f"{'=' * 60}\n")

    result = ""
    async for message in query(
        prompt=articolo["topic"],
        options=ClaudeAgentOptions(
            system_prompt=ORCHESTRATOR_PROMPT,
            allowed_tools=["Agent", "WebSearch", "WebFetch"],
            permission_mode="acceptEdits",
            agents={
                "ricercatore": RESEARCHER,
                "redattore": WRITER,
            },
            max_turns=40,
        ),
    ):
        if isinstance(message, ResultMessage):
            result = message.result

    return result


async def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))

    for articolo in ARTICLES:
        testo = await genera_articolo(articolo)

        if not testo:
            print(f"[ATTENZIONE] Articolo #{articolo['numero']} — output vuoto.")
            continue

        filepath = os.path.join(output_dir, articolo["output_file"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(testo)

        print(f"\n[OK] Salvato: {filepath}")
        print(f"     Lunghezza: {len(testo)} caratteri / "
              f"~{len(testo.split())} parole\n")

    print("\n" + "=" * 60)
    print("  Generazione completata.")
    print("=" * 60)


if __name__ == "__main__":
    anyio.run(main)
