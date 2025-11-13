"""
Fix the filter in Reviewed Posts table
"""

def fix_filter():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the Reviewed Posts section
    marker_start = '<!-- Reviewed Posts Tab -->'
    marker_end = '<!-- Summary Statistics -->'

    pos_start = content.find(marker_start)
    pos_end = content.find(marker_end)

    if pos_start == -1 or pos_end == -1:
        print("[ERROR] Could not find markers")
        return False

    section = content[pos_start:pos_end]

    # Replace the template loop
    old_loop = '<template x-for="(post, index) in reviewedPosts" :key="post.id">'
    new_loop = '<template x-for="(post, index) in reviewedPosts.filter(p => !searchReviewedAccount || p.twitter_author?.toLowerCase().includes(searchReviewedAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchReviewedAccount.toLowerCase()))" :key="post.id">'

    if old_loop in section:
        section = section.replace(old_loop, new_loop)
        content = content[:pos_start] + section + content[pos_end:]

        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(content)

        print("[OK] Fixed filter in Reviewed Posts table")
        return True
    else:
        print("[INFO] Loop already updated or not found")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Fixing Reviewed Posts Filter")
    print("=" * 60)
    success = fix_filter()
    print("=" * 60)
    if success:
        print("[SUCCESS] Filter fixed!")
    else:
        print("[INFO] No changes needed")
    print("=" * 60)
