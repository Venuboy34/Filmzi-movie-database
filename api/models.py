from . import db
from datetime import datetime
from sqlalchemy import ForeignKey

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, index=True)
    # ... [Keep all other columns from previous version] ...

    def serialize(self):
        return {
            'id': self.id,
            # ... [Keep all serialization from previous version] ...
        }

class TVSeries(db.Model):
    __tablename__ = 'tv_series'
    # ... [Keep all columns from previous version] ...

    def serialize_with_seasons(self):
        data = self.serialize()
        data['seasons'] = [{
            'id': season.id,
            'season_number': season.season_number,
            'episodes': [{
                'id': ep.id,
                'episode_number': ep.episode_number,
                'title': ep.episode_title,
                'video_720p': ep.video_720p
            } for ep in season.episodes]
        } for season in self.seasons]
        return data

# ... [Keep Season and Episode models from previous version] ...
