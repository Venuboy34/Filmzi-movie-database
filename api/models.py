from . import db
from datetime import datetime
from sqlalchemy import ForeignKey

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    poster_url = db.Column(db.String(500))
    release_date = db.Column(db.Date)
    language = db.Column(db.String(50))
    dubbed_language = db.Column(db.String(50))
    video_720p = db.Column(db.String(500))
    video_1080p = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'tmdb_id': self.tmdb_id,
            'title': self.title,
            'description': self.description,
            'poster_url': self.poster_url,
            'release_date': str(self.release_date) if self.release_date else None,
            'language': self.language,
            'dubbed_language': self.dubbed_language,
            'video_720p': self.video_720p,
            'video_1080p': self.video_1080p,
            'created_at': self.created_at.isoformat()
        }

class TVSeries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    poster_url = db.Column(db.String(500))
    release_date = db.Column(db.Date)
    language = db.Column(db.String(50))
    dubbed_language = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    seasons = db.relationship('Season', backref='series', lazy=True, cascade="all, delete-orphan")

    def serialize(self):
        return {
            'id': self.id,
            'tmdb_id': self.tmdb_id,
            'title': self.title,
            'description': self.description,
            'poster_url': self.poster_url,
            'release_date': str(self.release_date) if self.release_date else None,
            'language': self.language,
            'dubbed_language': self.dubbed_language,
            'created_at': self.created_at.isoformat()
        }
    
    def serialize_with_seasons(self):
        data = self.serialize()
        data['seasons'] = [season.serialize() for season in self.seasons]
        return data

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tv_series_id = db.Column(db.Integer, ForeignKey('tv_series.id'), nullable=False)
    season_number = db.Column(db.Integer, nullable=False)
    episodes = db.relationship('Episode', backref='season', lazy=True, cascade="all, delete-orphan")

    def serialize(self):
        return {
            'id': self.id,
            'season_number': self.season_number,
            'episodes': [episode.serialize() for episode in self.episodes]
        }

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, ForeignKey('season.id'), nullable=False)
    episode_number = db.Column(db.Integer, nullable=False)
    episode_title = db.Column(db.String(255))
    video_720p = db.Column(db.String(500))

    def serialize(self):
        return {
            'id': self.id,
            'episode_number': self.episode_number,
            'title': self.episode_title,
            'video_720p': self.video_720p
        }
