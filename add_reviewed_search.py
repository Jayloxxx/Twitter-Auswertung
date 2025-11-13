"""
Add search field to Reviewed Posts tab
"""

def add_reviewed_search():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add search field before the table in Reviewed Posts tab
    old_section = '''                <!-- Reviewed Posts Table -->
                <div class="bg-white rounded-lg shadow-md overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full">'''

    new_section = '''                <!-- Search Field for Reviewed Posts -->
                <div class="bg-white rounded-lg shadow-md p-4 mb-4" x-data="{ searchReviewedAccount: '' }">
                    <label class="block text-sm font-medium text-gray-700 mb-2">🔍 Nach Account-Name suchen</label>
                    <input type="text"
                           x-model="searchReviewedAccount"
                           placeholder="Autor oder Handle eingeben..."
                           class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                    <div class="text-sm text-gray-600 mt-2">
                        <span class="font-bold text-gray-900" x-text="reviewedPosts.filter(p => !searchReviewedAccount || p.twitter_author?.toLowerCase().includes(searchReviewedAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchReviewedAccount.toLowerCase())).length"></span>
                        von <span x-text="reviewedPosts.length"></span> Posts
                    </div>
                </div>

                <!-- Reviewed Posts Table -->
                <div class="bg-white rounded-lg shadow-md overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full">'''

    if old_section in content and 'searchReviewedAccount' not in content:
        content = content.replace(old_section, new_section)
        print("[OK] Added search field to Reviewed Posts tab")

        # Update the table loop to use filtered data
        # Find in Reviewed Posts section specifically
        pos = content.find('<!-- Reviewed Posts Tab -->')
        end_pos = content.find('<!-- Summary Statistics -->', pos)

        if pos != -1 and end_pos != -1:
            section = content[pos:end_pos]

            old_loop = '<template x-for="(post, index) in reviewedPosts" :key="post.id">'
            new_loop = '<template x-for="(post, index) in reviewedPosts.filter(p => !searchReviewedAccount || p.twitter_author?.toLowerCase().includes(searchReviewedAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchReviewedAccount.toLowerCase()))" :key="post.id">'

            if old_loop in section:
                section = section.replace(old_loop, new_loop, 1)
                content = content[:pos] + section + content[end_pos:]
                print("[OK] Updated Reviewed Posts table to use filtered data")

        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    else:
        print("[INFO] Search field already exists or marker not found")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Adding Search to Reviewed Posts Tab")
    print("=" * 60)
    success = add_reviewed_search()
    print("=" * 60)
    if success:
        print("[SUCCESS] Search field added!")
        print("Reload the application to use the search.")
    else:
        print("[INFO] No changes made")
    print("=" * 60)
