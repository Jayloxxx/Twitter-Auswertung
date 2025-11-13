"""
Add URL search to both search fields
"""

def add_url_search():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # 1. Update Reviewed Posts search placeholder and filter
    old_reviewed_placeholder = '''                           placeholder="Autor oder Handle eingeben..."'''
    new_reviewed_placeholder = '''                           placeholder="Autor, Handle oder URL eingeben..."'''

    if old_reviewed_placeholder in content:
        content = content.replace(old_reviewed_placeholder, new_reviewed_placeholder)
        changes += 1
        print("[OK] Updated Reviewed Posts search placeholder")

    # Update the filter to include URL
    old_reviewed_filter = '''reviewedPosts.filter(p => !searchReviewedAccount || p.twitter_author?.toLowerCase().includes(searchReviewedAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchReviewedAccount.toLowerCase()))'''
    new_reviewed_filter = '''reviewedPosts.filter(p => !searchReviewedAccount || p.twitter_author?.toLowerCase().includes(searchReviewedAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchReviewedAccount.toLowerCase()) || p.twitter_url?.toLowerCase().includes(searchReviewedAccount.toLowerCase()))'''

    # Count occurrences to replace all in reviewed section
    count = content.count(old_reviewed_filter)
    if count > 0:
        content = content.replace(old_reviewed_filter, new_reviewed_filter)
        changes += 1
        print(f"[OK] Updated Reviewed Posts filter ({count} occurrences)")

    # 2. Update Trigger & Frames search placeholder and filter
    old_trigger_placeholder = '''                                   placeholder="Autor oder Handle eingeben..."'''
    new_trigger_placeholder = '''                                   placeholder="Autor, Handle oder URL eingeben..."'''

    if old_trigger_placeholder in content:
        content = content.replace(old_trigger_placeholder, new_trigger_placeholder)
        changes += 1
        print("[OK] Updated Trigger & Frames search placeholder")

    # Update the filter to include URL
    old_trigger_filter = '''reviewedPosts.filter(p => !searchTriggerAccount || p.twitter_author?.toLowerCase().includes(searchTriggerAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchTriggerAccount.toLowerCase()))'''
    new_trigger_filter = '''reviewedPosts.filter(p => !searchTriggerAccount || p.twitter_author?.toLowerCase().includes(searchTriggerAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchTriggerAccount.toLowerCase()) || p.twitter_url?.toLowerCase().includes(searchTriggerAccount.toLowerCase()))'''

    count = content.count(old_trigger_filter)
    if count > 0:
        content = content.replace(old_trigger_filter, new_trigger_filter)
        changes += 1
        print(f"[OK] Updated Trigger & Frames filter ({count} occurrences)")

    # Write back
    if changes > 0:
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(content)

    return changes

if __name__ == '__main__':
    print("=" * 60)
    print("Adding URL Search Capability")
    print("=" * 60)
    changes = add_url_search()
    print("=" * 60)
    if changes > 0:
        print(f"[SUCCESS] Made {changes} updates!")
        print("Search now includes: Autor, Handle AND URL")
        print("Reload the application to use the enhanced search.")
    else:
        print("[INFO] Already updated or no changes needed")
    print("=" * 60)
