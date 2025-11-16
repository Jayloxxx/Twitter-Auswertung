import sqlite3
import sys
import pandas as pd

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect(r'C:\Users\Jason\Desktop\Masterarbeit\Twitter-Auswertung\instance\twitter_ter.db')
cursor = conn.cursor()

print("=" * 80)
print("POSTS MIT EMPÖRUNG = 0 (von den 69 wichtigen)")
print("=" * 80)

cursor.execute('''
    SELECT id, twitter_url
    FROM twitter_posts
    WHERE is_reviewed = 1 AND is_excluded = 0 AND trigger_empoerung = 0
''')
results = cursor.fetchall()

for post_id, url in results:
    print(f'Post ID {post_id}: {url}')

print("\n" + "=" * 80)
print("PRÜFE OB DIESE IN DER EXCEL-DATEI SIND")
print("=" * 80)

excel_path = r'C:\Users\Jason\Desktop\Masterarbeit\Finalendergebnis\trigger_frame_results_20251112_194157.xlsx'
df = pd.read_excel(excel_path)

for post_id, db_url in results:
    found = False
    for idx, row in df.iterrows():
        excel_url = row['Twitter URL']
        if db_url in excel_url or excel_url in db_url:
            found = True
            print(f"\nPost ID {post_id} GEFUNDEN in Excel:")
            print(f"  DB URL: {db_url}")
            print(f"  Excel URL: {excel_url}")
            print(f"  Empörung Score in Excel: {row['Empörung Score']}")
            print(f"  Begründung: {row['Empörung - Detaillierte Begründung'][:100] if pd.notna(row['Empörung - Detaillierte Begründung']) else 'N/A'}...")
            break

    if not found:
        print(f"\nPost ID {post_id} NICHT in Excel gefunden: {db_url}")

conn.close()
