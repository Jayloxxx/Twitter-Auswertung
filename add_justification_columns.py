"""
Add justification/Begründung columns to TwitterPost table
"""
import sqlite3

def add_justification_columns():
    """Add Text columns for trigger and frame justifications"""

    db_path = 'instance/twitter_ter.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # List of new columns to add
    columns_to_add = [
        # Trigger justifications
        'trigger_angst_begruendung',
        'trigger_wut_begruendung',
        'trigger_empoerung_begruendung',
        'trigger_ekel_begruendung',
        'trigger_identitaet_begruendung',
        'trigger_hoffnung_begruendung',
        # Frame justifications
        'frame_opfer_taeter_begruendung',
        'frame_bedrohung_begruendung',
        'frame_verschwoerung_begruendung',
        'frame_moral_begruendung',
        'frame_historisch_begruendung',
    ]

    added = 0
    skipped = 0

    for column_name in columns_to_add:
        try:
            cursor.execute(f'ALTER TABLE twitter_posts ADD COLUMN {column_name} TEXT')
            print(f"[OK] Added column: {column_name}")
            added += 1
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e).lower():
                print(f"[SKIP] Column already exists: {column_name}")
                skipped += 1
            else:
                print(f"[ERROR] {column_name}: {e}")

    conn.commit()
    conn.close()

    print("\n" + "=" * 60)
    print(f"[SUCCESS] Database migration completed!")
    print(f"  Added: {added} columns")
    print(f"  Skipped (already exist): {skipped}")
    print("=" * 60)

if __name__ == '__main__':
    print("=" * 60)
    print("Adding Justification Columns to Database")
    print("=" * 60)
    add_justification_columns()
