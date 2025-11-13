"""
Add descriptions for triggers and frames in PDF export
"""

def add_descriptions():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Trigger table to include descriptions
    old_trigger = """                trigger_data = [
                    ['Trigger', 'Intensität'],
                    ['Angst/Bedrohung', str(post.trigger_angst)],
                    ['Wut', str(post.trigger_wut)],
                    ['Empörung', str(post.trigger_empoerung)],
                    ['Ekel', str(post.trigger_ekel)],
                    ['Identitätsbezug', str(post.trigger_identitaet)],
                    ['Hoffnung/Stolz', str(post.trigger_hoffnung)],
                ]

                trigger_table = Table(trigger_data, colWidths=[10*cm, 6.5*cm])"""

    new_trigger = """                trigger_data = [
                    ['Trigger', 'Intensität', 'Beschreibung'],
                    ['Angst/Bedrohung', str(post.trigger_angst), 'Schutzreflexe, defensive Einstellungen'],
                    ['Wut', str(post.trigger_wut), 'Ärger, Frustration, aggressive Emotionen'],
                    ['Empörung', str(post.trigger_empoerung), 'Moralische Verurteilung, hohe Aktivierung'],
                    ['Ekel', str(post.trigger_ekel), 'Abwertung, Entmenschlichung'],
                    ['Identitätsbezug', str(post.trigger_identitaet), '"Wir vs. Sie"-Dynamik, Polarisierung'],
                    ['Hoffnung/Stolz', str(post.trigger_hoffnung), 'Positive Mobilisierung'],
                ]

                trigger_table = Table(trigger_data, colWidths=[5*cm, 2.5*cm, 9*cm])"""

    if old_trigger in content:
        content = content.replace(old_trigger, new_trigger)
        print("[OK] Added descriptions to Trigger table")
    else:
        print("[WARNING] Trigger table pattern not found")

    # 2. Update Frame table to include descriptions
    old_frame = """                frame_data = [
                    ['Frame', 'Vorhanden'],
                    ['Opfer-Täter Frame', '✓' if post.frame_opfer_taeter else '✗'],
                    ['Bedrohungs-Frame', '✓' if post.frame_bedrohung else '✗'],
                    ['Verschwörungs-Frame', '✓' if post.frame_verschwoerung else '✗'],
                    ['Moral-Frame', '✓' if post.frame_moral else '✗'],
                    ['Historischer Frame', '✓' if post.frame_historisch else '✗'],
                ]

                frame_table = Table(frame_data, colWidths=[10*cm, 6.5*cm])"""

    new_frame = """                frame_data = [
                    ['Frame', 'Vorhanden', 'Beschreibung'],
                    ['Opfer-Täter Frame', '✓' if post.frame_opfer_taeter else '✗', 'Schuldzuweisungen, moralische Bewertungen'],
                    ['Bedrohungs-Frame', '✓' if post.frame_bedrohung else '✗', 'Externe Gefahr, "Angriff", "bedroht"'],
                    ['Verschwörungs-Frame', '✓' if post.frame_verschwoerung else '✗', 'Geheime Mächte, "System", "Eliten"'],
                    ['Moral-Frame', '✓' if post.frame_moral else '✗', 'Gut-Böse-Dichotomie'],
                    ['Historischer Frame', '✓' if post.frame_historisch else '✗', 'Bezug auf Geschichte, Tradition'],
                ]

                frame_table = Table(frame_data, colWidths=[5*cm, 2.5*cm, 9*cm])"""

    if old_frame in content:
        content = content.replace(old_frame, new_frame)
        print("[OK] Added descriptions to Frame table")
    else:
        print("[WARNING] Frame table pattern not found")

    # Write back
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    print("=" * 60)
    print("Adding Trigger & Frame Descriptions to PDF Export")
    print("=" * 60)
    add_descriptions()
    print("=" * 60)
    print("[SUCCESS] Descriptions added!")
    print("PDF exports will now show explanations for each trigger and frame.")
    print("=" * 60)
