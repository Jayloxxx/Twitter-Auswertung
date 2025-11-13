import sqlite3

conn = sqlite3.connect('twitter_ter.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(twitter_posts)')
cols = cursor.fetchall()

print("Columns in twitter_posts table:")
print("-" * 60)
for c in cols:
    print(f"{c[1]:30s} {c[2]:15s} default={c[4]}")

print("\nSearching for is_excluded column...")
is_excluded_exists = any('is_excluded' in str(c[1]) for c in cols)
print(f"is_excluded column exists: {is_excluded_exists}")

conn.close()
