# Typing progress analyzer
# Reads keybr JSON export and shows real progress
# keybr speed field / 5 = approximate real WPM

import json
from collections import defaultdict

def load_data(filepath):
    """Load keybr JSON export."""
    with open(filepath) as f:
        return json.load(f)

def real_wpm(session):
    """Convert keybr speed field to standard WPM."""
    minutes = session['time'] / 1000 / 60
    return (session['length'] / 5) / minutes

def speed_summary(data):
    """Print speed progress summary."""
    speeds = [real_wpm(s) for s in data]
    print(f"Total sessions: {len(speeds)}")
    print(f"First session: {speeds[0]:.1f} WPM")
    print(f"Latest session: {speeds[-1]:.1f} WPM")
    print(f"Average: {sum(speeds)/len(speeds):.1f} WPM")
    print(f"Personal best: {max(speeds):.1f} WPM")

def shaky_keys(data, min_hits=50):
    """Find keys with highest miss rates."""
    key_hits = defaultdict(int)
    key_misses = defaultdict(int)
    for session in data:
        for k in session['histogram']:
            char = chr(k['codePoint'])
            key_hits[char] += k['hitCount']
            key_misses[char] += k['missCount']
    miss_rates = {
        k: key_misses[k] / (key_hits[k] + 1)
        for k in key_hits if key_hits[k] >= min_hits
    }
    worst = sorted(miss_rates.items(), key=lambda x: -x[1])[:5]
    print("\nShakyest keys (min 50 hits):")
    for key, rate in worst:
        print(f"  '{key}': {rate:.3f} miss rate, {key_hits[key]} hits")

if __name__ == "__main__":
    data = load_data("stats.txt")
    speed_summary(data)
    shaky_keys(data)
