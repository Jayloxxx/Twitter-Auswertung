"""
Twitter TER Dashboard - Backend
Professionelles Dashboard für Twitter Engagement Rate Analyse
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import csv
import io
import os
from sqlalchemy import func
import statistics

app = Flask(__name__)
CORS(app)

# Konfiguration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitter_ter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

db = SQLAlchemy(app)


# ==================== DATENBANKMODELLE ====================

class AnalysisSession(db.Model):
    """Speichert verschiedene Analysesitzungen/Projekte"""
    __tablename__ = 'analysis_sessions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)  # Nur eine Session kann aktiv sein

    # Relationship zu Posts
    posts = db.relationship('TwitterPost', backref='session', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Konvertiert Model zu Dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'post_count': len(self.posts),
            'reviewed_count': len([p for p in self.posts if p.is_reviewed]),
            'archived_count': len([p for p in self.posts if p.is_archived])
        }


class TwitterPost(db.Model):
    """Speichert alle Twitter-Post-Daten inklusive TER-Scores"""
    __tablename__ = 'twitter_posts'

    id = db.Column(db.Integer, primary_key=True)

    # Session-Zugehörigkeit
    session_id = db.Column(db.Integer, db.ForeignKey('analysis_sessions.id'), nullable=False)

    # Factcheck-Daten
    factcheck_url = db.Column(db.String(500))
    factcheck_title = db.Column(db.Text)
    factcheck_date = db.Column(db.String(100))
    factcheck_rating = db.Column(db.String(100))

    # Twitter-Daten
    twitter_url = db.Column(db.String(500), nullable=False)  # Nicht mehr unique, da in verschiedenen Sessions erlaubt
    twitter_author = db.Column(db.String(200))
    twitter_handle = db.Column(db.String(100))
    twitter_followers = db.Column(db.Integer, default=0)
    twitter_content = db.Column(db.Text)
    twitter_date = db.Column(db.String(100))

    # Engagement-Metriken (Automatisch aus CSV)
    likes = db.Column(db.Integer, default=0)
    retweets = db.Column(db.Integer, default=0)
    replies = db.Column(db.Integer, default=0)
    bookmarks = db.Column(db.Integer, default=0)
    quotes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)

    # Engagement-Metriken (Manuell eingegeben)
    likes_manual = db.Column(db.Integer, nullable=True)
    retweets_manual = db.Column(db.Integer, nullable=True)
    replies_manual = db.Column(db.Integer, nullable=True)
    bookmarks_manual = db.Column(db.Integer, nullable=True)
    quotes_manual = db.Column(db.Integer, nullable=True)
    views_manual = db.Column(db.Integer, nullable=True)

    # TER-Scores
    ter_automatic = db.Column(db.Float, default=0.0)  # TER√ (neue Formel)
    ter_linear = db.Column(db.Float, default=0.0)  # TER linear (alte Formel)
    ter_manual = db.Column(db.Float, nullable=True)    # Manuell eingegeben
    weighted_engagement = db.Column(db.Integer, default=0)
    total_interactions = db.Column(db.Integer, default=0)
    engagement_level = db.Column(db.String(100))  # z.B. "Hohes Engagement"
    engagement_level_code = db.Column(db.String(20))  # z.B. "high"

    # Trigger (Intensität 0-5)
    trigger_angst = db.Column(db.Integer, default=0)
    trigger_wut = db.Column(db.Integer, default=0)
    trigger_ekel = db.Column(db.Integer, default=0)
    trigger_identitaet = db.Column(db.Integer, default=0)
    trigger_hoffnung = db.Column(db.Integer, default=0)

    # Frames (Binär 0-1)
    frame_opfer_taeter = db.Column(db.Integer, default=0)
    frame_bedrohung = db.Column(db.Integer, default=0)
    frame_verschwoerung = db.Column(db.Integer, default=0)
    frame_moral = db.Column(db.Integer, default=0)
    frame_historisch = db.Column(db.Integer, default=0)

    # Metadaten
    is_reviewed = db.Column(db.Boolean, default=False)
    is_archived = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Konvertiert Model zu Dictionary"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'factcheck_url': self.factcheck_url,
            'factcheck_title': self.factcheck_title,
            'factcheck_date': self.factcheck_date,
            'factcheck_rating': self.factcheck_rating,
            'twitter_url': self.twitter_url,
            'twitter_author': self.twitter_author,
            'twitter_handle': self.twitter_handle,
            'twitter_followers': self.twitter_followers,
            'twitter_content': self.twitter_content,
            'twitter_date': self.twitter_date,
            'likes': self.likes,
            'retweets': self.retweets,
            'replies': self.replies,
            'bookmarks': self.bookmarks,
            'quotes': self.quotes,
            'views': self.views,
            'likes_manual': self.likes_manual,
            'retweets_manual': self.retweets_manual,
            'replies_manual': self.replies_manual,
            'bookmarks_manual': self.bookmarks_manual,
            'quotes_manual': self.quotes_manual,
            'views_manual': self.views_manual,
            'ter_automatic': self.ter_automatic,
            'ter_linear': self.ter_linear,
            'ter_manual': self.ter_manual,
            'weighted_engagement': self.weighted_engagement,
            'total_interactions': self.total_interactions,
            'engagement_level': self.engagement_level,
            'engagement_level_code': self.engagement_level_code,
            'trigger_angst': self.trigger_angst,
            'trigger_wut': self.trigger_wut,
            'trigger_ekel': self.trigger_ekel,
            'trigger_identitaet': self.trigger_identitaet,
            'trigger_hoffnung': self.trigger_hoffnung,
            'frame_opfer_taeter': self.frame_opfer_taeter,
            'frame_bedrohung': self.frame_bedrohung,
            'frame_verschwoerung': self.frame_verschwoerung,
            'frame_moral': self.frame_moral,
            'frame_historisch': self.frame_historisch,
            'is_reviewed': self.is_reviewed,
            'is_archived': self.is_archived,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# ==================== TER BERECHNUNG ====================

class TERCalculator:
    """Twitter Engagement Rate (TER) Berechnung nach Hirsch 2025"""

    WEIGHTS = {
        'like': 1,
        'bookmark': 2,
        'reply': 3,
        'retweet': 4,
        'quote': 5
    }

    @classmethod
    def calculate(cls, likes, bookmarks, replies, retweets, quotes, views):
        """
        Berechnet TER mit zwei Methoden:
        - TER√ (neu): weighted_engagement / √views (Wurzel-Normalisierung)
        - TER (linear alt): (weighted_engagement / views) * 100
        """
        import math

        weighted_engagement = (
            (likes * cls.WEIGHTS['like']) +
            (bookmarks * cls.WEIGHTS['bookmark']) +
            (replies * cls.WEIGHTS['reply']) +
            (retweets * cls.WEIGHTS['retweet']) +
            (quotes * cls.WEIGHTS['quote'])
        )

        # Neue TER√ Formel (Hirsch 2025)
        if views > 0:
            ter_sqrt = weighted_engagement / math.sqrt(views)
            ter_linear = (weighted_engagement / views) * 100
        else:
            ter_sqrt = 0
            ter_linear = 0

        total_interactions = likes + bookmarks + replies + retweets + quotes

        # Engagement Level Klassifizierung für TER√
        engagement_level = cls.get_engagement_level(ter_sqrt)

        return {
            'ter': round(ter_sqrt, 2),  # Hauptwert ist jetzt TER√
            'ter_sqrt': round(ter_sqrt, 2),
            'ter_linear': round(ter_linear, 2),
            'weighted_engagement': weighted_engagement,
            'total_interactions': total_interactions,
            'engagement_level': engagement_level['label'],
            'engagement_level_code': engagement_level['code']
        }

    @classmethod
    def get_engagement_level(cls, ter_sqrt):
        """
        Klassifiziert TER√-Werte nach psychologischer Intensität
        """
        if ter_sqrt < 5:
            return {
                'code': 'low',
                'label': 'Niedriges Engagement (passive Rezeption)',
                'color': 'blue',
                'description': 'Passive Rezeption, kaum Aktivierung'
            }
        elif ter_sqrt < 10:
            return {
                'code': 'medium',
                'label': 'Mittleres Engagement (moderate Aktivierung)',
                'color': 'green',
                'description': 'Moderate Aufmerksamkeit, normale Aktivierung'
            }
        elif ter_sqrt < 15:
            return {
                'code': 'high',
                'label': 'Hohes Engagement (starke emotionale Involvierung)',
                'color': 'orange',
                'description': 'Starke emotionale Beteiligung'
            }
        else:
            return {
                'code': 'very_high',
                'label': 'Sehr hohes Engagement (virale Aktivierung)',
                'color': 'red',
                'description': 'Virale Dynamik, maximale Involvierung'
            }


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Dashboard Hauptseite"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_csv():
    """CSV-Datei hochladen und in Datenbank importieren"""
    if 'file' not in request.files:
        return jsonify({'error': 'Keine Datei hochgeladen'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Keine Datei ausgewählt'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Nur CSV-Dateien erlaubt'}), 400

    try:
        # Aktive Session holen
        active_session = AnalysisSession.query.filter_by(is_active=True).first()
        if not active_session:
            return jsonify({'error': 'Keine aktive Session. Bitte erstelle zuerst eine Session.'}), 400

        # Alle Posts der aktiven Session löschen vor dem Import
        old_posts_count = TwitterPost.query.filter_by(session_id=active_session.id).count()
        TwitterPost.query.filter_by(session_id=active_session.id).delete()
        db.session.commit()

        # CSV-Datei lesen
        stream = io.StringIO(file.stream.read().decode('utf-8'), newline=None)
        csv_reader = csv.DictReader(stream)

        imported_count = 0
        skipped_count = 0

        for row in csv_reader:
            twitter_url = row.get('twitter_url', '').strip()

            if not twitter_url:
                skipped_count += 1
                continue

            # TER berechnen
            ter_data = TERCalculator.calculate(
                likes=int(row.get('likes', 0) or 0),
                bookmarks=int(row.get('bookmarks', 0) or 0),
                replies=int(row.get('replies', 0) or 0),
                retweets=int(row.get('retweets', 0) or 0),
                quotes=int(row.get('quotes', 0) or 0),
                views=int(row.get('views', 0) or 0)
            )

            # Neuen Post erstellen (alte wurden bereits gelöscht)
            post = TwitterPost(
                session_id=active_session.id,
                factcheck_url=row.get('factcheck_url', ''),
                factcheck_title=row.get('factcheck_title', ''),
                factcheck_date=row.get('factcheck_date', ''),
                factcheck_rating=row.get('factcheck_rating', ''),
                twitter_url=twitter_url,
                twitter_author=row.get('twitter_author', ''),
                twitter_handle=row.get('twitter_handle', ''),
                twitter_followers=int(row.get('twitter_followers', 0) or 0),
                twitter_content=row.get('twitter_content', ''),
                twitter_date=row.get('twitter_date', ''),
                likes=int(row.get('likes', 0) or 0),
                retweets=int(row.get('retweets', 0) or 0),
                replies=int(row.get('replies', 0) or 0),
                bookmarks=int(row.get('bookmarks', 0) or 0),
                quotes=int(row.get('quotes', 0) or 0),
                views=int(row.get('views', 0) or 0),
                ter_automatic=ter_data['ter_sqrt'],
                ter_linear=ter_data['ter_linear'],
                weighted_engagement=ter_data['weighted_engagement'],
                total_interactions=ter_data['total_interactions'],
                engagement_level=ter_data['engagement_level'],
                engagement_level_code=ter_data['engagement_level_code']
            )
            db.session.add(post)
            imported_count += 1

        db.session.commit()

        # Session aktualisieren
        active_session.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Import erfolgreich in Session "{active_session.name}"! {old_posts_count} alte Posts gelöscht, {imported_count} neue Posts importiert.',
            'session_name': active_session.name,
            'deleted': old_posts_count,
            'imported': imported_count,
            'skipped': skipped_count,
            'total': imported_count
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Import fehlgeschlagen: {str(e)}'}), 500


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Alle Posts abrufen mit Filteroptionen (OHNE archivierte Posts)"""
    # Aktive Session holen
    active_session = AnalysisSession.query.filter_by(is_active=True).first()
    if not active_session:
        return jsonify({'posts': [], 'total': 0, 'message': 'Keine aktive Session'})

    # Filter-Parameter
    reviewed = request.args.get('reviewed', None)
    sort_by = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')

    # WICHTIG: Nur Posts der aktiven Session und archivierte Posts ausschließen
    query = TwitterPost.query.filter_by(session_id=active_session.id, is_archived=False)

    # Filter anwenden
    if reviewed is not None:
        is_reviewed = reviewed.lower() == 'true'
        query = query.filter_by(is_reviewed=is_reviewed, is_archived=False)

    # Sortierung
    if sort_by == 'ter_automatic':
        query = query.order_by(TwitterPost.ter_automatic.desc() if order == 'desc' else TwitterPost.ter_automatic.asc())
    elif sort_by == 'ter_manual':
        query = query.order_by(TwitterPost.ter_manual.desc() if order == 'desc' else TwitterPost.ter_manual.asc())
    elif sort_by == 'views':
        query = query.order_by(TwitterPost.views.desc() if order == 'desc' else TwitterPost.views.asc())
    elif sort_by == 'followers':
        query = query.order_by(TwitterPost.twitter_followers.desc() if order == 'desc' else TwitterPost.twitter_followers.asc())
    else:
        query = query.order_by(TwitterPost.created_at.desc() if order == 'desc' else TwitterPost.created_at.asc())

    posts = query.all()

    return jsonify({
        'posts': [post.to_dict() for post in posts],
        'total': len(posts)
    })


