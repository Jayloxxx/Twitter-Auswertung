"""
Migrate backup database to current schema by adding all missing columns
"""
import sqlite3

def get_current_columns(cursor):
    """Get list of current columns in twitter_posts"""
    cursor.execute("PRAGMA table_info(twitter_posts)")
    return [col[1] for col in cursor.fetchall()]

def migrate_to_current_schema():
    db_path = 'instance/twitter_ter.db'

    print("=" * 60)
    print("MIGRATING DATABASE TO CURRENT SCHEMA")
    print("=" * 60)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get current columns
    current_columns = get_current_columns(cursor)
    print(f"\nCurrent columns: {len(current_columns)}")

    # Define all columns that should exist (from current model)
    required_columns = {
        'trigger_empoerung': ('INTEGER', 'DEFAULT 0'),
        'is_excluded': ('BOOLEAN', 'DEFAULT 0'),
        'is_favorite': ('BOOLEAN', 'DEFAULT 0'),
        'access_date': ('VARCHAR(100)', 'NULL'),
    }

    # Add missing columns
    columns_added = []
    for col_name, (col_type, col_default) in required_columns.items():
        if col_name not in current_columns:
            print(f"\n[+] Adding column: {col_name} {col_type} {col_default}")
            try:
                cursor.execute(f"""
                    ALTER TABLE twitter_posts
                    ADD COLUMN {col_name} {col_type} {col_default}
                """)
                conn.commit()
                columns_added.append(col_name)
                print(f"    [OK] Added {col_name}")
            except sqlite3.Error as e:
                print(f"    [ERROR] Failed to add {col_name}: {e}")
        else:
            print(f"[OK] Column exists: {col_name}")

    # Verify final schema
    print("\n" + "-" * 60)
    final_columns = get_current_columns(cursor)
    print(f"Final column count: {len(final_columns)}")

    # Check data integrity
    cursor.execute('SELECT COUNT(*) FROM analysis_sessions')
    sessions = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM twitter_posts')
    posts = cursor.fetchone()[0]

    print(f"\nData integrity check:")
    print(f"  Sessions: {sessions}")
    print(f"  Posts: {posts}")

    cursor.execute('SELECT id, name FROM analysis_sessions')
    for session in cursor.fetchall():
        cursor.execute('SELECT COUNT(*) FROM twitter_posts WHERE session_id = ?', (session[0],))
        post_count = cursor.fetchone()[0]
        print(f"  - Session {session[0]}: '{session[1]}' ({post_count} posts)")

    conn.close()

    print("\n" + "=" * 60)
    if columns_added:
        print(f"[SUCCESS] Added {len(columns_added)} missing columns:")
        for col in columns_added:
            print(f"  - {col}")
    else:
        print("[SUCCESS] All columns already exist")
    print("=" * 60)
    print("\nDatabase is ready! You can now start the application.")

if __name__ == '__main__':
    migrate_to_current_schema()
