import time
from providers.openai import OpenAIProvider
from providers.claude import ClaudeProvider
from poller import load_state, save_state, diff
from subscribers.discord import send

PROVIDERS = [
    OpenAIProvider(),
    ClaudeProvider()
]

INTERVAL = 120  # 2 minutter

def run():
    while True:
        current = []
        for p in PROVIDERS:
            try:
                raw = p.fetch()
                current.extend(p.normalize(raw))
            except Exception as e:
                print(f"[{p.name}] error:", e)

        last = load_state()
        changes = diff(last, current)

        for event in changes:
            send(event)

        save_state(current)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    run()
