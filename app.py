import os
import time
import logging
from providers.openai import OpenAIProvider
from providers.claude import ClaudeProvider
from providers.google import GoogleProvider
from poller import load_state, save_state, diff
from subscribers.discord import send

# Konfigurer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Udskriv .env variabler (pas på ikke at lægge følsomme data i produktionen)
logging.info("Environment Variables:")
for key, value in os.environ.items():
    # Maskér følsomme værdier
    if 'KEY' in key.upper() or 'SECRET' in key.upper() or 'TOKEN' in key.upper():
        logging.info(f"{key}: {'*' * 10}")
    else:
        logging.info(f"{key}: {value}")

PROVIDERS = [
    OpenAIProvider(),
    ClaudeProvider(),
    GoogleProvider(),
]

INTERVAL = 120  # 2 minutter

def run():
    logging.info("🟢 Status Agent startet!")
    logging.info(f"Opdateringsinterval: {INTERVAL} sekunder")
    
    iteration = 0
    while True:
        iteration += 1
        logging.info(f"Iteration {iteration}: Checker providers")
        
        current = []
        for p in PROVIDERS:
            try:
                logging.info(f"Checker {p.name}")
                raw = p.fetch()
                current.extend(p.normalize(raw))
                logging.info(f"{p.name} checked successfully")
            except Exception as e:
                logging.error(f"[{p.name}] error: {e}")

        last = load_state()
        changes = diff(last, current)

        if changes:
            logging.info(f"Fandt {len(changes)} ændringer")
            for event in changes:
                try:
                    send(event)
                    logging.info(f"Sendt besked for {event.get('provider')} {event.get('service')}")
                except Exception as e:
                    logging.error(f"Fejl ved sending af besked: {e}")
        else:
            logging.info("Ingen ændringer detekteret")

        save_state(current)
        
        logging.info(f"Venter {INTERVAL} sekunder før næste tjek")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logging.critical(f"Kritisk fejl: {e}")
        raise