import json
import os

DATA_FILE = os.path.join("data", "tasks.json")

def save_tasks_to_json(tasks: list):
    """Extracted aur prioritized tasks ko data/tasks.json file mein save karta hai."""
    os.makedirs("data", exist_ok=True)
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Tasks successfully saved to {DATA_FILE}")

def load_tasks_from_json() -> list:
    """data/tasks.json se saved tasks retrieve karne ke liye helper function."""
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)