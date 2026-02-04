# Status Hub
```
status-hub/
├── app.py                # entrypoint
├── poller.py             # scheduler + diff
├── providers/
│   ├── utils.py
│   ├── base.py
│   ├── openai.py
│   └── claude.py
├── subscribers/
│   └── discord.py
├── state.json            # gemt status
└── requirements.txt
```
Projekt: Discord webhook notifier

Kort beskrivelse
----------------
Dette lille Python-script sender statusbeskeder til en Discord-webhook. Webhook-URL'en skal ikke gemmes i koden — brug en `.env`-fil eller miljøvariabler.

Forudsætninger
--------------
- Python 3.8+ installeret
- Git (valgfrit)
- Anbefalet: oprettet virtual environment (.venv)

Installation og opsætning
-------------------------
1. Opret og aktiver virtualenv:

   - På macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

   - På Windows:
     ```powershell
     # Kommandoprompt
     python -m venv .venv
     .venv\Scripts\activate.bat

     # PowerShell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```

   - Alternativt med generisk Python-kommando (virker på alle platforme):
     ```bash
     python -m venv .venv
     
     # Aktivering
     # macOS/Linux: 
     source .venv/bin/activate
     
     # Windows:
     .venv\Scripts\activate
     ```

Installer dependencies:
pip install -r requirements.txt



Opret en .env-fil (eller sæt miljøvariabler) og tilføj din Discord webhook URL:
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
