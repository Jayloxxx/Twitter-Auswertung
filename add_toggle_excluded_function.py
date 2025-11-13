"""
Add the toggleExcluded JavaScript function to templates/index.html
"""

def add_function():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already added
    if 'async toggleExcluded' in content:
        print("[OK] toggleExcluded function already exists")
        return

    # Find the location after toggleFavorite
    marker = '                },\n\n                async loadArchivedPosts() {'

    if marker not in content:
        print("[ERROR] Could not find insertion point")
        return

    new_function = '''                },

                async toggleExcluded(postId, isExcluded) {
                    try {
                        const response = await fetch(`/api/posts/${postId}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ is_excluded: isExcluded })
                        });

                        if (response.ok) {
                            // Reload posts and statistics
                            await this.loadPosts(true);
                            await this.loadStats();
                            await this.loadStatistics();
                            this.showNotification(
                                isExcluded ? 'Post von Statistiken ausgeschlossen' : 'Post wieder in Statistiken aufgenommen',
                                'success'
                            );
                        }
                    } catch (error) {
                        console.error('Error toggling exclusion:', error);
                        this.showNotification('Fehler beim Aendern des Ausschluss-Status', 'error');
                    }
                },

                async loadArchivedPosts() {'''

    content = content.replace(marker, new_function)

    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("[OK] Added toggleExcluded function")

if __name__ == '__main__':
    add_function()