@app.route('/api/posts/archived', methods=['GET'])
def get_archived_posts():
    """Alle archivierten Posts abrufen"""
    sort_by = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')

    # NUR archivierte Posts
    query = TwitterPost.query.filter_by(is_archived=True)

    # Sortierung
    if sort_by == 'ter_automatic':
        query = query.order_by(TwitterPost.ter_automatic.desc() if order == 'desc' else TwitterPost.ter_automatic.asc())
    elif sort_by == 'ter_manual':
        query = query.order_by(TwitterPost.ter_manual.desc() if order == 'desc' else TwitterPost.ter_manual.asc())
    elif sort_by == 'views':
        query = query.order_by(TwitterPost.views.desc() if order == 'desc' else TwitterPost.views.asc())
    elif sort_by == 'followers':
        query = query.order_by(TwitterPost.twitter_followers.desc() if order == 'desc' else TwitterPost.twitter_followers.asc())
    else:
        query = query.order_by(TwitterPost.created_at.desc() if order == 'desc' else TwitterPost.created_at.asc())

    posts = query.all()

    return jsonify({
        'posts': [post.to_dict() for post in posts],
        'total': len(posts)
    })


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Einzelnen Post abrufen"""
    post = TwitterPost.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Post aktualisieren (z.B. manuellen TER-Score setzen)"""
    post = TwitterPost.query.get_or_404(post_id)
    data = request.json

    # Manuellen TER-Score aktualisieren
    if 'ter_manual' in data:
        ter_manual = data['ter_manual']
        if ter_manual is not None:
            post.ter_manual = float(ter_manual)
        else:
            post.ter_manual = None

    # Manuelle Engagement-Metriken aktualisieren
    if 'views_manual' in data:
        post.views_manual = int(data['views_manual']) if data['views_manual'] is not None else None
    if 'likes_manual' in data:
        post.likes_manual = int(data['likes_manual']) if data['likes_manual'] is not None else None
    if 'bookmarks_manual' in data:
        post.bookmarks_manual = int(data['bookmarks_manual']) if data['bookmarks_manual'] is not None else None
    if 'replies_manual' in data:
        post.replies_manual = int(data['replies_manual']) if data['replies_manual'] is not None else None
    if 'retweets_manual' in data:
        post.retweets_manual = int(data['retweets_manual']) if data['retweets_manual'] is not None else None
    if 'quotes_manual' in data:
        post.quotes_manual = int(data['quotes_manual']) if data['quotes_manual'] is not None else None

    # Review-Status
    if 'is_reviewed' in data:
        post.is_reviewed = bool(data['is_reviewed'])

    # Archive-Status
    if 'is_archived' in data:
        post.is_archived = bool(data['is_archived'])

    # Notizen
    if 'notes' in data:
        post.notes = data['notes']

    # Twitter-Datum
    if 'twitter_date' in data:
        post.twitter_date = data['twitter_date']

    # Trigger (Intensität 0-5)
    if 'trigger_angst' in data:
        post.trigger_angst = int(data['trigger_angst'])
    if 'trigger_wut' in data:
        post.trigger_wut = int(data['trigger_wut'])
    if 'trigger_ekel' in data:
        post.trigger_ekel = int(data['trigger_ekel'])
    if 'trigger_identitaet' in data:
        post.trigger_identitaet = int(data['trigger_identitaet'])
    if 'trigger_hoffnung' in data:
        post.trigger_hoffnung = int(data['trigger_hoffnung'])

    # Frames (Binär 0-1)
    if 'frame_opfer_taeter' in data:
        post.frame_opfer_taeter = int(data['frame_opfer_taeter'])
    if 'frame_bedrohung' in data:
        post.frame_bedrohung = int(data['frame_bedrohung'])
    if 'frame_verschwoerung' in data:
        post.frame_verschwoerung = int(data['frame_verschwoerung'])
    if 'frame_moral' in data:
        post.frame_moral = int(data['frame_moral'])
    if 'frame_historisch' in data:
        post.frame_historisch = int(data['frame_historisch'])

    post.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify(post.to_dict())


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Post löschen"""
    post = TwitterPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Post gelöscht'})


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Deskriptive Statistiken berechnen - NUR FÜR REVIEWED POSTS (OHNE ARCHIVIERTE)"""
    all_posts = TwitterPost.query.all()

    # Archivierte Posts zählen
    archived_posts = [p for p in all_posts if p.is_archived]

    # Nur nicht-archivierte Posts für Statistiken
    active_posts = [p for p in all_posts if not p.is_archived]

    # NUR REVIEWED POSTS für Statistiken verwenden (von nicht-archivierten)
    posts = [p for p in active_posts if p.is_reviewed]

    if not posts:
        return jsonify({
            'error': 'Keine reviewed Posts vorhanden',
            'total_posts': len(active_posts),
            'reviewed_posts': 0,
            'unreviewed_posts': len([p for p in active_posts if not p.is_reviewed]),
            'archived_posts': len(archived_posts)
        })

    # Daten sammeln (NUR von reviewed Posts)
    # Verwende manuelle Werte falls vorhanden, sonst automatische
    # WICHTIG: 0 ist ein gültiger Wert!
    ter_auto = [p.ter_automatic for p in posts if p.ter_automatic > 0]
    ter_manual = [p.ter_manual for p in posts if p.ter_manual is not None and p.ter_manual >= 0]

    # Views: manuelle Werte haben Vorrang, aber nur wenn gesetzt (auch 0 ist gültig)
    views = []
    for p in posts:
        val = p.views_manual if p.views_manual is not None else p.views
        if val is not None:
            views.append(val)

    followers = [p.twitter_followers for p in posts if p.twitter_followers > 0]
    likes = [(p.likes_manual if p.likes_manual is not None else p.likes) for p in posts]
    retweets = [(p.retweets_manual if p.retweets_manual is not None else p.retweets) for p in posts]
    replies = [(p.replies_manual if p.replies_manual is not None else p.replies) for p in posts]
    bookmarks = [(p.bookmarks_manual if p.bookmarks_manual is not None else p.bookmarks) for p in posts]
    quotes = [(p.quotes_manual if p.quotes_manual is not None else p.quotes) for p in posts]

    def calc_stats(data):
        """Berechnet Statistiken für eine Liste"""
        if not data:
            return None
        return {
            'count': len(data),
            'mean': round(statistics.mean(data), 2),
            'median': round(statistics.median(data), 2),
            'stdev': round(statistics.stdev(data), 2) if len(data) > 1 else 0,
            'min': round(min(data), 2),
            'max': round(max(data), 2),
            'sum': round(sum(data), 2)
        }

    return jsonify({
        'total_posts': len(active_posts),
        'reviewed_posts': len(posts),
        'unreviewed_posts': len([p for p in active_posts if not p.is_reviewed]),
        'archived_posts': len(archived_posts),
        'ter_automatic': calc_stats(ter_auto),
        'ter_manual': calc_stats(ter_manual),
        'views': calc_stats(views),
        'followers': calc_stats(followers),
        'likes': calc_stats(likes),
        'retweets': calc_stats(retweets),
        'replies': calc_stats(replies),
        'bookmarks': calc_stats(bookmarks),
        'quotes': calc_stats(quotes),
        'top_posts': [
            p.to_dict() for p in sorted(
                [p for p in posts if p.ter_manual is not None],
                key=lambda x: x.ter_manual,
                reverse=True
            )[:10]
        ]
    })


