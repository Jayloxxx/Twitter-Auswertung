"""
Force reload app.py and initialize database with is_excluded column
"""
import sys
import importlib

# Remove app from cache if it exists
if 'app' in sys.modules:
    del sys.modules['app']

# Now import fresh
from app import app, db, TwitterPost

def init_database():
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()
        print("[OK] Database tables created successfully")

        # Verify TwitterPost has is_excluded attribute
        import inspect
        post_attrs = [attr for attr in dir(TwitterPost) if not attr.startswith('_')]

        if 'is_excluded' in post_attrs:
            print("[OK] TwitterPost model has is_excluded attribute")
        else:
            print("[ERROR] TwitterPost model does NOT have is_excluded attribute")
            print(f"Available attributes: {post_attrs}")
            return

        # Create a test post to verify database schema
        from sqlalchemy import inspect as sql_inspect
        inspector = sql_inspect(db.engine)

        columns = inspector.get_columns('twitter_posts')
        column_names = [c['name'] for c in columns]

        print(f"\nColumns in twitter_posts table:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")

        if 'is_excluded' in column_names:
            print("\n[SUCCESS] is_excluded column exists in database!")
        else:
            print("\n[ERROR] is_excluded column NOT found in database!")

if __name__ == '__main__':
    print("=" * 60)
    print("Force Initialize Database with is_excluded")
    print("=" * 60)
    init_database()
    print("=" * 60)
