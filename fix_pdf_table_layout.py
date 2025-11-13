"""
Fix PDF table layout to show full descriptions without truncation
"""

def fix_table_layout():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # 1. Change trigger table to use full page width and enable text wrapping
    old_trigger_table = """                trigger_table = Table(trigger_data, colWidths=[4*cm, 1.5*cm, 11*cm])
                trigger_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
                ]))"""

    new_trigger_table = """                # Wrap descriptions in Paragraphs for text wrapping
                wrapped_trigger_data = []
                for row in trigger_data:
                    if trigger_data.index(row) == 0:  # Header row
                        wrapped_trigger_data.append(row)
                    else:
                        wrapped_trigger_data.append([
                            Paragraph(str(row[0]), normal_style),
                            Paragraph(str(row[1]), normal_style),
                            Paragraph(str(row[2]), normal_style)
                        ])

                trigger_table = Table(wrapped_trigger_data, colWidths=[4*cm, 1.2*cm, 11.3*cm])
                trigger_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
                ]))"""

    if old_trigger_table in content:
        content = content.replace(old_trigger_table, new_trigger_table)
        changes += 1
        print("[OK] Fixed trigger table layout with text wrapping")
    else:
        print("[WARNING] Trigger table pattern not found")

    # 2. Change frame table to use full page width and enable text wrapping
    old_frame_table = """                frame_table = Table(frame_data, colWidths=[4*cm, 1.5*cm, 11*cm])
                frame_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ec4899')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
                ]))"""

    new_frame_table = """                # Wrap descriptions in Paragraphs for text wrapping
                wrapped_frame_data = []
                for row in frame_data:
                    if frame_data.index(row) == 0:  # Header row
                        wrapped_frame_data.append(row)
                    else:
                        wrapped_frame_data.append([
                            Paragraph(str(row[0]), normal_style),
                            Paragraph(str(row[1]), normal_style),
                            Paragraph(str(row[2]), normal_style)
                        ])

                frame_table = Table(wrapped_frame_data, colWidths=[4*cm, 1.2*cm, 11.3*cm])
                frame_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ec4899')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
                ]))"""

    if old_frame_table in content:
        content = content.replace(old_frame_table, new_frame_table)
        changes += 1
        print("[OK] Fixed frame table layout with text wrapping")
    else:
        print("[WARNING] Frame table pattern not found")

    # Write back
    if changes > 0:
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)

    return changes

if __name__ == '__main__':
    print("=" * 60)
    print("Fixing PDF Table Layout for Full Text Display")
    print("=" * 60)
    changes = fix_table_layout()
    print("=" * 60)
    if changes > 0:
        print(f"[SUCCESS] Fixed table layouts!")
        print("\nChanges:")
        print("  + Text wrapping enabled (uses Paragraph objects)")
        print("  + Column widths optimized (4cm, 1.2cm, 11.3cm)")
        print("  + Vertical alignment set to TOP")
        print("  + Padding increased for better readability")
        print("\nFull descriptions will now be visible in PDF!")
        print("Export a new PDF to see the complete text.")
    else:
        print("[INFO] No changes needed")
    print("=" * 60)
