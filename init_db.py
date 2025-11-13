"""
Initialize database with current schema including is_excluded field
"""
from app import app, db

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("[OK] Database tables created successfully")

        # Verify the schema
        from sqlalchemy import inspect
        inspector = inspect(db.engine)

        print("\nTables created:")
        for table_name in inspector.get_table_names():
            print(f"  - {table_name}")
            columns = inspector.get_columns(table_name)
            is_excluded_found = False
            for col in columns:
                if col['name'] == 'is_excluded':
                    is_excluded_found = True
                    print(f"    [OK] is_excluded column found!")
                    break

            if table_name == 'twitter_posts' and not is_excluded_found:
                print(f"    [WARNING] is_excluded column NOT found in twitter_posts!")

if __name__ == '__main__':
    print("=" * 60)
    print("Initializing Database")
    print("=" * 60)
    init_database()
    print("=" * 60)
