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
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate


Installer dependencies:
pip install -r requirements.txt



Opret en .env-fil (eller sæt miljøvariabler) og tilføj din Discord webhook URL:
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

Bemærk: Gem aldrig denne URL i versionskontrol.

Kørsel
Start programmet (entrypoint):
python app.py

eller efter behov:
python poller.py

(Afhængigt af hvordan projektet er struktureret kan poller.py køres separat hvis det er et scheduler-script.)
Filer og mapper
app.py — Entrypoint til applikationen.
poller.py — Scheduler, der tjekker status og laver diff mellem tidligere og nuværende status.
providers/ — Implementeringer af status-udbydere:

base.py — Basisklasse / interface for providers.
openai.py — Eksempel på provider (OpenAI).
claude.py — Eksempel på provider (Claude).


subscribers/discord.py — Subscriber som sender beskeder til Discord via webhook.
state.json — Gemt (persisted) status fra sidste kørsel.
requirements.txt — Python-dependencies.
Sikkerhed og tips
Opbevar følsomme nøgler og webhooks i .env eller sikre hemmelighedsstyringsløsninger.
Tilføj .env og eventuelle state.json-filer til .gitignore for at undgå at pushe dem.
Overvej at køre scriptet som en systemtjeneste eller med en process manager (f.eks. systemd eller supervisord) hvis det skal køre kontinuerligt.
LicensTilføj eventuelt en licensfil (f.eks. LICENSE)
