#!/usr/bin/env python3
"""
Script to update app.py to filter out posts where is_excluded=True in all statistics calculations.

This script identifies all places where posts are filtered for statistics and adds the
is_excluded filter after filtering out archived posts.

The filter logic becomes:
1. Get all posts from active session
2. Filter out archived posts
3. **NEW: Filter out excluded posts (where is_excluded=True)**
4. Filter to only reviewed posts
5. Calculate statistics
"""

import re
import sys
from pathlib import Path


def read_file(filepath):
    """Read file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filepath, content):
    """Write content to file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def update_get_statistics(content):
    """
    Update get_statistics() function to filter out excluded posts.

    Pattern: Lines 967-973
    - Line 967: archived_posts = [p for p in all_posts if p.is_archived]
    - Line 970: active_posts = [p for p in all_posts if not p.is_archived]
    - Line 973: posts = [p for p in active_posts if p.is_reviewed]

    We need to add a filter between line 970 and 973 to exclude posts where is_excluded=True
    """

    # Pattern: Find the section where active_posts is filtered to posts
    old_pattern = re.compile(
        r'(    # Nur nicht-archivierte Posts für Statistiken\n'
        r'    active_posts = \[p for p in all_posts if not p\.is_archived\]\n)'
        r'\n'
        r'(    # NUR REVIEWED POSTS für Statistiken verwenden \(von nicht-archivierten\)\n'
        r'    posts = \[p for p in active_posts if p\.is_reviewed\])',
        re.MULTILINE
    )

    new_code = (
        r'\1'
        r'\n'
        r'    # Filter out excluded posts (is_excluded=True)\n'
        r'    active_posts = [p for p in active_posts if not p.is_excluded]\n'
        r'\n'
        r'\2'
    )

    updated = old_pattern.sub(new_code, content)

    if updated == content:
        print("WARNING: Could not find pattern in get_statistics()")
        return content, False

    print("+ Updated get_statistics() - Added is_excluded filter after archived filter")
    return updated, True


def update_get_distribution(content):
    """
    Update get_distribution() function to filter out excluded posts.

    Pattern: Lines 1050-1051
    - Line 1051: posts = TwitterPost.query.filter_by(session_id=active_session.id).all()

    This doesn't filter for is_reviewed but should still filter out archived and excluded posts.
    """

    # Pattern: Find the query that gets all posts for distribution
    old_pattern = re.compile(
        r'(    # NUR Posts der aktiven Session\n'
        r'    posts = TwitterPost\.query\.filter_by\(session_id=active_session\.id\)\.all\(\))',
        re.MULTILINE
    )

    new_code = (
        r'\1\n'
        r'\n'
        r'    # Filter out archived and excluded posts\n'
        r'    posts = [p for p in posts if not p.is_archived and not p.is_excluded]'
    )

    updated = old_pattern.sub(new_code, content)

    if updated == content:
        print("WARNING: Could not find pattern in get_distribution()")
        return content, False

    print("+ Updated get_distribution() - Added is_archived and is_excluded filters")
    return updated, True


def update_get_timeline_stats(content):
    """
    Update get_timeline_stats() function to filter out excluded posts.

    Pattern: Lines 1083-1087
    Uses query.filter_by() with is_reviewed=True, is_archived=False
    Need to add is_excluded=False
    """

    # Pattern: Find the query in get_timeline_stats
    old_pattern = re.compile(
        r'(    # NUR REVIEWED POSTS DER AKTIVEN SESSION \(OHNE ARCHIVIERTE\)\n'
        r'    all_posts = TwitterPost\.query\.filter_by\(\n'
        r'        session_id=active_session\.id,\n'
        r'        is_reviewed=True,\n'
        r'        is_archived=False\n'
        r'    \)\.all\(\))',
        re.MULTILINE
    )

    new_code = (
        r'    # NUR REVIEWED POSTS DER AKTIVEN SESSION (OHNE ARCHIVIERTE UND EXCLUDED)\n'
        r'    all_posts = TwitterPost.query.filter_by(\n'
        r'        session_id=active_session.id,\n'
        r'        is_reviewed=True,\n'
        r'        is_archived=False,\n'
        r'        is_excluded=False\n'
        r'    ).all()'
    )

    updated = old_pattern.sub(new_code, content)

    if updated == content:
        print("WARNING: Could not find pattern in get_timeline_stats()")
        return content, False

    print("+ Updated get_timeline_stats() - Added is_excluded=False to query")
    return updated, True


