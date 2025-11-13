"""
Add exclusion toggle buttons to the UI - FINAL VERSION
"""

def add_buttons():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # 1. Add button in Reviewed Posts table (Actions column)
    if '<!-- Exclusion Toggle Button -->' not in content:
        old_actions = '''                                                <button @click="openTwitterUrl(post.twitter_url)"
                                                        class="bg-twitter text-white p-2 rounded-lg hover:bg-blue-600 transition-colors"
                                                        title="Post öffnen">
                                                    🐦
                                                </button>
                                                <button @click="viewPostDetails(post)"'''

        new_actions = '''                                                <button @click="openTwitterUrl(post.twitter_url)"
                                                        class="bg-twitter text-white p-2 rounded-lg hover:bg-blue-600 transition-colors"
                                                        title="Post öffnen">
                                                    🐦
                                                </button>
                                                <!-- Exclusion Toggle Button -->
                                                <button @click="toggleExcluded(post.id, !post.is_excluded)"
                                                        :class="post.is_excluded ? 'bg-red-100 text-red-700 hover:bg-red-200' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                                                        class="p-2 rounded-lg transition-colors"
                                                        :title="post.is_excluded ? 'Aus Statistiken ausgeschlossen' : 'In Statistiken enthalten'">
                                                    <span x-show="post.is_excluded">🚫</span>
                                                    <span x-show="!post.is_excluded">📊</span>
                                                </button>
                                                <button @click="viewPostDetails(post)"'''

        if old_actions in content:
            content = content.replace(old_actions, new_actions)
            changes += 1
            print("[OK] Added exclusion button to Reviewed Posts table")
        else:
            print("[WARNING] Could not find location for Reviewed Posts button")

    # 2. Add button in Trigger & Frames tab
    # Find the Twitter link button in trigger tab
    trigger_marker = '''<!-- Open Twitter Link -->
                                    <a :href="'https://twitter.com/i/web/status/' + post.twitter_url.split('/status/')[1]"'''

    if trigger_marker in content and content.count('<!-- Exclusion Toggle Button -->') < 2:
        # Find the position after the Twitter link
        pos = content.find(trigger_marker)
        if pos != -1:
            # Find the end of the </a> tag
            end_pos = content.find('</a>', pos)
            if end_pos != -1:
                # Find the next element start
                next_elem_pos = content.find('<!-- Toggle Preview -->', end_pos)
                if next_elem_pos != -1:
                    # Insert button before Toggle Preview
                    exclusion_button = '''
                                    <!-- Exclusion Toggle Button -->
                                    <button @click="toggleExcluded(post.id, !post.is_excluded)"
                                            :class="post.is_excluded ? 'bg-red-100 text-red-700 hover:bg-red-200' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                                            class="px-3 py-2 rounded-lg transition-colors text-sm font-medium"
                                            :title="post.is_excluded ? 'Aus Statistiken ausgeschlossen' : 'In Statistiken enthalten'">
                                        <span x-show="post.is_excluded">🚫 Ausgeschlossen</span>
                                        <span x-show="!post.is_excluded">📊 In Statistik</span>
                                    </button>
                                    '''
                    content = content[:next_elem_pos] + exclusion_button + content[next_elem_pos:]
                    changes += 1
                    print("[OK] Added exclusion button to Trigger & Frames tab")

    # Write back
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n[OK] Added {changes} exclusion buttons")
    return changes

if __name__ == '__main__':
    print("=" * 60)
    print("Adding Exclusion Buttons to UI")
    print("=" * 60)
    changes = add_buttons()
    print("=" * 60)
    if changes > 0:
        print(f"[SUCCESS] {changes} buttons added!")
        print("Reload the application to see the buttons.")
    else:
        print("[INFO] Buttons already exist or could not be added")
    print("=" * 60)
