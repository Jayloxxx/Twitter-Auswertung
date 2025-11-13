"""
Script to add exclusion toggle buttons to the UI in templates/index.html
"""
import re

def add_exclusion_toggle_to_ui():
    """Add exclusion toggle button to reviewed posts table and trigger/frame tab"""

    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    changes_made = []

    # 1. Add JavaScript function for toggleExcluded (add after toggleFavorite function)
    toggle_favorite_pattern = r'(async toggleFavorite\(postId, isFavorite\) \{[^}]+\})'

    toggle_excluded_function = '''

            // Toggle exclusion status (exclude from statistics)
            async toggleExcluded(postId, isExcluded) {
                try {
                    const response = await fetch(`/api/posts/${postId}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            is_excluded: isExcluded
                        })
                    });

                    if (response.ok) {
                        this.showNotification(
                            isExcluded ? 'Post von Statistiken ausgeschlossen' : 'Post wieder in Statistiken aufgenommen',
                            'success'
                        );
                        await this.loadPosts();
                        await this.loadStats();
                    } else {
                        throw new Error('Failed to update exclusion status');
                    }
                } catch (error) {
                    console.error('Error updating exclusion status:', error);
                    this.showNotification('Fehler beim Aktualisieren des Ausschluss-Status', 'error');
                }
            },'''

    if 'toggleExcluded' not in content:
        # Find toggleFavorite and add after it
        match = re.search(r'(async toggleFavorite\([^{]+\{(?:[^{}]|\{[^{}]*\})*\}),', content, re.DOTALL)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + toggle_excluded_function + content[insert_pos:]
            changes_made.append("Added toggleExcluded JavaScript function")
        else:
            print("[WARNING] Could not find toggleFavorite function to add toggleExcluded after it")
    else:
        changes_made.append("toggleExcluded function already exists")

    # 2. Add exclusion button to Reviewed Posts Table (in Actions column)
    # Look for the Twitter link button in the reviewed posts table
    reviewed_actions_pattern = r'(<a :href="\'https://twitter\.com/i/web/status/\' \+ post\.twitter_url\.split\(\'/status/\'\)\[1\]"[^>]+>.*?</a>)\s*(<button @click="showPostDetails\(post\)" class="p-2 rounded-lg bg-blue-50)'

    exclusion_button_reviewed = r'''\1
                                        <!-- Exclusion Toggle Button -->
                                        <button @click="toggleExcluded(post.id, !post.is_excluded)"
                                                :class="post.is_excluded ? 'bg-red-100 text-red-700 hover:bg-red-200' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                                                class="p-2 rounded-lg transition-colors"
                                                :title="post.is_excluded ? 'Aus Statistiken ausgeschlossen - Klicken zum Einschließen' : 'In Statistiken enthalten - Klicken zum Ausschließen'">
                                            <span x-show="post.is_excluded">🚫</span>
                                            <span x-show="!post.is_excluded">📊</span>
                                        </button>
                                        \2'''

    if '<!-- Exclusion Toggle Button -->' not in content:
        content = re.sub(reviewed_actions_pattern, exclusion_button_reviewed, content)
        changes_made.append("Added exclusion button to Reviewed Posts table")
    else:
        changes_made.append("Exclusion button already exists in Reviewed Posts table")

    # 3. Add exclusion button to Trigger & Frames Tab (in post header)
    # Look for the Twitter link and Preview toggle in trigger tab
    trigger_actions_pattern = r'(<!-- Open Twitter Link -->\s*<a :href="\'https://twitter\.com/i/web/status/\' \+ post\.twitter_url\.split\(\'/status/\'\)\[1\][^>]+>.*?</a>)\s*(<!-- Toggle Preview -->\s*<button @click="post\.showPreview = !post\.showPreview")'

    exclusion_button_trigger = r'''\1
                                    <!-- Exclusion Toggle Button -->
                                    <button @click="toggleExcluded(post.id, !post.is_excluded)"
                                            :class="post.is_excluded ? 'bg-red-100 text-red-700 hover:bg-red-200' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                                            class="p-2 rounded-lg transition-colors text-sm font-medium"
                                            :title="post.is_excluded ? 'Aus Statistiken ausgeschlossen' : 'In Statistiken enthalten'">
                                        <span x-show="post.is_excluded">🚫 Ausgeschlossen</span>
                                        <span x-show="!post.is_excluded">📊 In Statistik</span>
                                    </button>
                                    \2'''

    # Check if already added in trigger tab
    if content.count('<!-- Exclusion Toggle Button -->') < 2:
        content = re.sub(trigger_actions_pattern, exclusion_button_trigger, content)
        changes_made.append("Added exclusion button to Trigger & Frames tab")
    else:
        changes_made.append("Exclusion button already exists in Trigger & Frames tab")

    # Write back
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    return changes_made

if __name__ == '__main__':
    print("=" * 60)
    print("Adding Exclusion Toggle to UI")
    print("=" * 60)

    changes = add_exclusion_toggle_to_ui()

    print("\nChanges made:")
    for change in changes:
        print(f"  - {change}")

    print("\n" + "=" * 60)
    print("UI Update Complete!")
    print("=" * 60)
