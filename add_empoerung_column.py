"""
Einfache Migration: Fügt trigger_empoerung Spalte hinzu
Kann auch bei laufender App ausgeführt werden (Achtung: App danach neu starten!)
"""
import sqlite3
import os

db_path = 'twitter_ter.db'

print("="*60)
print("Migration: trigger_empoerung Spalte hinzufügen")
print("="*60)

if not os.path.exists(db_path):
    print(f"\n[FEHLER] Datenbank nicht gefunden: {db_path}")
    print("Stelle sicher, dass du im richtigen Verzeichnis bist.")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Prüfe ob Tabelle existiert
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='twitter_posts'")
    if not cursor.fetchone():
        print("\n[FEHLER] Tabelle 'twitter_posts' nicht gefunden!")
        print("Die Datenbank scheint leer zu sein.")
        print("\nBitte:")
        print("1. Stoppe die Flask-App (Strg+C)")
        print("2. Führe dann das Skript 'migrate_trigger_empoerung_live.py' aus")
        conn.close()
        exit(1)

    # Prüfe ob Spalte bereits existiert
    cursor.execute("PRAGMA table_info(twitter_posts)")
    columns = [row[1] for row in cursor.fetchall()]

    if 'trigger_empoerung' in columns:
        print("\n[INFO] Spalte 'trigger_empoerung' existiert bereits!")
        print("Migration nicht nötig.")
        conn.close()
        exit(0)

    # Füge Spalte hinzu
    print("\n[INFO] Füge Spalte 'trigger_empoerung' hinzu...")
    cursor.execute("ALTER TABLE twitter_posts ADD COLUMN trigger_empoerung INTEGER DEFAULT 0")
    conn.commit()

    # Verifiziere
    cursor.execute("PRAGMA table_info(twitter_posts)")
    columns = [row[1] for row in cursor.fetchall()]

    if 'trigger_empoerung' in columns:
        # Zähle Posts
        cursor.execute("SELECT COUNT(*) FROM twitter_posts")
        count = cursor.fetchone()[0]

        print("[OK] Migration erfolgreich!")
        print(f"[INFO] Spalte 'trigger_empoerung' hinzugefügt.")
        print(f"[INFO] {count} Posts in der Datenbank.")
        print("\n" + "="*60)
        print("WICHTIG: Starte die Flask-App neu!")
        print("="*60)
    else:
        print("[FEHLER] Spalte wurde nicht hinzugefügt!")

    conn.close()

except sqlite3.OperationalError as e:
    print(f"\n[FEHLER] Datenbank-Fehler: {e}")
    print("\nWenn die Datenbank gesperrt ist:")
    print("1. Stoppe die Flask-App (Strg+C)")
    print("2. Führe dieses Skript erneut aus")
    exit(1)

except Exception as e:
    print(f"\n[FEHLER] Unerwarteter Fehler: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
