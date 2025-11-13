"""
Fix search variable scope - move to main Alpine component
"""

def fix_scope():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # 1. Remove the x-data from search field divs (they should not create isolated scope)
    old_reviewed_search_div = '''<div class="bg-white rounded-lg shadow-md p-4 mb-4" x-data="{ searchReviewedAccount: '' }">'''
    new_reviewed_search_div = '''<div class="bg-white rounded-lg shadow-md p-4 mb-4">'''

    if old_reviewed_search_div in content:
        content = content.replace(old_reviewed_search_div, new_reviewed_search_div)
        changes += 1
        print("[OK] Removed isolated scope from Reviewed Posts search div")

    # For Trigger & Frames
    old_trigger_search_div = '''<div class="mb-4" x-data="{ searchTriggerAccount: '' }">'''
    new_trigger_search_div = '''<div class="mb-4">'''

    if old_trigger_search_div in content:
        content = content.replace(old_trigger_search_div, new_trigger_search_div)
        changes += 1
        print("[OK] Removed isolated scope from Trigger & Frames search div")

    # 2. Add search variables to main Alpine data component
    # Find the main x-data definition
    marker = '''x-data="{
                currentTab: 'dashboard','''

    if marker in content:
        new_data = '''x-data="{
                currentTab: 'dashboard',
                searchReviewedAccount: '',
                searchTriggerAccount: '','''

        content = content.replace(marker, new_data)
        changes += 1
        print("[OK] Added search variables to main Alpine component")

    # Write back
    if changes > 0:
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(content)

    return changes

if __name__ == '__main__':
    print("=" * 60)
    print("Fixing Search Variable Scope")
    print("=" * 60)
    changes = fix_scope()
    print("=" * 60)
    if changes > 0:
        print(f"[SUCCESS] Made {changes} fixes!")
        print("Posts should now be visible again.")
        print("Reload the application.")
    else:
        print("[INFO] No changes needed")
    print("=" * 60)
