"""
Test how many posts would be exported
"""
from app import app, TwitterPost, AnalysisSession

with app.app_context():
    # Aktive Session
    active_session = AnalysisSession.query.filter_by(is_active=True).first()

    if active_session:
        print(f"Active Session: {active_session.name}\n")

        # Query für Export (wie im PDF/Excel Code)
        posts = TwitterPost.query.filter_by(
            session_id=active_session.id,
            is_reviewed=True,
            is_archived=False,
            is_excluded=False
        ).order_by(TwitterPost.ter_manual.desc().nullslast()).all()

        print(f"Posts für Export: {len(posts)}")
        print("\nListe der Posts:")
        print("-" * 80)

        for idx, post in enumerate(posts, 1):
            ter = post.ter_manual if post.ter_manual is not None else post.ter_automatic
            print(f"{idx:3d}. @{post.twitter_handle:20s} | TER: {ter:6.2f} | Reviewed: {post.is_reviewed} | Excluded: {post.is_excluded}")

        print("-" * 80)
        print(f"\nTotal: {len(posts)} Posts würden exportiert")
