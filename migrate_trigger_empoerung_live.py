"""
Live-Migration: Fügt trigger_empoerung Spalte zur laufenden Datenbank hinzu
WICHTIG: App muss gestoppt sein!
"""
from app import app, db
import sys

def migrate():
    """Fügt die trigger_empoerung Spalte hinzu"""

    with app.app_context():
        try:
            # Prüfe ob Spalte bereits existiert
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)

            # Hole alle Spalten der twitter_posts Tabelle
            columns = [col['name'] for col in inspector.get_columns('twitter_posts')]

            if 'trigger_empoerung' in columns:
                print("[INFO] Spalte 'trigger_empoerung' existiert bereits.")
                return True

            print("[INFO] Füge Spalte 'trigger_empoerung' hinzu...")

            # Führe ALTER TABLE direkt aus
            with db.engine.connect() as conn:
                conn.execute(text("""
                    ALTER TABLE twitter_posts
                    ADD COLUMN trigger_empoerung INTEGER DEFAULT 0
                """))
                conn.commit()

            # Verifiziere
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('twitter_posts')]

            if 'trigger_empoerung' in columns:
                print("[OK] Migration erfolgreich!")
                print(f"[INFO] Spalte 'trigger_empoerung' wurde hinzugefügt.")
                return True
            else:
                print("[FEHLER] Spalte wurde nicht hinzugefügt.")
                return False

        except Exception as e:
            print(f"[FEHLER] Migration fehlgeschlagen: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("="*60)
    print("Live-Migration: trigger_empoerung hinzufügen")
    print("="*60)
    print("\nWICHTIG: Stelle sicher, dass die Flask-App NICHT läuft!")
    print("Drücke Enter zum Fortfahren oder Strg+C zum Abbrechen...")
    input()

    success = migrate()

    if success:
        print("\n" + "="*60)
        print("[OK] Migration abgeschlossen!")
        print("Du kannst jetzt die App neu starten.")
        print("="*60)
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("[FEHLER] Migration fehlgeschlagen!")
        print("="*60)
        sys.exit(1)
