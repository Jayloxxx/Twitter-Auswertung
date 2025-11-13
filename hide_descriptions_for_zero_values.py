"""
Only show descriptions for triggers > 0 and frames that are present
"""

def update_conditional_descriptions():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # 1. Update trigger data to only show description if intensity > 0
    old_trigger_logic = """                # Full trigger descriptions
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

    new_trigger_logic = """                # Full trigger descriptions
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
                    ['Angst/Bedrohung', str(post.trigger_angst), trigger_descriptions['angst'] if post.trigger_angst > 0 else '-'],
                    ['Wut', str(post.trigger_wut), trigger_descriptions['wut'] if post.trigger_wut > 0 else '-'],
                    ['Empörung', str(post.trigger_empoerung), trigger_descriptions['empoerung'] if post.trigger_empoerung > 0 else '-'],
                    ['Ekel', str(post.trigger_ekel), trigger_descriptions['ekel'] if post.trigger_ekel > 0 else '-'],
                    ['Identitätsbezug', str(post.trigger_identitaet), trigger_descriptions['identitaet'] if post.trigger_identitaet > 0 else '-'],
                    ['Hoffnung/Stolz', str(post.trigger_hoffnung), trigger_descriptions['hoffnung'] if post.trigger_hoffnung > 0 else '-'],
                ]"""

    if old_trigger_logic in content:
        content = content.replace(old_trigger_logic, new_trigger_logic)
        changes += 1
        print("[OK] Trigger descriptions now only shown for intensity > 0")
    else:
        print("[WARNING] Trigger logic pattern not found")

    # 2. Update frame data to only show description if frame is present
    old_frame_logic = """                # Full frame descriptions
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

    new_frame_logic = """                # Full frame descriptions
                frame_descriptions = {
                    'opfer_taeter': 'Dieser Frame strukturiert die Erzählung in klare Opfer- und Täterrollen. Er ermöglicht einfache Schuldzuweisungen und moralische Bewertungen, die komplexe Situationen vereinfachen.',
                    'bedrohung': 'Der Bedrohungs-Frame stellt eine Situation als existenzielle Gefahr dar. Begriffe wie "Angriff", "bedroht" oder "gefährdet" aktivieren Verteidigungsreflexe und rechtfertigen defensive Maßnahmen.',
                    'verschwoerung': 'Verschwörungs-Frames erklären Ereignisse durch geheime Absprachen mächtiger Akteure. Sie verwenden Begriffe wie "Eliten", "System" oder "Deep State" und bieten alternative Erklärungen für komplexe Phänomene.',
                    'moral': 'Der Moral-Frame teilt die Welt in "Gut" und "Böse" ein. Er verleiht politischen Positionen moralische Autorität und macht Kompromisse schwieriger, da sie als moralisches Versagen interpretiert werden können.',
                    'historisch': 'Historische Frames ziehen Parallelen zu vergangenen Ereignissen, um aktuelle Situationen zu deuten. Sie nutzen kollektive Erinnerungen und können sowohl warnend als auch legitimierend wirken.'
                }

                frame_data = [
                    ['Frame', '✓/✗', 'Vollständige Beschreibung'],
                    ['Opfer-Täter Frame', '✓' if post.frame_opfer_taeter else '✗', frame_descriptions['opfer_taeter'] if post.frame_opfer_taeter else '-'],
                    ['Bedrohungs-Frame', '✓' if post.frame_bedrohung else '✗', frame_descriptions['bedrohung'] if post.frame_bedrohung else '-'],
                    ['Verschwörungs-Frame', '✓' if post.frame_verschwoerung else '✗', frame_descriptions['verschwoerung'] if post.frame_verschwoerung else '-'],
                    ['Moral-Frame', '✓' if post.frame_moral else '✗', frame_descriptions['moral'] if post.frame_moral else '-'],
                    ['Historischer Frame', '✓' if post.frame_historisch else '✗', frame_descriptions['historisch'] if post.frame_historisch else '-'],
                ]"""

    if old_frame_logic in content:
        content = content.replace(old_frame_logic, new_frame_logic)
        changes += 1
        print("[OK] Frame descriptions now only shown when present")
    else:
        print("[WARNING] Frame logic pattern not found")

    # Write back
    if changes > 0:
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)

    return changes

if __name__ == '__main__':
    print("=" * 60)
    print("Hiding Descriptions for Zero/Absent Values")
    print("=" * 60)
    changes = update_conditional_descriptions()
    print("=" * 60)
    if changes > 0:
        print(f"[SUCCESS] Updated conditional display!")
        print("\nNow:")
        print("  - Trigger intensity = 0 -> shows '-' instead of description")
        print("  - Frame not present -> shows '-' instead of description")
        print("  - Only active triggers/frames show full descriptions")
        print("\nExport a new PDF to see the cleaner output.")
    else:
        print("[INFO] No changes needed")
    print("=" * 60)
