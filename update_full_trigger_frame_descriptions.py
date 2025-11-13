"""
Update PDF with complete/full trigger and frame descriptions
"""

def update_descriptions():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # 1. Replace with FULL trigger descriptions
    old_trigger_data = """                trigger_data = [
                    ['Trigger', 'Intensität', 'Beschreibung'],
                    ['Angst/Bedrohung', str(post.trigger_angst), 'Schutzreflexe, defensive Einstellungen'],
                    ['Wut', str(post.trigger_wut), 'Ärger, Frustration, aggressive Emotionen'],
                    ['Empörung', str(post.trigger_empoerung), 'Moralische Verurteilung, hohe Aktivierung'],
                    ['Ekel', str(post.trigger_ekel), 'Abwertung, Entmenschlichung'],
                    ['Identitätsbezug', str(post.trigger_identitaet), '"Wir vs. Sie"-Dynamik, Polarisierung'],
                    ['Hoffnung/Stolz', str(post.trigger_hoffnung), 'Positive Mobilisierung'],
                ]"""

    new_trigger_data = """                # Full trigger descriptions
                trigger_descriptions = {
                    'angst': 'Dieser Trigger aktiviert Schutzreflexe und fördert defensive Einstellungen. Posts, die Angst auslösen, neigen dazu, Menschen vorsichtiger zu machen und können zu Rückzug oder verstärkter Abwehrhaltung führen.',
                    'wut': 'Wut ist eine stark aktivierende Emotion, die Menschen dazu bringt, gegen wahrgenommene Ungerechtigkeiten zu protestieren. Posts mit Wut-Triggern können zu schneller Verbreitung und emotionalen Reaktionen führen.',
                    'empoerung': 'Empörung kombiniert Wut mit moralischer Überlegenheit. Sie ist besonders wirksam für Mobilisierung, da sie Menschen das Gefühl gibt, auf der "richtigen Seite" zu stehen und gegen moralisches Fehlverhalten zu kämpfen.',
                    'ekel': 'Ekel dient der Abgrenzung und kann zur Entmenschlichung führen. Posts, die Ekel auslösen, schaffen starke emotionale Distanz zu den beschriebenen Personen oder Gruppen.',
                    'identitaet': 'Identitätsbezogene Trigger verstärken die "Wir vs. Sie"-Dynamik und fördern Gruppendenken. Sie sind besonders wirksam bei der Mobilisierung von In-Groups gegen Out-Groups.',
                    'hoffnung': 'Hoffnung und Stolz sind positive Mobilisierungstrigger. Sie motivieren Menschen durch das Versprechen einer besseren Zukunft oder durch die Bestätigung der eigenen Gruppenzugehörigkeit.'
                }

                trigger_data = [
                    ['Trigger', 'Int.', 'Vollständige Beschreibung'],
                    ['Angst/Bedrohung', str(post.trigger_angst), trigger_descriptions['angst']],
                    ['Wut', str(post.trigger_wut), trigger_descriptions['wut']],
                    ['Empörung', str(post.trigger_empoerung), trigger_descriptions['empoerung']],
                    ['Ekel', str(post.trigger_ekel), trigger_descriptions['ekel']],
                    ['Identitätsbezug', str(post.trigger_identitaet), trigger_descriptions['identitaet']],
                    ['Hoffnung/Stolz', str(post.trigger_hoffnung), trigger_descriptions['hoffnung']],
                ]"""

    if old_trigger_data in content:
        content = content.replace(old_trigger_data, new_trigger_data)
        changes += 1
        print("[OK] Updated Trigger descriptions to full version")
    else:
        print("[WARNING] Trigger data pattern not found")

    # Update trigger table column widths for better display
    old_trigger_table = """                trigger_table = Table(trigger_data, colWidths=[5*cm, 2.5*cm, 9*cm])"""
    new_trigger_table = """                trigger_table = Table(trigger_data, colWidths=[4*cm, 1.5*cm, 11*cm])"""

    if old_trigger_table in content:
        content = content.replace(old_trigger_table, new_trigger_table)
        print("[OK] Adjusted trigger table column widths")

    # 2. Replace with FULL frame descriptions
    old_frame_data = """                frame_data = [
                    ['Frame', 'Vorhanden', 'Beschreibung'],
                    ['Opfer-Täter Frame', '✓' if post.frame_opfer_taeter else '✗', 'Schuldzuweisungen, moralische Bewertungen'],
                    ['Bedrohungs-Frame', '✓' if post.frame_bedrohung else '✗', 'Externe Gefahr, "Angriff", "bedroht"'],
                    ['Verschwörungs-Frame', '✓' if post.frame_verschwoerung else '✗', 'Geheime Mächte, "System", "Eliten"'],
                    ['Moral-Frame', '✓' if post.frame_moral else '✗', 'Gut-Böse-Dichotomie'],
                    ['Historischer Frame', '✓' if post.frame_historisch else '✗', 'Bezug auf Geschichte, Tradition'],
                ]"""

    new_frame_data = """                # Full frame descriptions
                frame_descriptions = {
                    'opfer_taeter': 'Dieser Frame strukturiert die Erzählung in klare Opfer- und Täterrollen. Er ermöglicht einfache Schuldzuweisungen und moralische Bewertungen, die komplexe Situationen vereinfachen.',
                    'bedrohung': 'Der Bedrohungs-Frame stellt eine Situation als existenzielle Gefahr dar. Begriffe wie "Angriff", "bedroht" oder "gefährdet" aktivieren Verteidigungsreflexe und rechtfertigen defensive Maßnahmen.',
                    'verschwoerung': 'Verschwörungs-Frames erklären Ereignisse durch geheime Absprachen mächtiger Akteure. Sie verwenden Begriffe wie "Eliten", "System" oder "Deep State" und bieten alternative Erklärungen für komplexe Phänomene.',
                    'moral': 'Der Moral-Frame teilt die Welt in "Gut" und "Böse" ein. Er verleiht politischen Positionen moralische Autorität und macht Kompromisse schwieriger, da sie als moralisches Versagen interpretiert werden können.',
                    'historisch': 'Historische Frames ziehen Parallelen zu vergangenen Ereignissen, um aktuelle Situationen zu deuten. Sie nutzen kollektive Erinnerungen und können sowohl warnend als auch legitimierend wirken.'
                }

                frame_data = [
                    ['Frame', '✓/✗', 'Vollständige Beschreibung'],
                    ['Opfer-Täter Frame', '✓' if post.frame_opfer_taeter else '✗', frame_descriptions['opfer_taeter']],
                    ['Bedrohungs-Frame', '✓' if post.frame_bedrohung else '✗', frame_descriptions['bedrohung']],
                    ['Verschwörungs-Frame', '✓' if post.frame_verschwoerung else '✗', frame_descriptions['verschwoerung']],
                    ['Moral-Frame', '✓' if post.frame_moral else '✗', frame_descriptions['moral']],
                    ['Historischer Frame', '✓' if post.frame_historisch else '✗', frame_descriptions['historisch']],
                ]"""

    if old_frame_data in content:
        content = content.replace(old_frame_data, new_frame_data)
        changes += 1
        print("[OK] Updated Frame descriptions to full version")
    else:
        print("[WARNING] Frame data pattern not found")

    # Update frame table column widths
    old_frame_table = """                frame_table = Table(frame_data, colWidths=[5*cm, 2.5*cm, 9*cm])"""
    new_frame_table = """                frame_table = Table(frame_data, colWidths=[4*cm, 1.5*cm, 11*cm])"""

    if old_frame_table in content:
        content = content.replace(old_frame_table, new_frame_table)
        print("[OK] Adjusted frame table column widths")

    # Write back
    if changes > 0:
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)

    return changes

if __name__ == '__main__':
    print("=" * 60)
    print("Updating to FULL Trigger & Frame Descriptions")
    print("=" * 60)
    changes = update_descriptions()
    print("=" * 60)
    if changes > 0:
        print(f"[SUCCESS] Updated descriptions!")
        print("\nNow using complete, detailed descriptions:")
        print("  - Triggers: Explains psychological mechanisms")
        print("  - Frames: Explains narrative structures")
        print("\nExport a new PDF to see full descriptions.")
    else:
        print("[INFO] No changes needed")
    print("=" * 60)