@app.route('/api/stats/distribution', methods=['GET'])
def get_distribution():
    """Verteilungsdaten für Charts"""
    posts = TwitterPost.query.all()

    # TER-Verteilung (Bins)
    ter_bins = [0, 1, 2, 5, 10, 20, 50, 100, float('inf')]
    ter_distribution = {f'{ter_bins[i]}-{ter_bins[i+1]}': 0 for i in range(len(ter_bins)-1)}

    for post in posts:
        ter = post.ter_automatic
        for i in range(len(ter_bins)-1):
            if ter_bins[i] <= ter < ter_bins[i+1]:
                key = f'{ter_bins[i]}-{ter_bins[i+1]}'
                ter_distribution[key] += 1
                break

    return jsonify({
        'ter_distribution': ter_distribution,
        'posts_by_date': {},  # TODO: Implementieren falls benötigt
    })


@app.route('/api/stats/timeline', methods=['GET'])
def get_timeline_stats():
    """Zeitreihen-Statistiken für Charts - NUR REVIEWED POSTS"""
    from collections import defaultdict
    from datetime import datetime as dt

    # NUR REVIEWED POSTS
    # NUR REVIEWED POSTS (OHNE ARCHIVIERTE)
    all_posts = TwitterPost.query.filter_by(is_reviewed=True, is_archived=False).all()

    if not all_posts:
        return jsonify({
            'monthly': [],
            'yearly': []
        })

    # Daten nach Monat gruppieren
    monthly_data = defaultdict(lambda: {'posts': [], 'ter_values': []})
    yearly_data = defaultdict(lambda: {'posts': [], 'ter_values': []})

    for post in all_posts:
        # Twitter-Datum parsen
        if not post.twitter_date:
            continue

        try:
            # Verschiedene Datumsformate versuchen
            date_str = post.twitter_date.strip()
            parsed_date = None

            # Format: ISO 8601 mit Zeitzone "2022-12-22T13:13:09.000Z"
            if 'T' in date_str:
                # Entferne Millisekunden und Zeitzone für einfacheres Parsen
                date_str_clean = date_str.split('.')[0] if '.' in date_str else date_str.rstrip('Z')
                try:
                    parsed_date = dt.fromisoformat(date_str_clean)
                except:
                    # Versuche alternatives ISO-Format
                    parsed_date = dt.strptime(date_str_clean.replace('Z', ''), '%Y-%m-%dT%H:%M:%S')
            # Format: "DD.MM.YYYY" oder "D.M.YYYY"
            elif '.' in date_str:
                parts = date_str.split('.')
                if len(parts) == 3:
                    day, month, year = parts
                    parsed_date = dt(int(year), int(month), int(day))
            # Format: "YYYY-MM-DD"
            elif '-' in date_str and date_str.count('-') == 2:
                parsed_date = dt.strptime(date_str, '%Y-%m-%d')
            # Format: "DD/MM/YYYY"
            elif '/' in date_str:
                parts = date_str.split('/')
                if len(parts) == 3:
                    day, month, year = parts
                    parsed_date = dt(int(year), int(month), int(day))

            if parsed_date:
                # Monatlicher Key: "YYYY-MM"
                month_key = parsed_date.strftime('%Y-%m')
                year_key = str(parsed_date.year)

                monthly_data[month_key]['posts'].append(post)
                yearly_data[year_key]['posts'].append(post)

                # TER Manuell sammeln (falls vorhanden) - WICHTIG: 0 ist gültig!
                if post.ter_manual is not None and post.ter_manual >= 0:
                    monthly_data[month_key]['ter_values'].append(post.ter_manual)
                    yearly_data[year_key]['ter_values'].append(post.ter_manual)

        except (ValueError, AttributeError):
            # Datum konnte nicht geparst werden, überspringen
            continue

    # Monatliche Statistiken erstellen
    monthly_stats = []
    for month_key in sorted(monthly_data.keys()):
        data = monthly_data[month_key]
        post_count = len(data['posts'])
        avg_ter = round(statistics.mean(data['ter_values']), 2) if data['ter_values'] else 0

        monthly_stats.append({
            'period': month_key,
            'label': month_key,  # Format: "2024-01"
            'post_count': post_count,
            'avg_ter': avg_ter,
            'posts_with_ter': len(data['ter_values'])
        })

    # Jährliche Statistiken erstellen
    yearly_stats = []
    for year_key in sorted(yearly_data.keys()):
        data = yearly_data[year_key]
        post_count = len(data['posts'])
        avg_ter = round(statistics.mean(data['ter_values']), 2) if data['ter_values'] else 0

        yearly_stats.append({
            'period': year_key,
            'label': year_key,  # Format: "2024"
            'post_count': post_count,
            'avg_ter': avg_ter,
            'posts_with_ter': len(data['ter_values'])
        })

    return jsonify({
        'monthly': monthly_stats,
        'yearly': yearly_stats
    })


