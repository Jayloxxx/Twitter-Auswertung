"""
Test script to analyze trigger frequency for the 69 important posts
"""
import sys
import sqlite3

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

db_path = r'C:\Users\Jason\Desktop\Masterarbeit\Twitter-Auswertung\instance\twitter_ter.db'

print("=" * 80)
print("TRIGGER-HÄUFIGKEIT (69 wichtige Posts)")
print("=" * 80)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get the 69 important posts
cursor.execute('''
    SELECT
        trigger_angst, trigger_wut, trigger_empoerung,
        trigger_ekel, trigger_identitaet, trigger_hoffnung
    FROM twitter_posts
    WHERE is_reviewed = 1 AND is_excluded = 0
''')

posts = cursor.fetchall()
total = len(posts)

print(f"\nGesamtanzahl Posts: {total}")
print("\n" + "-" * 80)

triggers = {
    'Angst': [p[0] for p in posts],
    'Wut': [p[1] for p in posts],
    'Empörung': [p[2] for p in posts],
    'Ekel': [p[3] for p in posts],
    'Identität': [p[4] for p in posts],
    'Hoffnung': [p[5] for p in posts]
}

print("\n📊 TRIGGER-HÄUFIGKEIT (Anzahl Posts mit Trigger > 0)")
print("-" * 80)

frequency_data = []
for name, values in triggers.items():
    count_with = sum(1 for v in values if v > 0)
    percentage = (count_with / total) * 100
    frequency_data.append({
        'name': name,
        'count': count_with,
        'percentage': percentage
    })

# Sort by count descending
frequency_data.sort(key=lambda x: x['count'], reverse=True)

for item in frequency_data:
    bar_length = int(item['percentage'] / 2)  # Scale for console
    bar = '█' * bar_length
    print(f"{item['name']:12} │ {bar} {item['count']:2}/{total} ({item['percentage']:5.1f}%)")

print("\n" + "-" * 80)
print("\n📈 TRIGGER-INTENSITÄT (Durchschnittlicher Score bei Posts MIT Trigger)")
print("-" * 80)

for name, values in triggers.items():
    values_with_trigger = [v for v in values if v > 0]
    if values_with_trigger:
        avg_intensity = sum(values_with_trigger) / len(values_with_trigger)
        print(f"{name:12} │ Ø Score: {avg_intensity:.2f} (bei {len(values_with_trigger)} Posts)")

print("\n" + "-" * 80)
print("\n📋 DETAILLIERTE VERTEILUNG PRO TRIGGER-INTENSITÄT")
print("-" * 80)

for name, values in triggers.items():
    print(f"\n{name}:")
    for score in range(6):
        count = sum(1 for v in values if v == score)
        if count > 0:
            percentage = (count / total) * 100
            bar_length = int(percentage / 2)
            bar = '░' * bar_length if score == 0 else '█' * bar_length
            print(f"  Score {score}: {bar} {count:2} Posts ({percentage:5.1f}%)")

conn.close()
print("\n" + "=" * 80)
