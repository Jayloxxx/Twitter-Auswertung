import sys
import sqlite3
import statistics

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect(r'C:\Users\Jason\Desktop\Masterarbeit\Twitter-Auswertung\instance\twitter_ter.db')
cursor = conn.cursor()

print("=" * 80)
print("ANALYSE: WARUM HAT EMPÖRUNG NIEDRIGE TRIGGER-EFFEKTIVITÄT?")
print("=" * 80)

# Get posts with and without Empörung
cursor.execute('''
    SELECT
        id,
        trigger_empoerung,
        ter_automatic,
        ter_linear,
        trigger_angst,
        trigger_wut,
        trigger_ekel,
        trigger_identitaet,
        trigger_hoffnung
    FROM twitter_posts
    WHERE is_reviewed = 1 AND is_excluded = 0
''')

posts = cursor.fetchall()

posts_with_empoerung = []
posts_without_empoerung = []

for post in posts:
    post_id, empoerung, ter_auto, ter_linear, angst, wut, ekel, identitaet, hoffnung = post

    # Use ter_automatic (TER√) as the primary metric
    ter_value = ter_auto if ter_auto is not None else 0

    post_data = {
        'id': post_id,
        'empoerung': empoerung,
        'ter': ter_value,
        'angst': angst,
        'wut': wut,
        'ekel': ekel,
        'identitaet': identitaet,
        'hoffnung': hoffnung,
        'total_triggers': angst + wut + empoerung + ekel + identitaet + hoffnung
    }

    if empoerung > 0:
        posts_with_empoerung.append(post_data)
    else:
        posts_without_empoerung.append(post_data)

print(f"\n1. GRUNDLEGENDE STATISTIKEN")
print("-" * 80)
print(f"Posts MIT Empörung (>0):     {len(posts_with_empoerung)}")
print(f"Posts OHNE Empörung (=0):    {len(posts_without_empoerung)}")

# Calculate average TER
if posts_with_empoerung:
    avg_ter_with = statistics.mean([p['ter'] for p in posts_with_empoerung])
    print(f"\nDurchschnittlicher TER√ MIT Empörung:    {avg_ter_with:.4f}")

if posts_without_empoerung:
    avg_ter_without = statistics.mean([p['ter'] for p in posts_without_empoerung])
    print(f"Durchschnittlicher TER√ OHNE Empörung:   {avg_ter_without:.4f}")

if posts_with_empoerung and posts_without_empoerung:
    diff = avg_ter_with - avg_ter_without
    print(f"Differenz:                                {diff:.4f}")

# Analyze correlation between Empörung and other triggers
print(f"\n2. EMPÖRUNG UND ANDERE TRIGGER")
print("-" * 80)
print("Bei Posts MIT Empörung - Durchschnittliche andere Trigger-Scores:")

if posts_with_empoerung:
    avg_angst = statistics.mean([p['angst'] for p in posts_with_empoerung])
    avg_wut = statistics.mean([p['wut'] for p in posts_with_empoerung])
    avg_ekel = statistics.mean([p['ekel'] for p in posts_with_empoerung])
    avg_identitaet = statistics.mean([p['identitaet'] for p in posts_with_empoerung])
    avg_hoffnung = statistics.mean([p['hoffnung'] for p in posts_with_empoerung])
    avg_empoerung = statistics.mean([p['empoerung'] for p in posts_with_empoerung])

    print(f"  Angst:      {avg_angst:.2f}")
    print(f"  Wut:        {avg_wut:.2f}")
    print(f"  Empörung:   {avg_empoerung:.2f}")
    print(f"  Ekel:       {avg_ekel:.2f}")
    print(f"  Identität:  {avg_identitaet:.2f}")
    print(f"  Hoffnung:   {avg_hoffnung:.2f}")

