import json
import os

HIGHSCORE_FILE = "highscores.json"
MAX_ENTRIES = 5

def load_highscores():
    if not os.path.exists(HIGHSCORE_FILE):
        return []
    with open(HIGHSCORE_FILE, "r") as f:
        return json.load(f)

def save_highscores(highscores):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(highscores, f, indent=4)

def add_score(name, score):
    name = name.upper()[:3]
    highscores = load_highscores()
    highscores.append({"name": name, "score": score})
    highscores = sorted(highscores, key=lambda x: x["score"], reverse=True)[:MAX_ENTRIES]
    save_highscores(highscores)

def get_highscores():
    return load_highscores()