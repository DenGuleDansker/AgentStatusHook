import json
from pathlib import Path

STATE_FILE = Path("/app/state/state.json")

def load_state():
    # Sikr at mappen eksisterer
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Hvis filen ikke eksisterer, opret en tom
    if not STATE_FILE.exists():
        STATE_FILE.write_text(json.dumps([]))
    
    # Tjek om det er en fil (ikke en mappe)
    if not STATE_FILE.is_file():
        # Hvis det er en mappe, fjern den og opret en fil
        if STATE_FILE.is_dir():
            import shutil
            shutil.rmtree(STATE_FILE)
        
        STATE_FILE.write_text(json.dumps([]))
    
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception as e:
        print(f"Fejl ved indlæsning af state: {e}")
        return []

def save_state(state):
    # Sikr at mappen eksisterer
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

def diff(old, new):
    # Opret et map over gamle tilstande
    old_map = {(e["provider"], e["service"]): e["status"] for e in old}
    changes = []

    # Find ændringer
    for e in new:
        key = (e["provider"], e["service"])
        prev = old_map.get(key)

        # Tilføj til changes hvis status er ændret
        if prev != e["status"]:
            # Tilføj den forrige status til eventet
            e["previous"] = prev
            changes.append(e)

    return changes