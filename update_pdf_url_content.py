"""
Update PDF export: Show full URL and remove post content
"""

def update_pdf_export():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # 1. Change URL display to show full URL (not truncated)
    old_url_line = """                ['Twitter URL:', Paragraph(f'<link href="{post.twitter_url}">{post.twitter_url[:80]}...</link>', small_style) if post.twitter_url else 'N/A'],"""
    new_url_line = """                ['Twitter URL:', Paragraph(f'<link href="{post.twitter_url}">{post.twitter_url}</link>', small_style) if post.twitter_url else 'N/A'],"""

    if old_url_line in content:
        content = content.replace(old_url_line, new_url_line)
        changes += 1
        print("[OK] Changed URL to show full link (not truncated)")
    else:
        print("[INFO] URL line already updated or not found")

    # 2. Remove the "Post-Inhalt" section completely
    old_content_section = """
            # Post-Inhalt
            story.append(Paragraph('Post-Inhalt:', ParagraphStyle('BoldNormal', parent=normal_style, fontName='Helvetica-Bold')))
            story.append(Paragraph(content, normal_style))
            story.append(Spacer(1, 0.5*cm))

            # Engagement-Metriken"""

    new_content_section = """
            # Engagement-Metriken"""

    if old_content_section in content:
        content = content.replace(old_content_section, new_content_section)
        changes += 1
        print("[OK] Removed Post-Inhalt section from PDF")
    else:
        print("[INFO] Post-Inhalt section already removed or not found")

    # 3. Also remove the content truncation code that's no longer needed
    old_truncate = """
            # Twitter Content (gekürzt wenn zu lang)
            content = post.twitter_content or 'Kein Inhalt verfügbar'
            if len(content) > 500:
                content = content[:500] + '...'

            info_data = ["""

    new_truncate = """
            info_data = ["""

    if old_truncate in content:
        content = content.replace(old_truncate, new_truncate)
        changes += 1
        print("[OK] Removed content truncation code")
    else:
        print("[INFO] Content truncation code already removed or not found")

    # Write back
    if changes > 0:
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)

    return changes

if __name__ == '__main__':
    print("=" * 60)
    print("Updating PDF Export: Full URL, No Content")
    print("=" * 60)
    changes = update_pdf_export()
    print("=" * 60)
    if changes > 0:
        print(f"[SUCCESS] Made {changes} updates!")
        print("\nChanges:")
        print("  + Full Twitter URL now visible (not truncated)")
        print("  - Post content removed from PDF")
        print("\nExport a new PDF to see the changes.")
    else:
        print("[INFO] No changes needed")
    print("=" * 60)
