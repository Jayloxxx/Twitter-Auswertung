# Twitter TER Dashboard

Professionelles Dashboard zur Analyse von Twitter Engagement Rate (TER) nach Hirsch 2025.

## Features

- **CSV-Upload**: Importiere deine extrahierten Twitter-Daten direkt ins Dashboard
- **Automatische TER-Berechnung**: Berechnet TER nach der wissenschaftlichen Formel (Hirsch 2025)
- **Manuelle TER-Eingabe**: Füge deine eigenen TER-Berechnungen hinzu
- **Post-Review-System**: Gehe Posts einzeln durch, öffne Twitter-URLs automatisch
- **Deskriptive Statistiken**: Umfassende statistische Auswertung aller Daten
- **Professionelles UI**: Modern gestaltet mit Tailwind CSS
- **SQLite Datenbank**: Alle Daten werden persistent gespeichert

## TER-Berechnung (Hirsch 2025)

```
TER = (weighted_engagement / views) * 100

weighted_engagement = (likes × 1) + (bookmarks × 2) + (replies × 3) + (retweets × 4) + (quotes × 5)
```

## Installation

### 1. Python Virtual Environment erstellen

```bash
python -m venv venv
```

### 2. Virtual Environment aktivieren

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

## Verwendung

### 1. Server starten

```bash
python app.py
```

Der Server startet auf `http://localhost:5000`

### 2. Dashboard öffnen

Öffne deinen Browser und gehe zu: `http://localhost:5000`

### 3. CSV-Datei hochladen

1. Wechsle zum Tab "Upload"
2. Lade deine CSV-Datei hoch (erstellt von deinem Scraper-Skript)
3. Das System importiert automatisch alle Posts und berechnet TER-Scores

### 4. Posts reviewen

1. Wechsle zum Tab "Review Posts"
2. Gehe Posts nacheinander durch
3. Klicke auf "🐦 Öffnen" um den Twitter-Post im Browser zu öffnen
4. Trage deinen manuell berechneten TER-Score ein
5. Füge optional Notizen hinzu
6. Markiere den Post als "reviewed"

### 5. Statistiken anzeigen

1. Wechsle zum Tab "Statistiken"
2. Sieh dir umfassende deskriptive Statistiken an:
   - Durchschnittlicher TER
   - Mittelwert, Median, Standardabweichung
   - Views, Followers, Engagement-Metriken
   - Top 10 Posts

## CSV-Format

Das Dashboard erwartet folgende Spalten in der CSV-Datei:

```
factcheck_url, factcheck_title, factcheck_date, factcheck_rating,
twitter_url, twitter_author, twitter_handle, twitter_followers,
twitter_content, twitter_date,
likes, retweets, replies, bookmarks, quotes, views, TER
```

Diese Struktur wird automatisch von deinem Scraper-Skript erstellt.

## Datenbankstruktur

Die SQLite-Datenbank (`twitter_ter.db`) speichert:

- **twitter_posts**: Alle Twitter-Posts mit vollständigen Metadaten
  - Factcheck-Informationen
  - Twitter-Account-Daten
  - Engagement-Metriken (Likes, Retweets, etc.)
  - TER-Scores (automatisch & manuell)
  - Review-Status und Notizen

## API-Endpoints

### Posts abrufen
```
GET /api/posts?reviewed={true|false|all}&sort={created_at|ter_automatic|views|followers}&order={asc|desc}
```

### Einzelnen Post abrufen
```
GET /api/posts/<id>
```

### Post aktualisieren
```
PUT /api/posts/<id>
Body: { "ter_manual": 5.23, "is_reviewed": true, "notes": "..." }
```

### Post löschen
```
DELETE /api/posts/<id>
```

### Statistiken abrufen
```
GET /api/stats
```

### CSV hochladen
```
POST /api/upload
Form-Data: file=<csv-file>
```

## Technologie-Stack

- **Backend**: Python Flask
- **Datenbank**: SQLite mit SQLAlchemy ORM
- **Frontend**: HTML5 + Tailwind CSS (CDN)
- **JavaScript**: Alpine.js für Interaktivität
- **Charts**: Chart.js für Visualisierungen

## Workflow

1. **Daten extrahieren**: Nutze dein bestehendes Scraper-Skript
2. **CSV hochladen**: Importiere die Daten ins Dashboard
3. **Posts reviewen**: Gehe Posts durch und verifiziere TER-Berechnungen
4. **Statistiken analysieren**: Erhalte umfassende Insights
5. **Export**: Daten bleiben in der SQLite-Datenbank gespeichert

## Tipps

- **Filter nutzen**: Filtere nach "Unreviewed" Posts um effizient zu arbeiten
- **Sortierung**: Sortiere nach TER um interessanteste Posts zuerst zu sehen
- **Notizen**: Füge Kontext-Notizen zu Posts hinzu für spätere Analyse
- **Manuelle TER**: Vergleiche automatische vs. manuelle TER-Berechnungen

## Sicherheitshinweise

- **Production**: Ändere `SECRET_KEY` in `app.py` vor Production-Einsatz
- **Zugriff**: Das Dashboard läuft lokal, aber beachte Firewall-Einstellungen
- **Daten**: Die Datenbank enthält alle importierten Posts (Backup empfohlen)

## Troubleshooting

### Port bereits belegt
Ändere in `app.py` die Zeile:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
auf einen anderen Port, z.B. `port=8080`

### CSV-Import schlägt fehl
Prüfe ob:
- Die CSV-Datei UTF-8 kodiert ist
- Alle Spalten vorhanden sind
- Die `twitter_url` eindeutig ist

### Datenbank zurücksetzen
Lösche die Datei `twitter_ter.db` und starte den Server neu.

## Lizenz

Dieses Projekt dient der wissenschaftlichen Forschung (Masterarbeit).

## Kontakt

Bei Fragen oder Problemen, erstelle ein Issue oder kontaktiere den Entwickler.

---

**Made with ❤️ for Twitter TER Analysis**
