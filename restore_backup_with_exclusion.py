"""
Restore backup database and add is_excluded column
"""
import sqlite3
import shutil
from datetime import datetime

def restore_and_migrate():
    backup_file = 'instance/twitter_ter.db.backup.20251111_131851'
    current_db = 'instance/twitter_ter.db'

    print("=" * 60)
    print("RESTORING DATABASE FROM BACKUP")
    print("=" * 60)

    # 1. Create safety backup of current state
    safety_backup = f'instance/twitter_ter.db.before_restore_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    try:
        shutil.copy2(current_db, safety_backup)
        print(f"\n[OK] Created safety backup: {safety_backup}")
    except Exception as e:
        print(f"[INFO] No current db to backup: {e}")

    # 2. Restore from backup
    print(f"\n[1/3] Restoring from backup: {backup_file}")
    shutil.copy2(backup_file, current_db)
    print("[OK] Database restored from backup")

    # 3. Check restored data
    conn = sqlite3.connect(current_db)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM analysis_sessions')
    sessions = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM twitter_posts')
    posts = cursor.fetchone()[0]

    print(f"\n[2/3] Restored data:")
    print(f"  Sessions: {sessions}")
    print(f"  Posts: {posts}")

    cursor.execute('SELECT id, name FROM analysis_sessions')
    for session in cursor.fetchall():
        cursor.execute('SELECT COUNT(*) FROM twitter_posts WHERE session_id = ?', (session[0],))
        post_count = cursor.fetchone()[0]
        print(f"  - Session {session[0]}: {session[1]} ({post_count} posts)")

    # 4. Check if is_excluded column exists
    cursor.execute("PRAGMA table_info(twitter_posts)")
    columns = [col[1] for col in cursor.fetchall()]

    if 'is_excluded' in columns:
        print("\n[OK] is_excluded column already exists")
    else:
        print("\n[3/3] Adding is_excluded column...")
        cursor.execute("""
            ALTER TABLE twitter_posts
            ADD COLUMN is_excluded BOOLEAN DEFAULT 0
        """)
        conn.commit()
        print("[OK] is_excluded column added successfully")

        # Verify
        cursor.execute("PRAGMA table_info(twitter_posts)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'is_excluded' in columns:
            print("[OK] Verified: is_excluded column exists")

    conn.close()

    print("\n" + "=" * 60)
    print("[SUCCESS] Database restored and migrated!")
    print("=" * 60)
    print(f"\nYour data is back:")
    print(f"  - {sessions} sessions")
    print(f"  - {posts} posts")
    print(f"  - is_excluded column ready to use")
    print("\nYou can now start the application!")

if __name__ == '__main__':
    restore_and_migrate()
