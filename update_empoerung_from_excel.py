"""
Script to update Empörung values and justifications from Excel file
Matches posts via Twitter URL and updates the database
"""

import pandas as pd
import sqlite3
import sys
from urllib.parse import urlparse, parse_qs

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_twitter_url(url):
    """
    Normalizes Twitter URLs to handle different formats:
    - Direct twitter.com links
    - web.archive.org links
    - URLs with/without query parameters
    """
    if not url:
        return None

    url = url.strip()

    # Extract the status ID from the URL
    if 'status/' in url:
        # Get everything after 'status/'
        parts = url.split('status/')
        if len(parts) > 1:
            status_part = parts[1]
            # Remove query parameters and get just the ID
            status_id = status_part.split('?')[0].split('&')[0].strip('/')
            return status_id

    return None

def main():
    excel_path = r'C:\Users\Jason\Desktop\Masterarbeit\Finalendergebnis\trigger_frame_results_20251112_194157.xlsx'
    db_path = r'C:\Users\Jason\Desktop\Masterarbeit\Twitter-Auswertung\instance\twitter_ter.db'

    print("=" * 80)
    print("EMPÖRUNG-UPDATE AUS EXCEL-DATEI")
    print("=" * 80)

    # Read Excel file
    print(f"\n1. Lese Excel-Datei: {excel_path}")
    try:
        df = pd.read_excel(excel_path)
        print(f"   ✓ {len(df)} Zeilen geladen")
    except Exception as e:
        print(f"   ✗ Fehler beim Lesen der Excel-Datei: {e}")
        return

    # Check required columns
    required_cols = ['Twitter URL', 'Empörung Score', 'Empörung - Detaillierte Begründung']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"   ✗ Fehlende Spalten: {missing_cols}")
        return

    # Prepare data from Excel
    print("\n2. Bereite Excel-Daten vor...")
    excel_data = {}
    for idx, row in df.iterrows():
        url = row['Twitter URL']
        empoerung_score = row['Empörung Score']
        empoerung_begr = row['Empörung - Detaillierte Begründung']

        # Normalize URL
        status_id = normalize_twitter_url(url)
        if status_id:
            # Handle NaN values
            if pd.isna(empoerung_score):
                empoerung_score = 0
            if pd.isna(empoerung_begr):
                empoerung_begr = ""

            excel_data[status_id] = {
                'score': int(empoerung_score) if empoerung_score != '' else 0,
                'begruendung': str(empoerung_begr) if empoerung_begr else "",
                'original_url': url
            }

    print(f"   ✓ {len(excel_data)} URLs normalisiert und vorbereitet")

    # Connect to database
    print(f"\n3. Verbinde mit Datenbank: {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("   ✓ Verbindung hergestellt")
    except Exception as e:
        print(f"   ✗ Fehler bei Datenbankverbindung: {e}")
        return

    # Get all posts from database
    print("\n4. Lade Posts aus Datenbank...")
    cursor.execute("SELECT id, twitter_url, trigger_empoerung, is_reviewed, is_excluded FROM twitter_posts")
    db_posts = cursor.fetchall()
    print(f"   ✓ {len(db_posts)} Posts geladen")

    # Match and update
    print("\n5. Matche URLs und aktualisiere Empörung-Werte...")
    matched = 0
    updated = 0
    not_found = 0
    already_correct = 0

    update_log = []

    for post_id, db_url, current_empoerung, is_reviewed, is_excluded in db_posts:
        db_status_id = normalize_twitter_url(db_url)

        if db_status_id and db_status_id in excel_data:
            matched += 1
            excel_entry = excel_data[db_status_id]
            new_score = excel_entry['score']
            new_begr = excel_entry['begruendung']

            # Check if update is needed
            if current_empoerung != new_score:
                # Update the database
                cursor.execute("""
                    UPDATE twitter_posts
                    SET trigger_empoerung = ?,
                        trigger_empoerung_begruendung = ?
                    WHERE id = ?
                """, (new_score, new_begr, post_id))

                updated += 1
                update_log.append({
                    'post_id': post_id,
                    'url': db_url,
                    'old_score': current_empoerung,
                    'new_score': new_score,
                    'is_reviewed': is_reviewed,
                    'is_excluded': is_excluded
                })
            else:
                already_correct += 1
        else:
            not_found += 1

    # Commit changes
    conn.commit()
    print(f"   ✓ Änderungen gespeichert")

    # Statistics
    print("\n" + "=" * 80)
    print("ERGEBNISSE")
    print("=" * 80)
    print(f"Posts in Datenbank:        {len(db_posts)}")
    print(f"Einträge in Excel:         {len(excel_data)}")
    print(f"Erfolgreich gematcht:      {matched}")
    print(f"Aktualisiert:              {updated}")
    print(f"Bereits korrekt:           {already_correct}")
    print(f"Nicht in Excel gefunden:   {not_found}")

    # Detailed update log
    if update_log:
        print("\n" + "=" * 80)
        print("DETAILLIERTE UPDATES")
        print("=" * 80)
        for entry in update_log:
            status = []
            if entry['is_reviewed']:
                status.append("reviewed")
            if entry['is_excluded']:
                status.append("excluded")
            status_str = f" [{', '.join(status)}]" if status else ""

            print(f"Post ID {entry['post_id']}{status_str}:")
            print(f"  URL: {entry['url']}")
            print(f"  Empörung: {entry['old_score']} → {entry['new_score']}")
            print()

    # Verify the important 69 posts (is_reviewed=True, is_excluded=False)
    print("\n" + "=" * 80)
    print("VERIFIKATION DER 69 WICHTIGEN POSTS")
    print("=" * 80)
    cursor.execute("""
        SELECT COUNT(*),
               SUM(CASE WHEN trigger_empoerung > 0 THEN 1 ELSE 0 END) as with_empoerung
        FROM twitter_posts
        WHERE is_reviewed = 1 AND is_excluded = 0
    """)
    result = cursor.fetchone()
    important_count = result[0]
    important_with_empoerung = result[1]

    print(f"Wichtige Posts (reviewed & not excluded): {important_count}")
    print(f"Davon mit Empörung > 0:                   {important_with_empoerung}")

    # Verify all 80 posts
    print("\n" + "=" * 80)
    print("VERIFIKATION ALLER POSTS")
    print("=" * 80)
    cursor.execute("""
        SELECT COUNT(*),
               SUM(CASE WHEN trigger_empoerung > 0 THEN 1 ELSE 0 END) as with_empoerung
        FROM twitter_posts
    """)
    result = cursor.fetchone()
    all_count = result[0]
    all_with_empoerung = result[1]

    print(f"Alle Posts:                {all_count}")
    print(f"Davon mit Empörung > 0:    {all_with_empoerung}")

    # Show Empörung distribution
    print("\n" + "=" * 80)
    print("EMPÖRUNG-VERTEILUNG (alle Posts)")
    print("=" * 80)
    cursor.execute("""
        SELECT trigger_empoerung, COUNT(*) as count
        FROM twitter_posts
        GROUP BY trigger_empoerung
        ORDER BY trigger_empoerung
    """)
    for score, count in cursor.fetchall():
        print(f"Score {score}: {count} Posts")

    print("\n" + "=" * 80)
    print("EMPÖRUNG-VERTEILUNG (69 wichtige Posts)")
    print("=" * 80)
    cursor.execute("""
        SELECT trigger_empoerung, COUNT(*) as count
        FROM twitter_posts
        WHERE is_reviewed = 1 AND is_excluded = 0
        GROUP BY trigger_empoerung
        ORDER BY trigger_empoerung
    """)
    for score, count in cursor.fetchall():
        print(f"Score {score}: {count} Posts")

    conn.close()
    print("\n" + "=" * 80)
    print("✓ FERTIG!")
    print("=" * 80)

if __name__ == '__main__':
    main()
