"""
Datenbank-Migration: Fügt trigger_empoerung Spalte hinzu
"""
import sqlite3
import os

def migrate_database():
    """Fügt die trigger_empoerung Spalte zur twitter_posts Tabelle hinzu"""

    db_path = 'twitter_ter.db'

    if not os.path.exists(db_path):
        print(f"[FEHLER] Datenbank nicht gefunden: {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Prüfe ob Spalte bereits existiert
        cursor.execute("PRAGMA table_info(twitter_posts)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'trigger_empoerung' in columns:
            print("[INFO] Spalte 'trigger_empoerung' existiert bereits. Migration nicht nötig.")
            conn.close()
            return True

        # Füge neue Spalte hinzu
        print("[INFO] Füge Spalte 'trigger_empoerung' hinzu...")
        cursor.execute("""
            ALTER TABLE twitter_posts
            ADD COLUMN trigger_empoerung INTEGER DEFAULT 0
        """)

        conn.commit()

        # Verifiziere
        cursor.execute("PRAGMA table_info(twitter_posts)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'trigger_empoerung' in columns:
            print("[OK] Migration erfolgreich! Spalte 'trigger_empoerung' wurde hinzugefügt.")

            # Zähle Posts
            cursor.execute("SELECT COUNT(*) FROM twitter_posts")
            count = cursor.fetchone()[0]
            print(f"[INFO] {count} Posts in der Datenbank.")

            conn.close()
            return True
        else:
            print("[FEHLER] Migration fehlgeschlagen - Spalte wurde nicht hinzugefügt.")
            conn.close()
            return False

    except Exception as e:
        print(f"[FEHLER] Migration fehlgeschlagen: {e}")
        return False

if __name__ == '__main__':
    print("="*60)
    print("Datenbank-Migration: trigger_empoerung hinzufügen")
    print("="*60)

    success = migrate_database()

    if success:
        print("\n[OK] Migration abgeschlossen!")
        print("Du kannst jetzt die App neu starten.")
    else:
        print("\n[FEHLER] Migration fehlgeschlagen!")
        print("Bitte prüfe die Fehlermeldungen oben.")

    print("="*60)