def update_get_advanced_stats(content):
    """
    Update get_advanced_stats() function to filter out excluded posts.

    Pattern: Lines 1199-1204
    Uses query.filter_by() with is_reviewed=True, is_archived=False
    Need to add is_excluded=False
    """

    # Pattern: Find the query in get_advanced_stats
    old_pattern = re.compile(
        r'(    # NUR REVIEWED POSTS DER AKTIVEN SESSION mit TER-Werten \(OHNE ARCHIVIERTE\)\n'
        r'    posts = TwitterPost\.query\.filter_by\(\n'
        r'        session_id=active_session\.id,\n'
        r'        is_reviewed=True,\n'
        r'        is_archived=False\n'
        r'    \)\.all\(\))',
        re.MULTILINE
    )

    new_code = (
        r'    # NUR REVIEWED POSTS DER AKTIVEN SESSION mit TER-Werten (OHNE ARCHIVIERTE UND EXCLUDED)\n'
        r'    posts = TwitterPost.query.filter_by(\n'
        r'        session_id=active_session.id,\n'
        r'        is_reviewed=True,\n'
        r'        is_archived=False,\n'
        r'        is_excluded=False\n'
        r'    ).all()'
    )

    updated = old_pattern.sub(new_code, content)

    if updated == content:
        print("WARNING: Could not find pattern in get_advanced_stats()")
        return content, False

    print("+ Updated get_advanced_stats() - Added is_excluded=False to query")
    return updated, True


def update_export_pdf(content):
    """
    Update export_reviewed_posts_pdf() function to filter out excluded posts.

    Pattern: Lines 2042-2046
    Uses query.filter_by() with is_reviewed=True, is_archived=False
    Need to add is_excluded=False
    """

    # Pattern: Find the query in export_reviewed_posts_pdf
    old_pattern = re.compile(
        r'(        # Hole alle reviewed Posts der aktiven Session \(ohne archivierte\)\n'
        r'        posts = TwitterPost\.query\.filter_by\(\n'
        r'            session_id=active_session\.id,\n'
        r'            is_reviewed=True,\n'
        r'            is_archived=False\n'
        r'        \)\.order_by\(TwitterPost\.ter_manual\.desc\(\)\.nullslast\(\)\)\.all\(\))',
        re.MULTILINE
    )

    new_code = (
        r'        # Hole alle reviewed Posts der aktiven Session (ohne archivierte und excluded)\n'
        r'        posts = TwitterPost.query.filter_by(\n'
        r'            session_id=active_session.id,\n'
        r'            is_reviewed=True,\n'
        r'            is_archived=False,\n'
        r'            is_excluded=False\n'
        r'        ).order_by(TwitterPost.ter_manual.desc().nullslast()).all()'
    )

    updated = old_pattern.sub(new_code, content)

    if updated == content:
        print("WARNING: Could not find pattern in export_reviewed_posts_pdf()")
        return content, False

    print("+ Updated export_reviewed_posts_pdf() - Added is_excluded=False to query")
    return updated, True


