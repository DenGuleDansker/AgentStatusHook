status-hub/
├── app.py                # entrypoint
├── poller.py             # scheduler + diff
├── providers/
│   ├── base.py
│   ├── openai.py
│   └── claude.py
├── subscribers/
│   └── discord.py
├── state.json            # gemt status
└── requirements.txt

Projekt: Discord webhook notifier
Kort beskrivelse
Dette lille Python-script sender statusbeskeder til en Discord-webhook. Webhook-URL'en skal ikke gemmes i koden — brug en .env-fil eller miljøvariabler.

Forudsætninger

Python 3.8+ installeret
Git (valgfrit)
Anbefalet: oprettet virtual environment (.venv)
Installation og opsætning

Opret og aktiver virtualenv:
python3 -m venv .venv
source .venv/bin/activate

Installer dependencies:
pip install -r requirements.txt