print("\nBei Posts OHNE Empörung - Durchschnittliche andere Trigger-Scores:")
if posts_without_empoerung:
    avg_angst_no = statistics.mean([p['angst'] for p in posts_without_empoerung])
    avg_wut_no = statistics.mean([p['wut'] for p in posts_without_empoerung])
    avg_ekel_no = statistics.mean([p['ekel'] for p in posts_without_empoerung])
    avg_identitaet_no = statistics.mean([p['identitaet'] for p in posts_without_empoerung])
    avg_hoffnung_no = statistics.mean([p['hoffnung'] for p in posts_without_empoerung])

    print(f"  Angst:      {avg_angst_no:.2f}")
    print(f"  Wut:        {avg_wut_no:.2f}")
    print(f"  Empörung:   0.00")
    print(f"  Ekel:       {avg_ekel_no:.2f}")
    print(f"  Identität:  {avg_identitaet_no:.2f}")
    print(f"  Hoffnung:   {avg_hoffnung_no:.2f}")

# Analyze Empörung intensity distribution
print(f"\n3. EMPÖRUNG-INTENSITÄT UND TER")
print("-" * 80)

empoerung_by_score = {}
for post in posts_with_empoerung:
    score = post['empoerung']
    if score not in empoerung_by_score:
        empoerung_by_score[score] = []
    empoerung_by_score[score].append(post['ter'])

for score in sorted(empoerung_by_score.keys()):
    ter_values = empoerung_by_score[score]
    avg_ter = statistics.mean(ter_values)
    print(f"Empörung Score {score}: {len(ter_values)} Posts, Durchschn. TER√ = {avg_ter:.4f}")

# Check if posts with only Empörung (and no other triggers) have lower TER
print(f"\n4. EMPÖRUNG ALLEINE vs. EMPÖRUNG + ANDERE TRIGGER")
print("-" * 80)

only_empoerung = [p for p in posts_with_empoerung if p['angst'] == 0 and p['wut'] == 0 and p['ekel'] == 0 and p['identitaet'] == 0 and p['hoffnung'] == 0]
empoerung_with_others = [p for p in posts_with_empoerung if p['angst'] > 0 or p['wut'] > 0 or p['ekel'] > 0 or p['identitaet'] > 0 or p['hoffnung'] > 0]

print(f"Posts mit NUR Empörung (keine anderen Trigger):        {len(only_empoerung)}")
if only_empoerung:
    avg_ter_only = statistics.mean([p['ter'] for p in only_empoerung])
    print(f"  Durchschnittlicher TER√:                              {avg_ter_only:.4f}")

print(f"\nPosts mit Empörung UND anderen Triggern:               {len(empoerung_with_others)}")
if empoerung_with_others:
    avg_ter_combo = statistics.mean([p['ter'] for p in empoerung_with_others])
    print(f"  Durchschnittlicher TER√:                              {avg_ter_combo:.4f}")

# Correlation analysis
print(f"\n5. MÖGLICHE ERKLÄRUNGEN")
print("-" * 80)

# Check if the 2 posts without Empörung have exceptionally high TER
if posts_without_empoerung:
    print(f"\nDie {len(posts_without_empoerung)} Posts OHNE Empörung:")
    for post in posts_without_empoerung:
        print(f"  Post ID {post['id']}: TER√={post['ter']:.4f}, Angst={post['angst']}, Wut={post['wut']}, "
              f"Ekel={post['ekel']}, Identität={post['identitaet']}, Hoffnung={post['hoffnung']}")

    max_ter_without = max([p['ter'] for p in posts_without_empoerung])
    print(f"\n  → Höchster TER√ OHNE Empörung: {max_ter_without:.4f}")

if posts_with_empoerung:
    max_ter_with = max([p['ter'] for p in posts_with_empoerung])
    print(f"  → Höchster TER√ MIT Empörung:  {max_ter_with:.4f}")

# Statistical insight
print(f"\n6. STATISTISCHE ANALYSE")
print("-" * 80)

if posts_without_empoerung and len(posts_without_empoerung) == 2:
    print(f"⚠️  ACHTUNG: Nur {len(posts_without_empoerung)} Posts ohne Empörung!")
    print(f"   Das ist eine sehr kleine Kontrollgruppe für statistische Vergleiche.")
    print(f"   Die 'Trigger-Effektivität' könnte verzerrt sein durch:")
    print(f"   - Kleine Stichprobengröße der Kontrollgruppe")
    print(f"   - Outlier-Effekte (1-2 Posts mit sehr hohem/niedrigem TER)")
    print(f"   - Fehlende statistische Signifikanz")

conn.close()
print("\n" + "=" * 80)
