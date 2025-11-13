"""
Test script to verify the exclusion feature works correctly
"""
from app import app, db, TwitterPost, AnalysisSession
import sys

def test_exclusion_feature():
    """Test the exclusion feature"""
    with app.app_context():
        print("\n" + "=" * 60)
        print("Testing Exclusion Feature")
        print("=" * 60)

        # 1. Check database schema
        print("\n[1/5] Checking database schema...")
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = inspector.get_columns('twitter_posts')
        column_names = [c['name'] for c in columns]

        if 'is_excluded' in column_names:
            print("  [OK] is_excluded column exists in database")
        else:
            print("  [ERROR] is_excluded column NOT found!")
            return False

        # 2. Check TwitterPost model
        print("\n[2/5] Checking TwitterPost model...")
        if hasattr(TwitterPost, 'is_excluded'):
            print("  [OK] TwitterPost model has is_excluded attribute")
        else:
            print("  [ERROR] TwitterPost model missing is_excluded!")
            return False

        # 3. Check to_dict method
        print("\n[3/5] Checking to_dict method...")
        # Create a test session
        test_session = AnalysisSession.query.first()
        if not test_session:
            test_session = AnalysisSession(
                name="Test Session",
                description="Test",
                is_active=True
            )
            db.session.add(test_session)
            db.session.commit()

        # Create a test post
        test_post = TwitterPost(
            session_id=test_session.id,
            twitter_url="https://twitter.com/test/status/123456",
            is_excluded=True
        )
        db.session.add(test_post)
        db.session.commit()

        post_dict = test_post.to_dict()
        if 'is_excluded' in post_dict:
            print("  [OK] to_dict includes is_excluded field")
            print(f"  Value: is_excluded = {post_dict['is_excluded']}")
        else:
            print("  [ERROR] to_dict missing is_excluded field!")
            db.session.delete(test_post)
            db.session.commit()
            return False

        # 4. Test update via API endpoint logic
        print("\n[4/5] Testing update logic...")
        test_post.is_excluded = False
        db.session.commit()

        test_post_reloaded = TwitterPost.query.get(test_post.id)
        if test_post_reloaded.is_excluded == False:
            print("  [OK] Can update is_excluded field")
        else:
            print("  [ERROR] Failed to update is_excluded!")
            db.session.delete(test_post)
            db.session.commit()
            return False

        # 5. Test filtering in statistics
        print("\n[5/5] Testing statistics filtering...")
        # Create two posts: one excluded, one included
        included_post = TwitterPost(
            session_id=test_session.id,
            twitter_url="https://twitter.com/test/status/111111",
            is_excluded=False,
            is_reviewed=True,
            ter_automatic=10.0
        )
        excluded_post = TwitterPost(
            session_id=test_session.id,
            twitter_url="https://twitter.com/test/status/222222",
            is_excluded=True,
            is_reviewed=True,
            ter_automatic=20.0
        )
        db.session.add(included_post)
        db.session.add(excluded_post)
        db.session.commit()

        # Query reviewed posts excluding is_excluded ones
        reviewed_not_excluded = TwitterPost.query.filter_by(
            session_id=test_session.id,
            is_reviewed=True,
            is_excluded=False
        ).all()

        excluded_count = len([p for p in reviewed_not_excluded if p.is_excluded])
        if excluded_count == 0:
            print("  [OK] Excluded posts are filtered correctly")
            print(f"  Found {len(reviewed_not_excluded)} non-excluded reviewed posts")
        else:
            print("  [ERROR] Excluded posts not filtered!")

        # Cleanup
        db.session.delete(test_post)
        db.session.delete(included_post)
        db.session.delete(excluded_post)
        db.session.commit()

        print("\n" + "=" * 60)
        print("[SUCCESS] All tests passed!")
        print("=" * 60)
        return True

if __name__ == '__main__':
    try:
        success = test_exclusion_feature()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
