"""
Add search functionality for account names in Reviewed Posts and Trigger & Frames tabs
"""

def add_search_fields():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # 1. Add search field in Reviewed Posts tab (before the table)
    # Find the table header in reviewed posts
    reviewed_marker = '''                    <!-- Reviewed Posts Table -->
                    <div x-show="reviewedPosts.length > 0">
                        <table class="w-full">'''

    if reviewed_marker in content and 'searchReviewedAccount' not in content:
        search_field_reviewed = '''                    <!-- Search Field -->
                    <div class="mb-4 flex items-center space-x-4" x-data="{ searchReviewedAccount: '' }">
                        <div class="flex-1">
                            <label class="block text-sm font-medium text-gray-700 mb-2">🔍 Nach Account-Name suchen</label>
                            <input type="text"
                                   x-model="searchReviewedAccount"
                                   placeholder="Autor oder Handle eingeben..."
                                   class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                        </div>
                        <div class="text-sm text-gray-600 mt-6">
                            <span class="font-bold" x-text="reviewedPosts.filter(p => !searchReviewedAccount || p.twitter_author?.toLowerCase().includes(searchReviewedAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchReviewedAccount.toLowerCase())).length"></span>
                            von <span x-text="reviewedPosts.length"></span> Posts
                        </div>
                    </div>

                    <!-- Reviewed Posts Table -->
                    <div x-show="reviewedPosts.length > 0">
                        <table class="w-full">'''

        content = content.replace(reviewed_marker, search_field_reviewed)
        changes += 1
        print("[OK] Added search field to Reviewed Posts tab")

        # Now update the table to use filtered posts
        # Find the template loop
        old_loop = '''<template x-for="(post, index) in reviewedPosts" :key="post.id">'''
        new_loop = '''<template x-for="(post, index) in reviewedPosts.filter(p => !searchReviewedAccount || p.twitter_author?.toLowerCase().includes(searchReviewedAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchReviewedAccount.toLowerCase()))" :key="post.id">'''

        # Find the specific instance in reviewed posts tab (around line 1636)
        # We need to be careful to only replace in the reviewed section
        pos = content.find('<!-- Reviewed Posts Tab -->')
        if pos != -1:
            end_pos = content.find('<!-- Summary Statistics -->', pos)
            if end_pos != -1:
                section = content[pos:end_pos]
                if old_loop in section:
                    section = section.replace(old_loop, new_loop, 1)  # Only first occurrence in this section
                    content = content[:pos] + section + content[end_pos:]
                    print("[OK] Updated Reviewed Posts table to use filtered data")

    # 2. Add search field in Trigger & Frames tab
    trigger_marker = '''                        <!-- Filter & Stats -->
                        <div class="mb-4 flex justify-between items-center">
                            <div class="text-sm text-gray-600">
                                <span class="font-bold text-gray-900" x-text="reviewedPosts.length"></span> reviewed Posts gefunden
                            </div>
                        </div>'''

    if trigger_marker in content and 'searchTriggerAccount' not in content:
        search_field_trigger = '''                        <!-- Search Field -->
                        <div class="mb-4" x-data="{ searchTriggerAccount: '' }">
                            <label class="block text-sm font-medium text-gray-700 mb-2">🔍 Nach Account-Name suchen</label>
                            <input type="text"
                                   x-model="searchTriggerAccount"
                                   placeholder="Autor oder Handle eingeben..."
                                   class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                            <div class="text-sm text-gray-600 mt-2">
                                <span class="font-bold text-gray-900" x-text="reviewedPosts.filter(p => !searchTriggerAccount || p.twitter_author?.toLowerCase().includes(searchTriggerAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchTriggerAccount.toLowerCase())).length"></span>
                                von <span x-text="reviewedPosts.length"></span> Posts
                            </div>
                        </div>

                        <!-- Filter & Stats -->
                        <div class="mb-4 flex justify-between items-center" style="display:none">
                            <div class="text-sm text-gray-600">
                                <span class="font-bold text-gray-900" x-text="reviewedPosts.length"></span> reviewed Posts gefunden
                            </div>
                        </div>'''

        content = content.replace(trigger_marker, search_field_trigger)
        changes += 1
        print("[OK] Added search field to Trigger & Frames tab")

        # Update the posts loop in Trigger & Frames
        # Find the template in triggers section
        pos = content.find('<!-- Trigger & Frames Tab -->')
        if pos != -1:
            # Find the template loop after this position
            loop_start = content.find('<template x-for="(post, index) in reviewedPosts" :key="post.id">', pos)
            if loop_start != -1:
                # Make sure this is in the triggers section (before next major section)
                next_section = content.find('<!-- Advanced Statistics Tab -->', pos)
                if next_section == -1 or loop_start < next_section:
                    old_trigger_loop = '<template x-for="(post, index) in reviewedPosts" :key="post.id">'
                    new_trigger_loop = '<template x-for="(post, index) in reviewedPosts.filter(p => !searchTriggerAccount || p.twitter_author?.toLowerCase().includes(searchTriggerAccount.toLowerCase()) || p.twitter_handle?.toLowerCase().includes(searchTriggerAccount.toLowerCase()))" :key="post.id">'

                    # Replace only in triggers section
                    section = content[pos:next_section] if next_section != -1 else content[pos:]
                    section = section.replace(old_trigger_loop, new_trigger_loop, 1)
                    content = content[:pos] + section + (content[next_section:] if next_section != -1 else '')
                    print("[OK] Updated Trigger & Frames posts to use filtered data")

    # Write back
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    return changes

if __name__ == '__main__':
    print("=" * 60)
    print("Adding Search Functionality")
    print("=" * 60)
    changes = add_search_fields()
    print("=" * 60)
    if changes > 0:
        print(f"[SUCCESS] Added {changes} search fields!")
        print("Reload the application to use the search.")
    else:
        print("[INFO] Search fields already exist or could not be added")
    print("=" * 60)