@app.route('/api/stats/advanced', methods=['GET'])
def get_advanced_stats():
    """Erweiterte statistische Analysen: Korrelation, Regression, Gruppenvergleiche"""
    import numpy as np
    from scipy import stats as scipy_stats
    from sklearn.linear_model import LinearRegression

    # NUR REVIEWED POSTS mit TER-Werten
    # NUR REVIEWED POSTS (OHNE ARCHIVIERTE)
    posts = TwitterPost.query.filter_by(is_reviewed=True, is_archived=False).all()
    posts = [p for p in posts if p.ter_manual is not None and p.ter_manual >= 0]

    if len(posts) < 3:
        return jsonify({
            'error': 'Mindestens 3 reviewed Posts mit TER-Werten erforderlich',
            'post_count': len(posts)
        })

    # Daten sammeln
    ter_values = np.array([p.ter_manual for p in posts])
    trigger_angst = np.array([p.trigger_angst for p in posts])
    trigger_wut = np.array([p.trigger_wut for p in posts])
    trigger_ekel = np.array([p.trigger_ekel for p in posts])
    trigger_identitaet = np.array([p.trigger_identitaet for p in posts])
    trigger_hoffnung = np.array([p.trigger_hoffnung for p in posts])

    frame_opfer_taeter = np.array([p.frame_opfer_taeter for p in posts])
    frame_bedrohung = np.array([p.frame_bedrohung for p in posts])
    frame_verschwoerung = np.array([p.frame_verschwoerung for p in posts])
    frame_moral = np.array([p.frame_moral for p in posts])
    frame_historisch = np.array([p.frame_historisch for p in posts])

    # 1. KORRELATIONSANALYSE (Pearson)
    correlations = {}

    triggers = {
        'Angst/Bedrohung': trigger_angst,
        'Wut/Empörung': trigger_wut,
        'Ekel': trigger_ekel,
        'Identitätsbezug': trigger_identitaet,
        'Hoffnung/Stolz': trigger_hoffnung
    }

    frames = {
        'Opfer-Täter Frame': frame_opfer_taeter,
        'Bedrohungs-Frame': frame_bedrohung,
        'Verschwörungs-Frame': frame_verschwoerung,
        'Moral-Frame': frame_moral,
        'Historischer Frame': frame_historisch
    }

    for name, values in {**triggers, **frames}.items():
        if np.std(values) > 0:  # Nur wenn Varianz vorhanden
            corr, p_value = scipy_stats.pearsonr(values, ter_values)
            correlations[name] = {
                'correlation': round(float(corr), 3),
                'p_value': round(float(p_value), 4),
                'significant': bool(p_value < 0.05)
            }

    # 2. REGRESSIONSANALYSE
    # Alle Trigger als Features
    X = np.column_stack([
        trigger_angst, trigger_wut, trigger_ekel,
        trigger_identitaet, trigger_hoffnung,
        frame_bedrohung, frame_opfer_taeter, frame_verschwoerung,
        frame_moral, frame_historisch
    ])
    y = ter_values

    try:
        model = LinearRegression()
        model.fit(X, y)

        feature_names = [
            'Angst', 'Wut', 'Ekel', 'Identität', 'Hoffnung',
            'Bedrohung-Frame', 'Opfer-Täter-Frame', 'Verschwörung-Frame',
            'Moral-Frame', 'Historisch-Frame'
        ]

        coefficients = [
            {
                'feature': name,
                'coefficient': round(float(coef), 4),
                'abs_coefficient': round(abs(float(coef)), 4)
            }
            for name, coef in zip(feature_names, model.coef_)
        ]

        # Sortiere nach absoluter Stärke
        coefficients.sort(key=lambda x: x['abs_coefficient'], reverse=True)

        regression = {
            'r_squared': round(float(model.score(X, y)), 3),
            'intercept': round(float(model.intercept_), 4),
            'coefficients': coefficients
        }
    except:
        regression = {'error': 'Regression konnte nicht berechnet werden'}

    # 3. GRUPPENVERGLEICHE (t-Tests)
    group_comparisons = []

    # Vergleiche für jeden Frame: mit vs. ohne
    for frame_name, frame_values in frames.items():
        group_with = ter_values[frame_values == 1]
        group_without = ter_values[frame_values == 0]

        if len(group_with) >= 2 and len(group_without) >= 2:
            t_stat, p_value = scipy_stats.ttest_ind(group_with, group_without)

            group_comparisons.append({
                'frame': frame_name,
                'with_frame': {
                    'count': int(len(group_with)),
                    'mean_ter': round(float(np.mean(group_with)), 2),
                    'std_ter': round(float(np.std(group_with)), 2)
                },
                'without_frame': {
                    'count': int(len(group_without)),
                    'mean_ter': round(float(np.mean(group_without)), 2),
                    'std_ter': round(float(np.std(group_without)), 2)
                },
                't_statistic': round(float(t_stat), 3),
                'p_value': round(float(p_value), 4),
                'significant': bool(p_value < 0.05),
                'effect_size': round(float(np.mean(group_with) - np.mean(group_without)), 2)
            })

    # 4. DESKRIPTIVE STATISTIKEN
    descriptive = {
        'post_count': len(posts),
        'ter_mean': round(float(np.mean(ter_values)), 2),
        'ter_std': round(float(np.std(ter_values)), 2),
        'ter_min': round(float(np.min(ter_values)), 2),
        'ter_max': round(float(np.max(ter_values)), 2),
        'trigger_means': {
            'Angst': round(float(np.mean(trigger_angst)), 2),
            'Wut': round(float(np.mean(trigger_wut)), 2),
            'Ekel': round(float(np.mean(trigger_ekel)), 2),
            'Identität': round(float(np.mean(trigger_identitaet)), 2),
            'Hoffnung': round(float(np.mean(trigger_hoffnung)), 2)
        }
    }

    # 5. CLUSTERANALYSE (K-Means)
    clusters = None
    if len(posts) >= 10:  # Mindestens 10 Posts für sinnvolles Clustering
        try:
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import StandardScaler

            # Features: Nur Trigger (0-5 Skala)
            X_clustering = np.column_stack([
                trigger_angst, trigger_wut, trigger_ekel,
                trigger_identitaet, trigger_hoffnung
            ])

            # Standardisierung
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_clustering)

            # K-Means mit 3 Clustern
            n_clusters = 3
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(X_scaled)

            # Cluster-Profile berechnen
            cluster_profiles = []
            for i in range(n_clusters):
                cluster_mask = cluster_labels == i
                cluster_posts = np.array(posts)[cluster_mask]

                profile = {
                    'cluster_id': int(i),
                    'size': int(np.sum(cluster_mask)),
                    'avg_ter': round(float(np.mean(ter_values[cluster_mask])), 2),
                    'trigger_profile': {
                        'Angst': round(float(np.mean(trigger_angst[cluster_mask])), 2),
                        'Wut': round(float(np.mean(trigger_wut[cluster_mask])), 2),
                        'Ekel': round(float(np.mean(trigger_ekel[cluster_mask])), 2),
                        'Identität': round(float(np.mean(trigger_identitaet[cluster_mask])), 2),
                        'Hoffnung': round(float(np.mean(trigger_hoffnung[cluster_mask])), 2)
                    }
                }

                # Dominant Trigger identifizieren
                trigger_values = list(profile['trigger_profile'].values())
                trigger_names = list(profile['trigger_profile'].keys())
                max_trigger_idx = np.argmax(trigger_values)
                profile['dominant_trigger'] = trigger_names[max_trigger_idx]

                cluster_profiles.append(profile)

            # Sortiere nach TER
            cluster_profiles.sort(key=lambda x: x['avg_ter'], reverse=True)

            clusters = {
                'n_clusters': n_clusters,
                'profiles': cluster_profiles,
                'silhouette_score': None  # Optional: Könnte hinzugefügt werden
            }

        except Exception as e:
            print(f"Clustering error: {e}")
            clusters = {'error': 'Clusteranalyse konnte nicht durchgeführt werden'}

    return jsonify({
        'descriptive': descriptive,
        'correlations': correlations,
        'regression': regression,
        'group_comparisons': group_comparisons,
        'clusters': clusters
    })


