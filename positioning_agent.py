"""
Agente di Posizionamento - Supporto Decisionale per Professionisti
=================================================================
Un sistema multi-agente che analizza la domanda di mercato e supporta
le decisioni strategiche di posizionamento, gestito da professionisti
esperti con assistenza AI.
"""

import anyio
import os
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AgentDefinition,
    ResultMessage,
    SystemMessage,
)


# ─── Definizione degli agenti specializzati ───────────────────────────────────

ANALYST_AGENT = AgentDefinition(
    description=(
        "Esperto analista di mercato specializzato nell'analisi della domanda, "
        "trend di settore e dinamiche competitive. Fornisce insight quantitativi "
        "e qualitativi per supportare decisioni di posizionamento."
    ),
    prompt=(
        "Sei un analista di mercato senior con oltre 15 anni di esperienza. "
        "Il tuo compito è:\n"
        "1. Analizzare la domanda di mercato nel segmento richiesto\n"
        "2. Identificare trend emergenti e pattern di consumo\n"
        "3. Valutare i gap di mercato e le opportunità di posizionamento\n"
        "4. Fornire dati e evidenze a supporto delle conclusioni\n"
        "Usa ricerche web per dati aggiornati. Struttura le analisi in modo chiaro "
        "con sezioni: Sintesi, Dati Chiave, Trend, Opportunità, Rischi."
    ),
    tools=["WebSearch", "WebFetch", "Bash"],
)

STRATEGY_AGENT = AgentDefinition(
    description=(
        "Consulente strategico specializzato in posizionamento di prodotto/servizio, "
        "analisi competitiva e definizione del valore unico. Trasforma le analisi "
        "in raccomandazioni strategiche concrete e actionable."
    ),
    prompt=(
        "Sei un consulente strategico di alto livello con esperienza in McKinsey-style "
        "framework. Il tuo compito è:\n"
        "1. Definire opzioni di posizionamento strategico basate sull'analisi\n"
        "2. Valutare la fattibilità e il potenziale di ogni opzione\n"
        "3. Costruire una matrice decisionale con criteri ponderati\n"
        "4. Raccomandare la strategia ottimale con piano di implementazione\n"
        "Usa framework come Porter's Five Forces, Blue Ocean, Jobs-to-be-done "
        "dove appropriato. Sii concreto, misurabile, orientato all'azione."
    ),
    tools=["WebSearch", "WebFetch", "Bash"],
)

RISK_AGENT = AgentDefinition(
    description=(
        "Esperto di risk management e analisi degli scenari. Valuta rischi e "
        "opportunità associate alle decisioni di posizionamento, fornendo "
        "una visione bilanciata per decisioni informate."
    ),
    prompt=(
        "Sei un risk manager specializzato in analisi strategica. Il tuo compito è:\n"
        "1. Identificare i principali rischi per ogni opzione di posizionamento\n"
        "2. Valutare probabilità e impatto di ciascun rischio\n"
        "3. Definire scenari (ottimistico, base, pessimistico)\n"
        "4. Proporre misure di mitigazione e contingency plan\n"
        "Struttura l'output come: Risk Register, Analisi Scenari, Piano di Mitigazione."
    ),
    tools=["WebSearch", "WebFetch"],
)


# ─── System prompt dell'orchestratore principale ─────────────────────────────

ORCHESTRATOR_SYSTEM_PROMPT = """
Sei il Coordinatore dell'Agente di Posizionamento, un sistema di supporto decisionale
avanzato per professionisti esperti.

Il tuo ruolo è orchestrare un'analisi completa di posizionamento usando agenti specializzati:
- **analista-mercato**: Per analisi della domanda, trend e dati di mercato
- **stratega**: Per opzioni strategiche e raccomandazioni di posizionamento
- **risk-manager**: Per analisi dei rischi e scenari

WORKFLOW STANDARD:
1. Comprendi la richiesta del professionista e il contesto
2. Delega all'analista-mercato per l'analisi della domanda
3. Passa i risultati allo stratega per le opzioni strategiche
4. Coinvolgi il risk-manager per la valutazione dei rischi
5. Sintetizza tutte le analisi in un REPORT DECISIONALE strutturato

FORMATO DEL REPORT FINALE:
---
# REPORT DI POSIZIONAMENTO STRATEGICO
## Executive Summary (3-5 punti chiave)
## Analisi della Domanda
## Opzioni di Posizionamento
## Valutazione dei Rischi
## RACCOMANDAZIONE (con piano d'azione)
## KPI e Metriche di Successo
---

Mantieni sempre un approccio professionale, basato su dati e orientato alla decisione.
"""


# ─── Funzione principale ──────────────────────────────────────────────────────

async def run_positioning_agent(query_text: str, verbose: bool = False) -> str:
    """
    Esegue l'agente di posizionamento per la query fornita.

    Args:
        query_text: La richiesta di analisi del professionista
        verbose: Se True, mostra i messaggi di sistema durante l'esecuzione

    Returns:
        Il report decisionale generato
    """
    result = ""

    async for message in query(
        prompt=query_text,
        options=ClaudeAgentOptions(
            system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
            allowed_tools=["Agent", "WebSearch", "WebFetch", "Bash"],
            permission_mode="bypassPermissions",
            agents={
                "analista-mercato": ANALYST_AGENT,
                "stratega": STRATEGY_AGENT,
                "risk-manager": RISK_AGENT,
            },
            max_turns=30,
        ),
    ):
        if isinstance(message, ResultMessage):
            result = message.result
        elif isinstance(message, SystemMessage) and verbose:
            if message.subtype == "init":
                session_id = message.data.get("session_id", "N/A")
                print(f"[Sistema] Sessione avviata: {session_id}")

    return result


async def interactive_session():
    """
    Sessione interattiva con il professionista esperto.
    """
    print("\n" + "=" * 60)
    print("  AGENTE DI POSIZIONAMENTO - Supporto Decisionale")
    print("=" * 60)
    print("\nBenvenuto nel sistema di analisi e posizionamento strategico.")
    print("Descrivi il tuo progetto, prodotto o mercato da analizzare.")
    print("Digita 'esci' per terminare.\n")

    while True:
        try:
            user_input = input("Professionista: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSessione terminata.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("esci", "exit", "quit"):
            print("\nArrivederci!")
            break

        print("\n[Agenti AI al lavoro - analisi in corso...]\n")

        result = await run_positioning_agent(user_input, verbose=True)

        print("\n" + "─" * 60)
        print(result)
        print("─" * 60 + "\n")


async def demo():
    """
    Demo con una query di esempio per testare il sistema.
    """
    sample_query = (
        "Analizza le opportunità di posizionamento per un servizio SaaS di "
        "gestione documentale con AI rivolto a studi professionali (avvocati, "
        "commercialisti, consulenti) in Italia. Budget annuo stimato: €500K. "
        "Fornisci raccomandazioni strategiche e piano d'azione."
    )

    print("\n" + "=" * 60)
    print("  AGENTE DI POSIZIONAMENTO - Demo")
    print("=" * 60)
    print(f"\nQuery di esempio:\n{sample_query}\n")
    print("[Avvio analisi multi-agente...]\n")

    result = await run_positioning_agent(sample_query, verbose=True)

    print("\n" + "=" * 60)
    print("REPORT DECISIONALE FINALE")
    print("=" * 60)
    print(result)


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else "interactive"

    if mode == "demo":
        anyio.run(demo)
    else:
        anyio.run(interactive_session)
