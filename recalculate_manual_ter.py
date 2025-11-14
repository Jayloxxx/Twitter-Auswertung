"""
Skript zur Neuberechnung aller manuellen TER-Werte
Nur für Posts mit manuellen Metriken (likes_manual, retweets_manual, etc.)
"""

from app import app, db, TwitterPost, TERCalculator
import math

def recalculate_manual_ter():
    """Berechnet alle manuellen TER-Werte neu"""

    with app.app_context():
        # Alle Posts mit ter_manual Werten
        posts = TwitterPost.query.filter(TwitterPost.ter_manual.isnot(None)).all()

        print(f"Starte Neuberechnung fuer {len(posts)} Posts mit manuellen TER-Werten...")
        updated_count = 0

        for post in posts:
            try:
                # Manuelle Werte verwenden, falls vorhanden, sonst automatische
                likes = post.likes_manual if post.likes_manual is not None else post.likes
                bookmarks = post.bookmarks_manual if post.bookmarks_manual is not None else post.bookmarks
                replies = post.replies_manual if post.replies_manual is not None else post.replies
                retweets = post.retweets_manual if post.retweets_manual is not None else post.retweets
                quotes = post.quotes_manual if post.quotes_manual is not None else post.quotes
                views = post.views_manual if post.views_manual is not None else post.views

                # TER mit korrigierter Gewichtung neu berechnen
                ter_result = TERCalculator.calculate(
                    likes=likes,
                    bookmarks=bookmarks,
                    replies=replies,
                    retweets=retweets,
                    quotes=quotes,
                    views=views
                )

                # Nur ter_manual aktualisieren
                post.ter_manual = ter_result['ter_sqrt']

                updated_count += 1

                if updated_count <= 5 or updated_count % 20 == 0:
                    print(f"  Post ID {post.id}: ter_manual = {post.ter_manual:.2f}")
                    print(f"    Metriken: L={likes}, B={bookmarks}, Rep={replies}, Ret={retweets}, Q={quotes}, V={views}")
                    print(f"    Weighted Engagement: {ter_result['weighted_engagement']}")

            except Exception as e:
                print(f"Fehler bei Post ID {post.id}: {str(e)}")
                continue

        # Alle Änderungen speichern
        db.session.commit()

        print(f"\nErfolgreich {updated_count} von {len(posts)} Posts mit manuellen TER-Werten aktualisiert!")

if __name__ == '__main__':
    recalculate_manual_ter()
