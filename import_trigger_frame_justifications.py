"""
Import trigger and frame justifications from Excel and update database
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
from app import db, TwitterPost, app
from sqlalchemy import text

def normalize_url(url):
    """Normalize URL for comparison"""
    if not url:
        return ""
    url = url.lower().strip()
    # Replace x.com with twitter.com
    url = url.replace('x.com', 'twitter.com')
    # Remove trailing slashes
    url = url.rstrip('/')
    # Remove web.archive.org prefix if present
    if 'web.archive.org' in url:
        parts = url.split('https://twitter.com/')
        if len(parts) > 1:
            url = 'https://twitter.com/' + parts[-1]
    return url

def import_justifications():
    """Import justifications from Excel file"""

    # Read Excel file
    excel_path = r'C:\Users\Jason\Downloads\trigger_frame_results_20251112_194157.xlsx'
    print(f"Reading Excel file: {excel_path}")
    df = pd.read_excel(excel_path)
    print(f"Found {len(df)} posts in Excel\n")

    # Create URL mapping for Excel data
    excel_data = {}
    for _, row in df.iterrows():
        url = normalize_url(row['Twitter URL'])
        if url:
            excel_data[url] = {
                'angst_justification': row.get('Angst - Detaillierte Begründung', ''),
                'wut_justification': row.get('Wut - Detaillierte Begründung', ''),
                'empoerung_justification': row.get('Empörung - Detaillierte Begründung', ''),
                'ekel_justification': row.get('Ekel - Detaillierte Begründung', ''),
                'identitaet_justification': row.get('Identität - Detaillierte Begründung', ''),
                'hoffnung_justification': row.get('Hoffnung/Stolz - Detaillierte Begründung', ''),
                'frame_opfer_taeter_justification': row.get('Opfer-Täter - Detaillierte Begründung', ''),
                'frame_bedrohung_justification': row.get('Bedrohung - Detaillierte Begründung', ''),
                'frame_verschwoerung_justification': row.get('Verschwörung - Detaillierte Begründung', ''),
                'frame_moral_justification': row.get('Moral - Detaillierte Begründung', ''),
                'frame_historisch_justification': row.get('Historisch - Detaillierte Begründung', ''),
            }

    print(f"Prepared {len(excel_data)} URL mappings from Excel\n")

    # Update database
    with app.app_context():
        # Get all posts from database
        posts = TwitterPost.query.all()
        print(f"Found {len(posts)} posts in database\n")

        matched = 0
        not_matched = 0

        for post in posts:
            post_url = normalize_url(post.twitter_url)

            if post_url in excel_data:
                # Update justifications
                excel_row = excel_data[post_url]

                post.trigger_angst_begruendung = excel_row['angst_justification']
                post.trigger_wut_begruendung = excel_row['wut_justification']
                post.trigger_empoerung_begruendung = excel_row['empoerung_justification']
                post.trigger_ekel_begruendung = excel_row['ekel_justification']
                post.trigger_identitaet_begruendung = excel_row['identitaet_justification']
                post.trigger_hoffnung_begruendung = excel_row['hoffnung_justification']

                post.frame_opfer_taeter_begruendung = excel_row['frame_opfer_taeter_justification']
                post.frame_bedrohung_begruendung = excel_row['frame_bedrohung_justification']
                post.frame_verschwoerung_begruendung = excel_row['frame_verschwoerung_justification']
                post.frame_moral_begruendung = excel_row['frame_moral_justification']
                post.frame_historisch_begruendung = excel_row['frame_historisch_justification']

                matched += 1
                print(f"[OK] Matched: {post.twitter_author} - {post.twitter_handle}")
            else:
                not_matched += 1
                print(f"[SKIP] Not found in Excel: {post.twitter_author} - {post_url}")

        # Commit changes
        db.session.commit()

        print("\n" + "=" * 60)
        print(f"[SUCCESS] Import completed!")
        print(f"  Matched and updated: {matched}")
        print(f"  Not matched: {not_matched}")
        print("=" * 60)

if __name__ == '__main__':
    print("=" * 60)
    print("Importing Trigger & Frame Justifications from Excel")
    print("=" * 60)
    import_justifications()