def update_export_excel(content):
    """
    Update export_reviewed_posts_excel() function to filter out excluded posts.

    Pattern: Lines 2367-2372
    Uses query.filter_by() with is_reviewed=True, is_archived=False
    Need to add is_excluded=False
    """

    # Pattern: Find the query in export_reviewed_posts_excel
    old_pattern = re.compile(
        r'(        # Hole alle reviewed Posts der aktiven Session \(ohne archivierte\)\n'
        r'        posts = TwitterPost\.query\.filter_by\(\n'
        r'            session_id=active_session\.id,\n'
        r'            is_reviewed=True,\n'
        r'            is_archived=False\n'
        r'        \)\.order_by\(TwitterPost\.ter_manual\.desc\(\)\.nullslast\(\)\)\.all\(\))',
        re.MULTILINE
    )

    new_code = (
        r'        # Hole alle reviewed Posts der aktiven Session (ohne archivierte und excluded)\n'
        r'        posts = TwitterPost.query.filter_by(\n'
        r'            session_id=active_session.id,\n'
        r'            is_reviewed=True,\n'
        r'            is_archived=False,\n'
        r'            is_excluded=False\n'
        r'        ).order_by(TwitterPost.ter_manual.desc().nullslast()).all()'
    )

    updated = old_pattern.sub(new_code, content)

    if updated == content:
        print("WARNING: Could not find pattern in export_reviewed_posts_excel()")
        return content, False

    print("+ Updated export_reviewed_posts_excel() - Added is_excluded=False to query")
    return updated, True


def update_analysis_session_to_dict(content):
    """
    Update AnalysisSession.to_dict() method to filter out excluded posts from counts.

    Pattern: Lines 66-67
    - Line 66: 'reviewed_count': len([p for p in self.posts if p.is_reviewed]),
    - Line 67: 'archived_count': len([p for p in self.posts if p.is_archived]),

    We need to exclude is_excluded posts from reviewed_count
    """

    # Pattern: Find the reviewed_count line in to_dict
    old_pattern = re.compile(
        r"(            'reviewed_count': len\(\[p for p in self\.posts if p\.is_reviewed\]\),)",
        re.MULTILINE
    )

    new_code = (
        r"            'reviewed_count': len([p for p in self.posts if p.is_reviewed and not p.is_excluded]),"
    )

    updated = old_pattern.sub(new_code, content)

    if updated == content:
        print("WARNING: Could not find pattern in AnalysisSession.to_dict()")
        return content, False

    print("+ Updated AnalysisSession.to_dict() - Excluded is_excluded posts from reviewed_count")
    return updated, True


def main():
    """Main function to update app.py"""

    # Get the path to app.py
    script_dir = Path(__file__).parent
    app_file = script_dir / 'app.py'

    if not app_file.exists():
        print(f"ERROR: app.py not found at {app_file}")
        sys.exit(1)

    print(f"Reading {app_file}")
    content = read_file(app_file)
    original_content = content

    print("\nApplying updates...\n")

    # Apply all updates
    updates_applied = 0

    content, success = update_analysis_session_to_dict(content)
    if success:
        updates_applied += 1

    content, success = update_get_statistics(content)
    if success:
        updates_applied += 1

    content, success = update_get_distribution(content)
    if success:
        updates_applied += 1

    content, success = update_get_timeline_stats(content)
    if success:
        updates_applied += 1

    content, success = update_get_advanced_stats(content)
    if success:
        updates_applied += 1

    content, success = update_export_pdf(content)
    if success:
        updates_applied += 1

    content, success = update_export_excel(content)
    if success:
        updates_applied += 1

    # Check if anything was updated
    if content == original_content:
        print("\nNo changes were made. The patterns may have already been updated or not found.")
        sys.exit(1)

    # Create backup
    backup_file = app_file.with_suffix('.py.backup')
    print(f"\nCreating backup at {backup_file}")
    write_file(backup_file, original_content)

    # Write updated content
    print(f"Writing updated content to {app_file}")
    write_file(app_file, content)

    print(f"\nSUCCESS! Applied {updates_applied} updates to app.py")
    print(f"Backup saved to {backup_file}")
    print("\nSummary of changes:")
    print("   1. AnalysisSession.to_dict() - Excludes is_excluded posts from reviewed_count")
    print("   2. get_statistics() - Filters out posts where is_excluded=True")
    print("   3. get_distribution() - Filters out archived and excluded posts")
    print("   4. get_timeline_stats() - Added is_excluded=False to query filter")
    print("   5. get_advanced_stats() - Added is_excluded=False to query filter")
    print("   6. export_reviewed_posts_pdf() - Added is_excluded=False to query filter")
    print("   7. export_reviewed_posts_excel() - Added is_excluded=False to query filter")
    print("\nPlease review the changes and test the application!")


if __name__ == '__main__':
    main()
