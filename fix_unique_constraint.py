# -*- coding: utf-8 -*-
"""
Fix UNIQUE constraint on twitter_url column

This script removes the UNIQUE constraint from twitter_url to allow
the same URL to exist in different sessions.
"""
import sqlite3
import os
import shutil
from datetime import datetime

db_path = r'c:\Users\Jason\Desktop\Masterarbeit\Twitter-Auswertung\instance\twitter_ter.db'

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

print("=" * 80)
print("FIX UNIQUE CONSTRAINT ON TWITTER_URL")
print("=" * 80)

# Create backup
backup_path = db_path + f'.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
print(f"\n[1/4] Creating backup: {backup_path}")
shutil.copy2(db_path, backup_path)
print("      Backup created successfully!")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("\n[2/4] Checking current schema...")
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='twitter_posts'")
    old_schema = cursor.fetchone()[0]

    if 'UNIQUE (twitter_url)' in old_schema or 'twitter_url VARCHAR(500) UNIQUE' in old_schema:
        print("      UNIQUE constraint found - will be removed")
    else:
        print("      No UNIQUE constraint found - nothing to do")
        conn.close()
        exit(0)

    print("\n[3/4] Recreating table without UNIQUE constraint...")

    # Start transaction
    cursor.execute("BEGIN TRANSACTION")

    # Create new table without UNIQUE constraint
    cursor.execute("""
        CREATE TABLE twitter_posts_new (
            id INTEGER NOT NULL PRIMARY KEY,
            session_id INTEGER NOT NULL,
            factcheck_url VARCHAR(500),
            factcheck_title TEXT,
            factcheck_date VARCHAR(100),
            factcheck_rating VARCHAR(100),
            twitter_url VARCHAR(500) NOT NULL,
            twitter_author VARCHAR(200),
            twitter_handle VARCHAR(100),
            twitter_followers INTEGER,
            twitter_content TEXT,
            twitter_date VARCHAR(100),
            likes INTEGER,
            retweets INTEGER,
            replies INTEGER,
            bookmarks INTEGER,
            quotes INTEGER,
            views INTEGER,
            likes_manual INTEGER,
            retweets_manual INTEGER,
            replies_manual INTEGER,
            bookmarks_manual INTEGER,
            quotes_manual INTEGER,
            views_manual INTEGER,
            ter_automatic FLOAT,
            ter_linear FLOAT,
            ter_manual FLOAT,
            weighted_engagement INTEGER,
            total_interactions INTEGER,
            engagement_level VARCHAR(100),
            engagement_level_code VARCHAR(20),
            trigger_angst INTEGER DEFAULT 0,
            trigger_wut INTEGER DEFAULT 0,
            trigger_ekel INTEGER DEFAULT 0,
            trigger_identitaet INTEGER DEFAULT 0,
            trigger_hoffnung INTEGER DEFAULT 0,
            frame_opfer_taeter INTEGER DEFAULT 0,
            frame_bedrohung INTEGER DEFAULT 0,
            frame_verschwoerung INTEGER DEFAULT 0,
            frame_moral INTEGER DEFAULT 0,
            frame_historisch INTEGER DEFAULT 0,
            is_reviewed BOOLEAN,
            is_archived BOOLEAN,
            notes TEXT,
            created_at DATETIME,
            updated_at DATETIME,
            FOREIGN KEY (session_id) REFERENCES analysis_sessions (id)
        )
    """)

    # Copy all data from old table to new table
    cursor.execute("""
        INSERT INTO twitter_posts_new
        SELECT
            id, session_id, factcheck_url, factcheck_title, factcheck_date, factcheck_rating,
            twitter_url, twitter_author, twitter_handle, twitter_followers, twitter_content, twitter_date,
            likes, retweets, replies, bookmarks, quotes, views,
            likes_manual, retweets_manual, replies_manual, bookmarks_manual, quotes_manual, views_manual,
            ter_automatic, ter_linear, ter_manual, weighted_engagement, total_interactions,
            engagement_level, engagement_level_code,
            trigger_angst, trigger_wut, trigger_ekel, trigger_identitaet, trigger_hoffnung,
            frame_opfer_taeter, frame_bedrohung, frame_verschwoerung, frame_moral, frame_historisch,
            is_reviewed, is_archived, notes, created_at, updated_at
        FROM twitter_posts
    """)

    rows_copied = cursor.rowcount
    print(f"      Copied {rows_copied} rows to new table")

    # Drop old table
    cursor.execute("DROP TABLE twitter_posts")

    # Rename new table to original name
    cursor.execute("ALTER TABLE twitter_posts_new RENAME TO twitter_posts")

    # Commit transaction
    cursor.execute("COMMIT")

    print("      Table recreated successfully!")

    print("\n[4/4] Verifying new schema...")
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='twitter_posts'")
    new_schema = cursor.fetchone()[0]

    if 'UNIQUE (twitter_url)' not in new_schema and 'twitter_url VARCHAR(500) UNIQUE' not in new_schema:
        print("      SUCCESS: UNIQUE constraint removed!")
    else:
        print("      WARNING: UNIQUE constraint still exists")

    print("\n" + "=" * 80)
    print("MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\nBackup saved at: {backup_path}")
    print(f"Rows migrated: {rows_copied}")
    print("\nYou can now import CSV files with duplicate twitter_url values.")

except Exception as e:
    print(f"\nERROR: {str(e)}")
    cursor.execute("ROLLBACK")
    print("\nRolling back changes...")
    print(f"Your backup is safe at: {backup_path}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
