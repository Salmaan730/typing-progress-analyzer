# Typing progress analyzer
# Reads keybr practice data and shows my progress

import json

def load_data(filepath):
    """Load keybr JSON export."""
    with open(filepath) as f:
        return json.load(f)

if __name__ == "__main__":
    data = load_data("stats.txt")
    print("Data loaded successfully.")
    print(type(data))
