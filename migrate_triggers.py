"""
Database Migration Script
Adds trigger and frame columns to the twitter_posts table
"""
import sqlite3
import os

DB_PATH = 'instance/twitter_ter.db'

def migrate_database():
    """Add trigger and frame columns to twitter_posts table"""

    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Datenbank '{DB_PATH}' existiert nicht!")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Trigger columns (Intensität 0-5)
    trigger_columns = [
        ('trigger_angst', 'INTEGER DEFAULT 0'),
        ('trigger_wut', 'INTEGER DEFAULT 0'),
        ('trigger_ekel', 'INTEGER DEFAULT 0'),
        ('trigger_identitaet', 'INTEGER DEFAULT 0'),
        ('trigger_hoffnung', 'INTEGER DEFAULT 0'),
    ]

    # Frame columns (Binär 0-1)
    frame_columns = [
        ('frame_opfer_taeter', 'INTEGER DEFAULT 0'),
        ('frame_bedrohung', 'INTEGER DEFAULT 0'),
        ('frame_verschwoerung', 'INTEGER DEFAULT 0'),
        ('frame_moral', 'INTEGER DEFAULT 0'),
        ('frame_historisch', 'INTEGER DEFAULT 0'),
    ]

    all_columns = trigger_columns + frame_columns

    print("=" * 80)
    print("DATABASE MIGRATION: Adding Trigger & Frame Columns")
    print("=" * 80)

    for column_name, column_type in all_columns:
        try:
            # Check if column already exists
            cursor.execute(f"PRAGMA table_info(twitter_posts)")
            columns = [col[1] for col in cursor.fetchall()]

            if column_name in columns:
                print(f"[OK] Column '{column_name}' already exists - skipping")
                continue

            # Add the column
            sql = f"ALTER TABLE twitter_posts ADD COLUMN {column_name} {column_type}"
            cursor.execute(sql)
            print(f"[OK] Added column: {column_name} ({column_type})")

        except sqlite3.Error as e:
            print(f"[ERROR] Error adding column '{column_name}': {e}")
            conn.rollback()
            return False

    # Commit changes
    conn.commit()
    conn.close()

    print("\n" + "=" * 80)
    print("[OK] Migration completed successfully!")
    print("=" * 80)
    return True

if __name__ == '__main__':
    migrate_database()
