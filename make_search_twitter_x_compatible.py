"""
Make search compatible with both twitter.com and x.com URLs
"""

def make_search_compatible():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # Old filter for Reviewed Posts
    old_reviewed_filter = '''reviewedPosts.filter(p => !searchReviewedAccount || p.twitter_author?.toLowerCase().includes(searchReviewedAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchReviewedAccount.toLowerCase()) || p.twitter_url?.toLowerCase().includes(searchReviewedAccount.toLowerCase()))'''

    # New filter that normalizes twitter.com/x.com
    new_reviewed_filter = '''reviewedPosts.filter(p => {
                                if (!searchReviewedAccount) return true;
                                const search = searchReviewedAccount.toLowerCase();
                                const normalizedSearch = search.replace('x.com', 'twitter.com');
                                const normalizedUrl = p.twitter_url?.toLowerCase().replace('x.com', 'twitter.com') || '';
                                return p.twitter_author?.toLowerCase().includes(search) ||
                                       p.twitter_handle?.toLowerCase().includes(search) ||
                                       normalizedUrl.includes(normalizedSearch);
                            })'''

    if old_reviewed_filter in content:
        content = content.replace(old_reviewed_filter, new_reviewed_filter)
        changes += 1
        print("[OK] Updated Reviewed Posts filter to handle twitter.com/x.com")

    # Old filter for Trigger & Frames
    old_trigger_filter = '''reviewedPosts.filter(p => !searchTriggerAccount || p.twitter_author?.toLowerCase().includes(searchTriggerAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchTriggerAccount.toLowerCase()) || p.twitter_url?.toLowerCase().includes(searchTriggerAccount.toLowerCase()))'''

    # New filter
    new_trigger_filter = '''reviewedPosts.filter(p => {
                                if (!searchTriggerAccount) return true;
                                const search = searchTriggerAccount.toLowerCase();
                                const normalizedSearch = search.replace('x.com', 'twitter.com');
                                const normalizedUrl = p.twitter_url?.toLowerCase().replace('x.com', 'twitter.com') || '';
                                return p.twitter_author?.toLowerCase().includes(search) ||
                                       p.twitter_handle?.toLowerCase().includes(search) ||
                                       normalizedUrl.includes(normalizedSearch);
                            })'''

    if old_trigger_filter in content:
        content = content.replace(old_trigger_filter, new_trigger_filter)
        changes += 1
        print("[OK] Updated Trigger & Frames filter to handle twitter.com/x.com")

    # Write back
    if changes > 0:
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(content)

    return changes

if __name__ == '__main__':
    print("=" * 60)
    print("Making Search Compatible with twitter.com AND x.com")
    print("=" * 60)
    changes = make_search_compatible()
    print("=" * 60)
    if changes > 0:
        print(f"[SUCCESS] Updated {changes} filters!")
        print("\nNow you can search with BOTH:")
        print("  - twitter.com URLs")
        print("  - x.com URLs")
        print("\nBoth will find posts regardless of which domain is stored!")
        print("\nReload the application to use the enhanced search.")
    else:
        print("[INFO] No changes needed")
    print("=" * 60)
