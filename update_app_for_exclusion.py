"""
Script to update app.py with is_excluded functionality
"""

def update_app_py():
    """Add is_excluded support to app.py"""

    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add is_excluded field to TwitterPost model (after is_favorite)
    if 'is_excluded = db.Column' not in content:
        old_meta = '''    is_favorite = db.Column(db.Boolean, default=False)  # Session-übergreifende Favoriten
    notes = db.Column(db.Text)'''

        new_meta = '''    is_favorite = db.Column(db.Boolean, default=False)  # Session-übergreifende Favoriten
    is_excluded = db.Column(db.Boolean, default=False)  # Aus Statistiken ausschließen
    notes = db.Column(db.Text)'''

        content = content.replace(old_meta, new_meta)
        print("[OK] Added is_excluded field to TwitterPost model")
    else:
        print("[OK] is_excluded field already exists in model")

    # 2. Add is_excluded to to_dict method
    if "'is_excluded': self.is_excluded" not in content:
        old_dict = '''            'is_favorite': self.is_favorite,
            'notes': self.notes,'''

        new_dict = '''            'is_favorite': self.is_favorite,
            'is_excluded': self.is_excluded,
            'notes': self.notes,'''

        content = content.replace(old_dict, new_dict)
        print("[OK] Added is_excluded to to_dict method")
    else:
        print("[OK] is_excluded already in to_dict method")

    # 3. Add is_excluded handling in update_post endpoint
    if "# Ausschluss-Status" not in content:
        old_update = '''    # Favoriten-Status
    if 'is_favorite' in data:
        post.is_favorite = bool(data['is_favorite'])

    # Notizen
    if 'notes' in data:
        post.notes = data['notes']'''

        new_update = '''    # Favoriten-Status
    if 'is_favorite' in data:
        post.is_favorite = bool(data['is_favorite'])

    # Ausschluss-Status (aus Statistiken)
    if 'is_excluded' in data:
        post.is_excluded = bool(data['is_excluded'])

    # Notizen
    if 'notes' in data:
        post.notes = data['notes']'''

        content = content.replace(old_update, new_update)
        print("[OK] Added is_excluded handling in update_post endpoint")
    else:
        print("[OK] is_excluded handling already in update_post endpoint")

    # Write back
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n[OK] Successfully updated app.py")

if __name__ == '__main__':
    print("=" * 60)
    print("Updating app.py with is_excluded functionality")
    print("=" * 60)
    update_app_py()
    print("=" * 60)
