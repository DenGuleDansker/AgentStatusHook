import json
from pathlib import Path

STATE_FILE = Path("state.json")

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return []

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def diff(old, new):
    old_map = {(e["provider"], e["service"]): e["status"] for e in old}
    changes = []

    for e in new:
        key = (e["provider"], e["service"])
        prev = old_map.get(key)

        if prev != e["status"]:
            e["previous"] = prev
            changes.append(e)

    return changes
