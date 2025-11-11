# -*- coding: utf-8 -*-
"""
Check database schema and remove UNIQUE constraint from twitter_url if it exists
"""
import sqlite3
import os

db_path = r'c:\Users\Jason\Desktop\Masterarbeit\Twitter-Auswertung\instance\twitter_ter.db'

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 80)
print("DATABASE SCHEMA CHECK")
print("=" * 80)

# Get table schema
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='twitter_posts'")
schema = cursor.fetchone()

if schema:
    print("\nCurrent schema for twitter_posts:")
    print("-" * 80)
    print(schema[0])
    print("-" * 80)

    # Check if UNIQUE constraint exists on twitter_url
    if 'UNIQUE' in schema[0] and 'twitter_url' in schema[0]:
        print("\n⚠️  FOUND: UNIQUE constraint on twitter_url column")
        print("\nThis constraint needs to be removed to allow the same URL in different sessions.")
    else:
        print("\n✓ No UNIQUE constraint found on twitter_url")
else:
    print("\n❌ twitter_posts table not found")

# Get all indexes
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='twitter_posts'")
indexes = cursor.fetchall()

if indexes:
    print("\n\nIndexes on twitter_posts:")
    print("-" * 80)
    for name, sql in indexes:
        print(f"Index: {name}")
        if sql:
            print(f"SQL: {sql}")
        print()
else:
    print("\nNo indexes found on twitter_posts")

conn.close()
print("=" * 80)
