"""
Test script to verify the small control group warning feature
"""
import sys
import sqlite3
import numpy as np

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

db_path = r'C:\Users\Jason\Desktop\Masterarbeit\Twitter-Auswertung\instance\twitter_ter.db'

print("=" * 80)
print("TEST: WARNUNG BEI KLEINER KONTROLLGRUPPE")
print("=" * 80)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get reviewed posts (not excluded)
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

# Convert to numpy arrays
triggers = {
    'Angst': np.array([p[0] for p in posts]),
    'Wut': np.array([p[1] for p in posts]),
    'Empörung': np.array([p[2] for p in posts]),
    'Ekel': np.array([p[3] for p in posts]),
    'Identität': np.array([p[4] for p in posts]),
    'Hoffnung': np.array([p[5] for p in posts])
}

ter_values = np.array([p[6] if p[6] is not None else 0 for p in posts])

print("\n" + "-" * 80)
print("TRIGGER-ANALYSE:")
print("-" * 80)

for name, values in triggers.items():
    has_trigger = values > 0
    count_with = int(np.sum(has_trigger))
    count_without = int(np.sum(~has_trigger))

    warning = " ⚠️ WARNUNG!" if count_without < 10 else ""

    print(f"\n{name}:")
    print(f"  Posts MIT {name}: {count_with}")
    print(f"  Posts OHNE {name}: {count_without}{warning}")

    if count_with >= 2:
        avg_ter_with = np.mean(ter_values[has_trigger])
        avg_ter_without = np.mean(ter_values[~has_trigger])
        difference = avg_ter_with - avg_ter_without

        print(f"  Durchschn. TER MIT: {avg_ter_with:.2f}%")
        print(f"  Durchschn. TER OHNE: {avg_ter_without:.2f}%")
        print(f"  Differenz: {difference:.2f}%")

        if count_without < 10:
            print(f"  ⚠️  Kontrollgruppe zu klein (n={count_without})")
            print(f"      → Ergebnis statistisch nicht aussagekräftig!")

print("\n" + "=" * 80)
print("ERWARTETE WARNUNGEN IN DER ANWENDUNG:")
print("=" * 80)

warnings = []
for name, values in triggers.items():
    has_trigger = values > 0
    count_without = int(np.sum(~has_trigger))
    if count_without < 10 and np.sum(has_trigger) >= 2:
        warnings.append(f"{name} (n={count_without})")

if warnings:
    print(f"\n⚠️  Die Anwendung sollte folgende Warnung anzeigen:")
    print(f"    Folgende Trigger haben eine sehr kleine Kontrollgruppe: {', '.join(warnings)}")
else:
    print("\n✓ Keine Warnungen erwartet (alle Kontrollgruppen ≥ 10)")

conn.close()
print("\n" + "=" * 80)
