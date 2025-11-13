import sqlite3

for db_name in ['twitter_ter.db', 'twitter_analysis.db']:
    print(f"\nChecking {db_name}:")
    print("-" * 60)
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables: {[t[0] for t in tables]}")

        # Check if twitter_posts exists
        if any('twitter_posts' in str(t) for t in tables):
            cursor.execute("SELECT COUNT(*) FROM twitter_posts")
            count = cursor.fetchone()[0]
            print(f"Number of posts: {count}")

            if count > 0:
                cursor.execute("PRAGMA table_info(twitter_posts)")
                columns = [c[1] for c in cursor.fetchall()]
                print(f"Has is_excluded column: {'is_excluded' in columns}")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")
