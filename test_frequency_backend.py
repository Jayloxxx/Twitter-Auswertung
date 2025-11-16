"""
Test to verify that trigger_frequency data is correctly generated in backend
"""
import sys
import sqlite3
import numpy as np

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

db_path = r'C:\Users\Jason\Desktop\Masterarbeit\Twitter-Auswertung\instance\twitter_ter.db'

print("=" * 80)
print("TEST: BACKEND TRIGGER-HÄUFIGKEIT BERECHNUNG")
print("=" * 80)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Simulate what the backend does
cursor.execute('''
    SELECT
        trigger_angst, trigger_wut, trigger_empoerung,
        trigger_ekel, trigger_identitaet, trigger_hoffnung,
        ter_automatic
    FROM twitter_posts
    WHERE is_reviewed = 1 AND is_excluded = 0
''')

posts = cursor.fetchall()
print(f"\nGeladene Posts: {len(posts)}")

# Convert to numpy arrays (like in the backend)
triggers = {
    'Angst': np.array([p[0] for p in posts]),
    'Wut': np.array([p[1] for p in posts]),
    'Empörung': np.array([p[2] for p in posts]),
    'Ekel': np.array([p[3] for p in posts]),
    'Identität': np.array([p[4] for p in posts]),
    'Hoffnung': np.array([p[5] for p in posts])
}

ter_values = np.array([p[6] if p[6] is not None else 0 for p in posts])

# Simulate Chart 0: Trigger-Häufigkeit
trigger_frequency = []
total_posts = len(ter_values)

print(f"\nBerechne Häufigkeiten für {total_posts} Posts...\n")

for name, values in triggers.items():
    has_trigger = values > 0
    count_with = int(np.sum(has_trigger))
    percentage = (count_with / total_posts) * 100 if total_posts > 0 else 0

    trigger_frequency.append({
        'trigger': name,
        'count': count_with,
        'total': total_posts,
        'percentage': round(float(percentage), 1)
    })

# Sort by percentage descending
trigger_frequency.sort(key=lambda x: x['percentage'], reverse=True)

print("=" * 80)
print("ERWARTETE DATEN FÜR FRONTEND (trigger_frequency):")
print("=" * 80)

import json
print(json.dumps(trigger_frequency, indent=2, ensure_ascii=False))

print("\n" + "=" * 80)
print("VISUALISIERUNG:")
print("=" * 80)

for item in trigger_frequency:
    bar_length = int(item['percentage'] / 2)
    bar = '█' * bar_length
    print(f"{item['trigger']:12} │ {bar} {item['count']}/{item['total']} ({item['percentage']}%)")

conn.close()
print("\n" + "=" * 80)
print("✓ Test abgeschlossen - Daten sollten im Frontend korrekt angezeigt werden")
print("=" * 80)
