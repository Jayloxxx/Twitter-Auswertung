"""
Migration script to add is_excluded column to twitter_posts table
"""
import sqlite3
import os

def migrate_database():
    db_path = 'twitter_ter.db'

    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found!")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(twitter_posts)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'is_excluded' in columns:
            print("Column 'is_excluded' already exists!")
            return True

        # Add the is_excluded column
        print("Adding 'is_excluded' column to twitter_posts table...")
        cursor.execute("""
            ALTER TABLE twitter_posts
            ADD COLUMN is_excluded BOOLEAN DEFAULT 0
        """)

        conn.commit()
        print("✓ Successfully added 'is_excluded' column!")

        # Verify the change
        cursor.execute("PRAGMA table_info(twitter_posts)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'is_excluded' in columns:
            print("✓ Verified: Column exists in database")

            # Count posts
            cursor.execute("SELECT COUNT(*) FROM twitter_posts")
            count = cursor.fetchone()[0]
            print(f"✓ Total posts in database: {count}")
            print(f"✓ All posts default to is_excluded = False")

            return True
        else:
            print("✗ Error: Column was not added successfully")
            return False

    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    print("=" * 60)
    print("Database Migration: Add is_excluded column")
    print("=" * 60)
    success = migrate_database()
    print("=" * 60)
    if success:
        print("Migration completed successfully!")
    else:
        print("Migration failed!")
    print("=" * 60)
