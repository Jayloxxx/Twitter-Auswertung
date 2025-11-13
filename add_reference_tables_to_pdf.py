"""
Add reference tables for triggers and frames at the beginning of PDF export
"""

def add_reference_tables():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # Find where to insert the reference tables (after summary, before post loop)
    old_section = """        story.append(summary_table)
        story.append(Spacer(1, 1*cm))

        # Für jeden Post eine detaillierte Seite"""

    new_section = """        story.append(summary_table)
        story.append(Spacer(1, 1*cm))

        # Referenztabellen für Trigger und Frames
        story.append(Paragraph('Erklärung: Emotionale Trigger', heading_style))
        story.append(Paragraph('Die folgenden Trigger beschreiben emotionale Reaktionen, die durch Posts ausgelöst werden können. Intensität wird auf einer Skala von 0-3 gemessen.', normal_style))
        story.append(Spacer(1, 0.3*cm))

        # Trigger-Referenztabelle
        trigger_ref_descriptions = {
            'angst': 'Dieser Trigger aktiviert Schutzreflexe und fördert defensive Einstellungen. Posts, die Angst auslösen, neigen dazu, Menschen vorsichtiger zu machen und können zu Rückzug oder verstärkter Abwehrhaltung führen.',
            'wut': 'Wut ist eine stark aktivierende Emotion, die Menschen dazu bringt, gegen wahrgenommene Ungerechtigkeiten zu protestieren. Posts mit Wut-Triggern können zu schneller Verbreitung und emotionalen Reaktionen führen.',
            'empoerung': 'Empörung kombiniert Wut mit moralischer Überlegenheit. Sie ist besonders wirksam für Mobilisierung, da sie Menschen das Gefühl gibt, auf der "richtigen Seite" zu stehen und gegen moralisches Fehlverhalten zu kämpfen.',
            'ekel': 'Ekel dient der Abgrenzung und kann zur Entmenschlichung führen. Posts, die Ekel auslösen, schaffen starke emotionale Distanz zu den beschriebenen Personen oder Gruppen.',
            'identitaet': 'Identitätsbezogene Trigger verstärken die "Wir vs. Sie"-Dynamik und fördern Gruppendenken. Sie sind besonders wirksam bei der Mobilisierung von In-Groups gegen Out-Groups.',
            'hoffnung': 'Hoffnung und Stolz sind positive Mobilisierungstrigger. Sie motivieren Menschen durch das Versprechen einer besseren Zukunft oder durch die Bestätigung der eigenen Gruppenzugehörigkeit.'
        }

        trigger_ref_data = [
            ['Trigger', 'Beschreibung'],
            [Paragraph('Angst/Bedrohung', normal_style), Paragraph(trigger_ref_descriptions['angst'], normal_style)],
            [Paragraph('Wut', normal_style), Paragraph(trigger_ref_descriptions['wut'], normal_style)],
            [Paragraph('Empörung', normal_style), Paragraph(trigger_ref_descriptions['empoerung'], normal_style)],
            [Paragraph('Ekel', normal_style), Paragraph(trigger_ref_descriptions['ekel'], normal_style)],
            [Paragraph('Identitätsbezug', normal_style), Paragraph(trigger_ref_descriptions['identitaet'], normal_style)],
            [Paragraph('Hoffnung/Stolz', normal_style), Paragraph(trigger_ref_descriptions['hoffnung'], normal_style)],
        ]

        trigger_ref_table = Table(trigger_ref_data, colWidths=[4*cm, 12.5*cm])
        trigger_ref_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        story.append(trigger_ref_table)
        story.append(Spacer(1, 0.8*cm))

        # Frame-Referenztabelle
        story.append(Paragraph('Erklärung: Narrative Frames', heading_style))
        story.append(Paragraph('Frames sind narrative Strukturen, die bestimmen, wie eine Geschichte erzählt wird. Sie beeinflussen, wie Informationen interpretiert werden.', normal_style))
        story.append(Spacer(1, 0.3*cm))

        frame_ref_descriptions = {
            'opfer_taeter': 'Dieser Frame strukturiert die Erzählung in klare Opfer- und Täterrollen. Er ermöglicht einfache Schuldzuweisungen und moralische Bewertungen, die komplexe Situationen vereinfachen.',
            'bedrohung': 'Der Bedrohungs-Frame stellt eine Situation als existenzielle Gefahr dar. Begriffe wie "Angriff", "bedroht" oder "gefährdet" aktivieren Verteidigungsreflexe und rechtfertigen defensive Maßnahmen.',
            'verschwoerung': 'Verschwörungs-Frames erklären Ereignisse durch geheime Absprachen mächtiger Akteure. Sie verwenden Begriffe wie "Eliten", "System" oder "Deep State" und bieten alternative Erklärungen für komplexe Phänomene.',
            'moral': 'Der Moral-Frame teilt die Welt in "Gut" und "Böse" ein. Er verleiht politischen Positionen moralische Autorität und macht Kompromisse schwieriger, da sie als moralisches Versagen interpretiert werden können.',
            'historisch': 'Historische Frames ziehen Parallelen zu vergangenen Ereignissen, um aktuelle Situationen zu deuten. Sie nutzen kollektive Erinnerungen und können sowohl warnend als auch legitimierend wirken.'
        }

        frame_ref_data = [
            ['Frame', 'Beschreibung'],
            [Paragraph('Opfer-Täter Frame', normal_style), Paragraph(frame_ref_descriptions['opfer_taeter'], normal_style)],
            [Paragraph('Bedrohungs-Frame', normal_style), Paragraph(frame_ref_descriptions['bedrohung'], normal_style)],
            [Paragraph('Verschwörungs-Frame', normal_style), Paragraph(frame_ref_descriptions['verschwoerung'], normal_style)],
            [Paragraph('Moral-Frame', normal_style), Paragraph(frame_ref_descriptions['moral'], normal_style)],
            [Paragraph('Historischer Frame', normal_style), Paragraph(frame_ref_descriptions['historisch'], normal_style)],
        ]

        frame_ref_table = Table(frame_ref_data, colWidths=[4*cm, 12.5*cm])
        frame_ref_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ec4899')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        story.append(frame_ref_table)
        story.append(Spacer(1, 1*cm))

        # Für jeden Post eine detaillierte Seite"""

    if old_section in content:
        content = content.replace(old_section, new_section)
        changes += 1
        print("[OK] Added reference tables for triggers and frames")
    else:
        print("[WARNING] Section not found")

    # Write back
    if changes > 0:
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)

    return changes

if __name__ == '__main__':
    print("=" * 60)
    print("Adding Reference Tables to PDF Export")
    print("=" * 60)
    changes = add_reference_tables()
    print("=" * 60)
    if changes > 0:
        print("[SUCCESS] Reference tables added!")
        print("\nThe PDF will now include:")
        print("  + Overview table of all 6 emotional triggers")
        print("  + Overview table of all 5 narrative frames")
        print("  + Full descriptions for each concept")
        print("  + Explanatory text before each table")
        print("\nExport a new PDF to see the reference section.")
    else:
        print("[INFO] No changes needed")
    print("=" * 60)
