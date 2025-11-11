"""
Database Migration Script
Adds is_archived column to the twitter_posts table
"""
import sqlite3
import os

DB_PATH = 'instance/twitter_ter.db'

def migrate_database():
    """Add is_archived column to twitter_posts table"""

    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Datenbank '{DB_PATH}' existiert nicht!")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 80)
    print("DATABASE MIGRATION: Adding Archive Column")
    print("=" * 80)

    try:
        # Check if column already exists
        cursor.execute(f"PRAGMA table_info(twitter_posts)")
        columns = [col[1] for col in cursor.fetchall()]

        if 'is_archived' in columns:
            print(f"[OK] Column 'is_archived' already exists - skipping")
        else:
            # Add the column
            sql = "ALTER TABLE twitter_posts ADD COLUMN is_archived INTEGER DEFAULT 0"
            cursor.execute(sql)
            print(f"[OK] Added column: is_archived (INTEGER DEFAULT 0)")

        # Commit changes
        conn.commit()
        conn.close()

        print("\n" + "=" * 80)
        print("[OK] Migration completed successfully!")
        print("=" * 80)
        return True

    except sqlite3.Error as e:
        print(f"[ERROR] Error adding column: {e}")
        conn.rollback()
        conn.close()
        return False

if __name__ == '__main__':
    migrate_database()
