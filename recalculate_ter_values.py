"""
Skript zur Neuberechnung aller TER-Werte nach Korrektur der Gewichtung
Retweets ×3, Replies ×4 (vorher falsch: Replies ×3, Retweets ×4)
"""

from app import app, db, TwitterPost, TERCalculator
import math

def recalculate_all_ter():
    """Berechnet alle TER-Werte in der Datenbank neu"""

    with app.app_context():
        # Alle Posts abrufen
        posts = TwitterPost.query.all()

        print(f"Starte Neuberechnung für {len(posts)} Posts...")
        updated_count = 0

        for post in posts:
            try:
                # TER mit korrigierter Gewichtung neu berechnen
                ter_result = TERCalculator.calculate(
                    likes=post.likes,
                    bookmarks=post.bookmarks,
                    replies=post.replies,
                    retweets=post.retweets,
                    quotes=post.quotes,
                    views=post.views
                )

                # Werte aktualisieren
                post.ter_automatic = ter_result['ter_sqrt']
                post.ter_linear = ter_result['ter_linear']
                post.weighted_engagement = ter_result['weighted_engagement']
                post.total_interactions = ter_result['total_interactions']
                post.engagement_level = ter_result['engagement_level']
                post.engagement_level_code = ter_result['engagement_level_code']

                updated_count += 1

                if updated_count % 100 == 0:
                    print(f"  {updated_count} Posts aktualisiert...")

            except Exception as e:
                print(f"Fehler bei Post ID {post.id}: {str(e)}")
                continue

        # Alle Änderungen speichern
        db.session.commit()

        print(f"\nErfolgreich {updated_count} von {len(posts)} Posts aktualisiert!")
        print("\nBeispiel-Vergleich (erste 5 Posts):")
        print("-" * 80)

        # Beispiele anzeigen
        sample_posts = TwitterPost.query.limit(5).all()
        for post in sample_posts:
            print(f"\nPost ID {post.id}:")
            print(f"  Likes: {post.likes}, Bookmarks: {post.bookmarks}, Replies: {post.replies}, Retweets: {post.retweets}, Quotes: {post.quotes}")
            print(f"  Weighted Engagement: {post.weighted_engagement}")
            print(f"  TER-sqrt: {post.ter_automatic:.2f}")
            print(f"  TER linear: {post.ter_linear:.2f}")
            print(f"  Engagement Level: {post.engagement_level}")

if __name__ == '__main__':
    recalculate_all_ter()