# ==================== SESSION MANAGEMENT ====================

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Alle Analysesitzungen abrufen"""
    sessions = AnalysisSession.query.order_by(AnalysisSession.updated_at.desc()).all()
    return jsonify({
        'sessions': [session.to_dict() for session in sessions],
        'total': len(sessions)
    })


@app.route('/api/sessions/<int:session_id>', methods=['GET'])
def get_session(session_id):
    """Einzelne Session abrufen"""
    session = AnalysisSession.query.get_or_404(session_id)
    return jsonify(session.to_dict())


@app.route('/api/sessions', methods=['POST'])
def create_session():
    """Neue Analysesitzung erstellen"""
    data = request.json
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()

    if not name:
        return jsonify({'error': 'Name ist erforderlich'}), 400

    # Prüfe ob Name bereits existiert
    existing = AnalysisSession.query.filter_by(name=name).first()
    if existing:
        return jsonify({'error': 'Eine Session mit diesem Namen existiert bereits'}), 400

    try:
        # Neue Session erstellen
        session = AnalysisSession(
            name=name,
            description=description,
            is_active=False
        )
        db.session.add(session)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Session "{name}" erfolgreich erstellt',
            'session': session.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Fehler beim Erstellen der Session: {str(e)}'}), 500


@app.route('/api/sessions/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    """Session aktualisieren (Name, Beschreibung, etc.)"""
    session = AnalysisSession.query.get_or_404(session_id)
    data = request.json

    if 'name' in data:
        new_name = data['name'].strip()
        if new_name:
            # Prüfe ob neuer Name bereits existiert (außer bei aktueller Session)
            existing = AnalysisSession.query.filter(
                AnalysisSession.name == new_name,
                AnalysisSession.id != session_id
            ).first()
            if existing:
                return jsonify({'error': 'Eine Session mit diesem Namen existiert bereits'}), 400
            session.name = new_name

    if 'description' in data:
        session.description = data['description']

    session.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify(session.to_dict())


@app.route('/api/sessions/<int:session_id>/activate', methods=['POST'])
def activate_session(session_id):
    """Session als aktiv setzen (deaktiviert alle anderen)"""
    try:
        # Alle Sessions auf inaktiv setzen
        AnalysisSession.query.update({'is_active': False})

        # Ausgewählte Session aktivieren
        session = AnalysisSession.query.get_or_404(session_id)
        session.is_active = True
        session.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Session "{session.name}" ist jetzt aktiv',
            'session': session.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Fehler beim Aktivieren: {str(e)}'}), 500


@app.route('/api/sessions/active', methods=['GET'])
def get_active_session():
    """Aktive Session abrufen"""
    session = AnalysisSession.query.filter_by(is_active=True).first()
    if not session:
        return jsonify({'active_session': None})
    return jsonify({'active_session': session.to_dict()})


@app.route('/api/sessions/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Session und alle zugehörigen Posts löschen"""
    session = AnalysisSession.query.get_or_404(session_id)

    try:
        session_name = session.name
        db.session.delete(session)  # Cascade löscht automatisch alle Posts
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Session "{session_name}" und alle zugehörigen Posts wurden gelöscht'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Fehler beim Löschen: {str(e)}'}), 500


# ==================== INITIALISIERUNG ====================

if __name__ == '__main__':
    # Datenbank initialisieren
    with app.app_context():
        db.create_all()
        print("[OK] Datenbank initialisiert")

    print("\n" + "="*80)
    print("TWITTER TER DASHBOARD")
    print("="*80)
    print("\n[START] Server startet...")
    print("[DASHBOARD] http://localhost:5001")
    print("[API] http://localhost:5001/api/")
    print("\n")

    app.run(debug=True, host='0.0.0.0', port=5001)
