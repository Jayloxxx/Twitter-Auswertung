"""
Konvertiert die Excel-Datei mit Trigger/Frame-Ergebnissen in das richtige CSV-Format für den Import
"""
import pandas as pd
import sys

# Mapping: Excel-Spaltenname -> CSV-Spaltenname
COLUMN_MAPPING = {
    'Twitter URL': 'twitter_url',
    'Angst Score': 'trigger_angst',
    'Wut Score': 'trigger_wut',
    'Empörung Score': 'trigger_empoerung',
    'Ekel Score': 'trigger_ekel',
    'Identität Score': 'trigger_identitaet',
    'Hoffnung/Stolz Score': 'trigger_hoffnung',
    'Opfer-Täter Frame': 'frame_opfer_taeter',
    'Bedrohung Frame': 'frame_bedrohung',
    'Verschwörung Frame': 'frame_verschwoerung',
    'Moral Frame': 'frame_moral',
    'Historisch Frame': 'frame_historisch'
}

def convert_excel_to_csv(excel_path, csv_path):
    """Konvertiert Excel-Datei zu CSV mit korrekten Spaltennamen"""
    print(f"Lese Excel-Datei: {excel_path}")

    # Excel-Datei einlesen
    df = pd.read_excel(excel_path)

    print(f"Gefundene Spalten: {list(df.columns)}")
    print(f"Anzahl Zeilen: {len(df)}")

    # Neues DataFrame mit nur den benötigten Spalten erstellen
    new_df = pd.DataFrame()

    for excel_col, csv_col in COLUMN_MAPPING.items():
        if excel_col in df.columns:
            new_df[csv_col] = df[excel_col]
            print(f"[OK] Spalte gemappt: '{excel_col}' -> '{csv_col}'")
        else:
            print(f"[WARNUNG] Spalte '{excel_col}' nicht gefunden!")
            new_df[csv_col] = 0  # Standardwert

    # Datenbereinigung
    # Frames sollten 0 oder 1 sein
    frame_columns = ['frame_opfer_taeter', 'frame_bedrohung', 'frame_verschwoerung', 'frame_moral', 'frame_historisch']
    for col in frame_columns:
        if col in new_df.columns:
            # Konvertiere zu 0 oder 1 (alles > 0 wird zu 1)
            new_df[col] = new_df[col].fillna(0).astype(float).apply(lambda x: 1 if x > 0 else 0)

    # Trigger sollten 0-5 sein
    trigger_columns = ['trigger_angst', 'trigger_wut', 'trigger_empoerung', 'trigger_ekel', 'trigger_identitaet', 'trigger_hoffnung']
    for col in trigger_columns:
        if col in new_df.columns:
            # Fülle fehlende Werte mit 0 und runde auf ganze Zahlen
            new_df[col] = new_df[col].fillna(0).astype(float).round().astype(int)
            # Begrenze auf 0-5
            new_df[col] = new_df[col].clip(0, 5)

    # twitter_url bereinigen
    if 'twitter_url' in new_df.columns:
        new_df['twitter_url'] = new_df['twitter_url'].fillna('').astype(str).str.strip()

    # Zeilen ohne twitter_url entfernen
    new_df = new_df[new_df['twitter_url'] != '']

    print(f"\n[OK] Konvertierung abgeschlossen!")
    print(f"Anzahl gueltiger Zeilen: {len(new_df)}")
    print(f"\nErste 3 Zeilen:")
    print(new_df.head(3).to_string())

    # Als CSV speichern
    new_df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"\n[OK] CSV gespeichert: {csv_path}")

    return new_df

if __name__ == '__main__':
    # Pfade
    excel_path = r"C:\Users\Jason\Desktop\Masterarbeit\CSV Tabellen\trigger_frame_results_20251112_194157.csv"
    csv_path = r"C:\Users\Jason\Desktop\Masterarbeit\Twitter-Auswertung\trigger_frames_converted.csv"

    try:
        df = convert_excel_to_csv(excel_path, csv_path)
        print("\n" + "="*60)
        print("FERTIG! Du kannst jetzt die Datei importieren:")
        print(f"  {csv_path}")
        print("="*60)
    except Exception as e:
        print(f"\n[FEHLER] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
