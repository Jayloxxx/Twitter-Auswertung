"""
Reconstruct database from CSV export and backup
"""
import sqlite3
import csv
from datetime import datetime

def reconstruct_database():
    backup_db = 'instance/twitter_ter.db.backup.20251111_131851'
    current_db = 'instance/twitter_ter.db'
    csv_file = 'trigger_frames_converted.csv'

    print("=" * 60)
    print("RECONSTRUCTING DATABASE FROM CSV AND BACKUP")
    print("=" * 60)

    # 1. Read CSV to get trigger/frame data for 79 posts
    print(f"\n[1/5] Reading CSV file: {csv_file}")
    csv_data = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row['twitter_url']
            csv_data[url] = {
                'trigger_angst': int(row['trigger_angst']),
                'trigger_wut': int(row['trigger_wut']),
                'trigger_ekel': int(row['trigger_ekel']),
                'trigger_identitaet': int(row['trigger_identitaet']),
                'trigger_hoffnung': int(row['trigger_hoffnung']),
                'frame_opfer_taeter': int(row['frame_opfer_taeter']),
                'frame_bedrohung': int(row['frame_bedrohung']),
                'frame_verschwoerung': int(row['frame_verschwoerung']),
                'frame_moral': int(row['frame_moral']),
                'frame_historisch': int(row['frame_historisch']),
            }

    print(f"   Found {len(csv_data)} posts in CSV")

    # 2. Create safety backup
    safety_backup = f'instance/twitter_ter.db.before_reconstruction_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    import shutil
    shutil.copy2(current_db, safety_backup)
    print(f"\n[2/5] Created safety backup: {safety_backup}")

    # 3. Copy backup as base
    print(f"\n[3/5] Using backup as base: {backup_db}")
    shutil.copy2(backup_db, current_db)

    # 4. Open current database and check
    conn = sqlite3.connect(current_db)
    cursor = conn.cursor()

    print("\n[4/5] Checking backup data...")
    cursor.execute('SELECT id, name FROM analysis_sessions')
    sessions = cursor.fetchall()
    print(f"   Sessions in backup: {len(sessions)}")
    for s in sessions:
        print(f"   - Session {s[0]}: {s[1]}")

    cursor.execute('SELECT COUNT(*) FROM twitter_posts')
    total_posts = cursor.fetchone()[0]
    print(f"   Total posts in backup: {total_posts}")

    # 5. Update posts with CSV data and mark as reviewed
    print("\n[5/5] Updating posts with CSV data...")

    # First, add missing columns if needed
    cursor.execute("PRAGMA table_info(twitter_posts)")
    columns = [col[1] for col in cursor.fetchall()]

    columns_to_add = {
        'trigger_empoerung': 'INTEGER DEFAULT 0',
        'is_excluded': 'BOOLEAN DEFAULT 0',
        'is_favorite': 'BOOLEAN DEFAULT 0',
        'access_date': 'VARCHAR(100) NULL'
    }

    for col_name, col_def in columns_to_add.items():
        if col_name not in columns:
            print(f"   Adding missing column: {col_name}")
            cursor.execute(f"ALTER TABLE twitter_posts ADD COLUMN {col_name} {col_def}")

    conn.commit()

    # Now update posts with CSV data
    updated_count = 0
    not_found_urls = []

    for url, data in csv_data.items():
        # Try to find post by URL
        cursor.execute('SELECT id FROM twitter_posts WHERE twitter_url = ?', (url,))
        result = cursor.fetchone()

        if result:
            post_id = result[0]
            # Update with CSV data and mark as reviewed
            cursor.execute('''
                UPDATE twitter_posts
                SET trigger_angst = ?,
                    trigger_wut = ?,
                    trigger_empoerung = 0,
                    trigger_ekel = ?,
                    trigger_identitaet = ?,
                    trigger_hoffnung = ?,
                    frame_opfer_taeter = ?,
                    frame_bedrohung = ?,
                    frame_verschwoerung = ?,
                    frame_moral = ?,
                    frame_historisch = ?,
                    is_reviewed = 1
                WHERE id = ?
            ''', (
                data['trigger_angst'],
                data['trigger_wut'],
                data['trigger_ekel'],
                data['trigger_identitaet'],
                data['trigger_hoffnung'],
                data['frame_opfer_taeter'],
                data['frame_bedrohung'],
                data['frame_verschwoerung'],
                data['frame_moral'],
                data['frame_historisch'],
                post_id
            ))
            updated_count += 1
        else:
            not_found_urls.append(url)

    conn.commit()

    print(f"\n   Updated {updated_count} posts with CSV data")
    print(f"   Marked {updated_count} posts as reviewed")

    if not_found_urls:
        print(f"\n   WARNING: {len(not_found_urls)} URLs from CSV not found in backup:")
        for url in not_found_urls[:5]:
            print(f"      - {url}")
        if len(not_found_urls) > 5:
            print(f"      ... and {len(not_found_urls) - 5} more")

    # Final verification
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    cursor.execute('SELECT COUNT(*) FROM twitter_posts')
    total = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM twitter_posts WHERE is_reviewed = 1')
    reviewed = cursor.fetchone()[0]

    cursor.execute('SELECT id, name FROM analysis_sessions')
    for session in cursor.fetchall():
        cursor.execute('SELECT COUNT(*) FROM twitter_posts WHERE session_id = ?', (session[0],))
        session_posts = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM twitter_posts WHERE session_id = ? AND is_reviewed = 1', (session[0],))
        session_reviewed = cursor.fetchone()[0]
        print(f"\nSession {session[0]}: {session[1]}")
        print(f"  Total posts: {session_posts}")
        print(f"  Reviewed posts: {session_reviewed}")

    print(f"\nOVERALL:")
    print(f"  Total posts: {total}")
    print(f"  Reviewed posts: {reviewed}")

    conn.close()

    print("\n" + "=" * 60)
    if reviewed == len(csv_data):
        print(f"[SUCCESS] Reconstructed {reviewed} reviewed posts!")
    else:
        print(f"[PARTIAL SUCCESS] Reconstructed {reviewed} of {len(csv_data)} posts")
    print("=" * 60)

    return reviewed, len(csv_data)

if __name__ == '__main__':
    try:
        reconstructed, expected = reconstruct_database()
        if reconstructed < expected:
            print(f"\nNote: {expected - reconstructed} posts from CSV were not in the backup.")
            print("These posts were added after the backup was created (Nov 11).")
    except Exception as e:
        print(f"\n[ERROR] Reconstruction failed: {e}")
        import traceback
        traceback.print_exc()
