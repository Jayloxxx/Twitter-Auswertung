"""
Add exclusion button to Trigger & Frame tab
"""

def add_button():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace in Trigger & Frames tab
    old_buttons = '''                                            <div class="ml-4 flex space-x-2">
                                                <a :href="post.twitter_url" target="_blank"
                                                   class="px-3 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600 transition-colors">
                                                    🐦 Öffnen
                                                </a>
                                                <button @click="showPreview = !showPreview"
                                                        :class="showPreview ? 'bg-green-500' : 'bg-indigo-500'"
                                                        class="px-3 py-1 text-white text-xs rounded hover:opacity-90 transition-colors">
                                                    <span x-text="showPreview ? '🔼 Vorschau' : '👁️ Vorschau'"></span>
                                                </button>
                                            </div>'''

    new_buttons = '''                                            <div class="ml-4 flex space-x-2">
                                                <a :href="post.twitter_url" target="_blank"
                                                   class="px-3 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600 transition-colors">
                                                    🐦 Öffnen
                                                </a>
                                                <!-- Exclusion Toggle Button -->
                                                <button @click="toggleExcluded(post.id, !post.is_excluded)"
                                                        :class="post.is_excluded ? 'bg-red-100 text-red-700 hover:bg-red-200' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                                                        class="px-3 py-1 text-xs rounded transition-colors font-medium"
                                                        :title="post.is_excluded ? 'Aus Statistiken ausgeschlossen' : 'In Statistiken enthalten'">
                                                    <span x-show="post.is_excluded">🚫 Ausgeschlossen</span>
                                                    <span x-show="!post.is_excluded">📊 In Statistik</span>
                                                </button>
                                                <button @click="showPreview = !showPreview"
                                                        :class="showPreview ? 'bg-green-500' : 'bg-indigo-500'"
                                                        class="px-3 py-1 text-white text-xs rounded hover:opacity-90 transition-colors">
                                                    <span x-text="showPreview ? '🔼 Vorschau' : '👁️ Vorschau'"></span>
                                                </button>
                                            </div>'''

    if old_buttons in content:
        content = content.replace(old_buttons, new_buttons)
        print("[OK] Added exclusion button to Trigger & Frame tab")

        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    else:
        print("[WARNING] Could not find location for button")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Adding Exclusion Button to Trigger & Frame Tab")
    print("=" * 60)
    success = add_button()
    print("=" * 60)
    if success:
        print("[SUCCESS] Button added!")
        print("Reload the application to see the button.")
    else:
        print("[ERROR] Button could not be added")
    print("=" * 60)
