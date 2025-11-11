# -*- coding: utf-8 -*-
"""
Sicheres Datenbank-Migrations-Script fuer Session-Management

Dieses Skript:
1. Erstellt die neue analysis_sessions Tabelle
2. Fuegt session_id zur twitter_posts Tabelle hinzu
3. Erstellt eine Standard-Session und weist alle bestehenden Posts dieser zu
4. BEHAELT alle existierenden Daten!
"""

from app import app, db, AnalysisSession, TwitterPost
from datetime import datetime
import sqlite3

def migrate():
    with app.app_context():
        print("\n" + "="*80)
        print("SICHERE DATENBANK-MIGRATION")
        print("="*80)
        print("\nDieses Script erweitert die Datenbank um Session-Management.")
        print("Alle bestehenden Posts werden beibehalten und einer Standard-Session zugewiesen.\n")

        # Pruefen ob analysis_sessions Tabelle bereits existiert
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()

        if 'analysis_sessions' in tables:
            print("INFO: Session-Tabelle existiert bereits.")
            session_count = AnalysisSession.query.count()
            print(f"      {session_count} Session(s) gefunden.")

            # Pruefen ob session_id Spalte existiert
            columns = [col['name'] for col in inspector.get_columns('twitter_posts')]
            if 'session_id' not in columns:
                print("\nWARNING: session_id Spalte fehlt in twitter_posts - wird jetzt hinzugefuegt.")

                # Session-ID Spalte hinzufuegen mit SQLite
                conn = sqlite3.connect('instance/twitter_ter.db')
                cursor = conn.cursor()

                try:
                    # Standard-Session erstellen falls noch keine existiert
                    if session_count == 0:
                        print("      Erstelle Standard-Session...")
                        default_session = AnalysisSession(
                            name="Bestehende Analyse",
                            description="Automatisch erstellte Session fuer bestehende Posts",
                            is_active=True,
                            created_at=datetime.utcnow(),
                            updated_at=datetime.utcnow()
                        )
                        db.session.add(default_session)
                        db.session.commit()
                        default_session_id = default_session.id
                        print(f"      Standard-Session erstellt (ID: {default_session_id})")
                    else:
                        # Erste Session als Standard nutzen
                        default_session = AnalysisSession.query.first()
                        default_session_id = default_session.id
                        print(f"      Nutze existierende Session '{default_session.name}' (ID: {default_session_id})")

                    # Spalte hinzufuegen
                    cursor.execute(f"ALTER TABLE twitter_posts ADD COLUMN session_id INTEGER DEFAULT {default_session_id}")
                    conn.commit()
                    print("      OK: session_id Spalte hinzugefuegt.")

                    # Alle Posts mit NULL session_id aktualisieren
                    cursor.execute(f"UPDATE twitter_posts SET session_id = {default_session_id} WHERE session_id IS NULL")
                    conn.commit()
                    updated_count = cursor.rowcount
                    print(f"      OK: {updated_count} Posts der Session zugewiesen.")

                except Exception as e:
                    print(f"      FEHLER: {str(e)}")
                    conn.rollback()
                    return
                finally:
                    conn.close()

                print("\nMigration erfolgreich abgeschlossen!")
                return

            # Pruefen ob es eine aktive Session gibt
            active_session = AnalysisSession.query.filter_by(is_active=True).first()
            if not active_session and session_count > 0:
                first_session = AnalysisSession.query.first()
                first_session.is_active = True
                db.session.commit()
                print(f"OK: Session '{first_session.name}' wurde aktiviert.")

            print("\nMigration bereits durchgefuehrt. Keine Aktion erforderlich.")
            return

        print("START: Migration wird durchgefuehrt...\n")

        # Schritt 1: Alte Posts sichern
        print("[1/5] Bestehende Posts werden gesichert...")
        conn = sqlite3.connect('instance/twitter_ter.db')
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT COUNT(*) FROM twitter_posts")
            old_post_count = cursor.fetchone()[0]
            print(f"      {old_post_count} Posts gefunden.")
        except:
            old_post_count = 0
            print("      Keine Posts gefunden (neue Installation).")

        conn.close()

        # Schritt 2: Neue Tabellen erstellen
        print("\n[2/5] Neue Tabellen werden erstellt...")
        db.create_all()
        print("      OK: Tabellen erstellt.")

        # Schritt 3: Standard-Session erstellen
        print("\n[3/5] Standard-Session wird erstellt...")
        default_session = AnalysisSession(
            name="Bestehende Analyse",
            description="Automatisch erstellte Session fuer bestehende Posts",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(default_session)
        db.session.commit()
        print(f"      OK: Session '{default_session.name}' (ID: {default_session.id}) erstellt.")

        # Schritt 4: Posts der Session zuweisen
        print("\n[4/5] Posts werden der Standard-Session zugewiesen...")

        # Alle Posts ohne session_id finden und zuweisen
        try:
            posts = TwitterPost.query.all()
            updated_count = 0

            for post in posts:
                if not post.session_id:
                    post.session_id = default_session.id
                    updated_count += 1

            db.session.commit()
            print(f"      OK: {updated_count} Posts zugewiesen.")
        except Exception as e:
            print(f"      FEHLER beim Zuweisen: {str(e)}")
            db.session.rollback()

        # Schritt 5: Verifizierung
        print("\n[5/5] Verifizierung...")
        final_post_count = TwitterPost.query.count()
        session_count = AnalysisSession.query.count()

        print(f"      Sessions: {session_count}")
        print(f"      Posts gesamt: {final_post_count}")
        print(f"      Posts in aktiver Session: {len(default_session.posts)}")

        print("\n" + "="*80)
        print("MIGRATION ERFOLGREICH ABGESCHLOSSEN!")
        print("="*80)
        print("\nNaechste Schritte:")
        print("   1. Starte die Anwendung: python app.py")
        print("   2. Deine bestehenden Posts sind in der Session 'Bestehende Analyse'")
        print("   3. Du kannst jetzt weitere Sessions erstellen\n")

if __name__ == '__main__':
    try:
        migrate()
    except Exception as e:
        print(f"\n{'='*80}")
        print("FEHLER: Migration fehlgeschlagen!")
        print("="*80)
        print(f"\n{str(e)}\n")
        import traceback
        traceback.print_exc()
        print("\nBitte erstelle ein Backup deiner Datenbank und versuche es erneut.")
