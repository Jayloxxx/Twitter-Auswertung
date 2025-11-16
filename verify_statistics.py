import sys
import sqlite3

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect(r'C:\Users\Jason\Desktop\Masterarbeit\Twitter-Auswertung\instance\twitter_ter.db')
cursor = conn.cursor()

print("=" * 80)
print("EMPÖRUNG-STATISTIKEN NACH UPDATE")
print("=" * 80)

print("\n80 POSTS (is_reviewed = 1):")
print("-" * 80)
cursor.execute('''
    SELECT trigger_empoerung, COUNT(*)
    FROM twitter_posts
    WHERE is_reviewed = 1
    GROUP BY trigger_empoerung
    ORDER BY trigger_empoerung
''')
for score, count in cursor.fetchall():
    print(f'  Score {score}: {count} Posts')

cursor.execute('''
    SELECT COUNT(*), SUM(CASE WHEN trigger_empoerung > 0 THEN 1 ELSE 0 END)
    FROM twitter_posts
    WHERE is_reviewed = 1
''')
total, with_emp = cursor.fetchone()
print(f'\n  Total: {total}, Mit Empörung > 0: {with_emp}')

print("\n69 POSTS (is_reviewed = 1 AND is_excluded = 0):")
print("-" * 80)
cursor.execute('''
    SELECT trigger_empoerung, COUNT(*)
    FROM twitter_posts
    WHERE is_reviewed = 1 AND is_excluded = 0
    GROUP BY trigger_empoerung
    ORDER BY trigger_empoerung
''')
for score, count in cursor.fetchall():
    print(f'  Score {score}: {count} Posts')

cursor.execute('''
    SELECT COUNT(*), SUM(CASE WHEN trigger_empoerung > 0 THEN 1 ELSE 0 END)
    FROM twitter_posts
    WHERE is_reviewed = 1 AND is_excluded = 0
''')
total, with_emp = cursor.fetchone()
print(f'\n  Total: {total}, Mit Empörung > 0: {with_emp}')

conn.close()
print("\n" + "=" * 80)
