import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from flask_basicauth import BasicAuth
from sqlalchemy import func
from .models import db, Movie, TVSeries, Season, Episode
from .tmdb import fetch_movie_details, fetch_tv_details, fetch_tv_season_details
from .utils import error_response

app = Flask(__name__)
CORS(app)

# Neon PostgreSQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_W8EduA9LzYBm@ep-royal-field-a1sp0296-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 300,
    'pool_pre_ping': True
}
app.config['BASIC_AUTH_USERNAME'] = 'venura'
app.config['BASIC_AUTH_PASSWORD'] = 'venura'
app.config['TMDB_API_KEY'] = os.getenv('TMDB_API_KEY', '52f6a75a38a397d940959b336801e1c3')

# Initialize extensions
db.init_app(app)
basic_auth = BasicAuth(app)

@app.route('/')
def index():
    return jsonify({'message': 'Movie/Series Database API'})

@app.route('/health')
def health_check():
    try:
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/api/stats')
def stats():
    movies = db.session.query(func.count(Movie.id)).scalar()
    series = db.session.query(func.count(TVSeries.id)).scalar()
    episodes = db.session.query(func.count(Episode.id)).scalar()
    return jsonify({
        'movies': movies,
        'tv_series': series,
        'episodes': episodes,
        'total': movies + series
    })

@app.route('/media')
def get_all_media():
    movies = Movie.query.all()
    series = TVSeries.query.all()
    return jsonify({
        'movies': [m.serialize() for m in movies],
        'tv_series': [s.serialize() for s in series]
    })

@app.route('/media/<int:media_id>')
def get_media(media_id):
    movie = Movie.query.get(media_id)
    if movie:
        return jsonify(movie.serialize())
    series = TVSeries.query.get(media_id)
    if series:
        return jsonify(series.serialize_with_seasons())
    return error_response('Media not found', 404)

@app.route('/search')
def search_media():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': []})
    
    movies = Movie.query.filter(
        Movie.title.ilike(f'%{query}%') | 
        Movie.description.ilike(f'%{query}%') |
        Movie.language.ilike(f'%{query}%') |
        Movie.dubbed_language.ilike(f'%{query}%')
    ).all()
    
    series = TVSeries.query.filter(
        TVSeries.title.ilike(f'%{query}%') | 
        TVSeries.description.ilike(f'%{query}%') |
        TVSeries.language.ilike(f'%{query}%') |
        TVSeries.dubbed_language.ilike(f'%{query}%')
    ).all()
    
    return jsonify({
        'movies': [m.serialize() for m in movies],
        'tv_series': [s.serialize() for s in series]
    })

# Admin Routes
@app.route('/admin')
@basic_auth.required
def admin_panel():
    movies = Movie.query.all()
    series = TVSeries.query.all()
    return render_template('admin.html', movies=movies, series=series)

@app.route('/admin/movie/new', methods=['GET', 'POST'])
@basic_auth.required
def add_movie():
    if request.method == 'POST':
        data = request.form
        tmdb_id = data.get('tmdb_id')
        
        if tmdb_id:
            tmdb_data = fetch_movie_details(tmdb_id)
            if not tmdb_data:
                return render_template('edit_movie.html', error='TMDB ID not found')
            movie = Movie(**tmdb_data)
        else:
            movie = Movie()
        
        # Update fields
        movie.title = data.get('title', movie.title)
        movie.description = data.get('description', movie.description)
        movie.poster_url = data.get('poster_url', movie.poster_url)
        movie.release_date = data.get('release_date', movie.release_date)
        movie.language = data.get('language', movie.language)
        movie.dubbed_language = data.get('dubbed_language', movie.dubbed_language)
        movie.video_720p = data.get('video_720p', movie.video_720p)
        movie.video_1080p = data.get('video_1080p', movie.video_1080p)
        
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('admin_panel'))
    
    return render_template('edit_movie.html')

@app.route('/admin/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@basic_auth.required
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        data = request.form
        movie.title = data.get('title', movie.title)
        movie.description = data.get('description', movie.description)
        movie.poster_url = data.get('poster_url', movie.poster_url)
        movie.release_date = data.get('release_date', movie.release_date)
        movie.language = data.get('language', movie.language)
        movie.dubbed_language = data.get('dubbed_language', movie.dubbed_language)
        movie.video_720p = data.get('video_720p', movie.video_720p)
        movie.video_1080p = data.get('video_1080p', movie.video_1080p)
        
        db.session.commit()
        return redirect(url_for('admin_panel'))
    
    return render_template('edit_movie.html', movie=movie)

@app.route('/admin/movie/delete/<int:movie_id>', methods=['POST'])
@basic_auth.required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/series/new', methods=['GET', 'POST'])
@basic_auth.required
def add_series():
    if request.method == 'POST':
        data = request.form
        tmdb_id = data.get('tmdb_id')
        
        if tmdb_id:
            tmdb_data = fetch_tv_details(tmdb_id)
            if not tmdb_data:
                return render_template('edit_series.html', error='TMDB ID not found')
            series = TVSeries(**tmdb_data)
        else:
            series = TVSeries()
        
        # Update fields
        series.title = data.get('title', series.title)
        series.description = data.get('description', series.description)
        series.poster_url = data.get('poster_url', series.poster_url)
        series.release_date = data.get('release_date', series.release_date)
        series.language = data.get('language', series.language)
        series.dubbed_language = data.get('dubbed_language', series.dubbed_language)
        
        db.session.add(series)
        db.session.commit()
        return redirect(url_for('admin_panel'))
    
    return render_template('edit_series.html')

@app.route('/admin/series/edit/<int:series_id>', methods=['GET', 'POST'])
@basic_auth.required
def edit_series(series_id):
    series = TVSeries.query.get_or_404(series_id)
    if request.method == 'POST':
        data = request.form
        series.title = data.get('title', series.title)
        series.description = data.get('description', series.description)
        series.poster_url = data.get('poster_url', series.poster_url)
        series.release_date = data.get('release_date', series.release_date)
        series.language = data.get('language', series.language)
        series.dubbed_language = data.get('dubbed_language', series.dubbed_language)
        
        db.session.commit()
        return redirect(url_for('admin_panel'))
    
    return render_template('edit_series.html', series=series)

@app.route('/admin/series/delete/<int:series_id>', methods=['POST'])
@basic_auth.required
def delete_series(series_id):
    series = TVSeries.query.get_or_404(series_id)
    db.session.delete(series)
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/series/<int:series_id>/season/new', methods=['GET', 'POST'])
@basic_auth.required
def add_season(series_id):
    series = TVSeries.query.get_or_404(series_id)
    if request.method == 'POST':
        data = request.form
        season = Season(
            tv_series_id=series_id,
            season_number=data.get('season_number')
        )
        db.session.add(season)
        db.session.commit()
        return redirect(url_for('edit_season', season_id=season.id))
    
    return render_template('edit_season.html', series=series)

@app.route('/admin/season/edit/<int:season_id>', methods=['GET', 'POST'])
@basic_auth.required
def edit_season(season_id):
    season = Season.query.get_or_404(season_id)
    if request.method == 'POST':
        data = request.form
        season.season_number = data.get('season_number', season.season_number)
        db.session.commit()
        return redirect(url_for('admin_panel'))
    
    return render_template('edit_season.html', season=season)

@app.route('/admin/season/delete/<int:season_id>', methods=['POST'])
@basic_auth.required
def delete_season(season_id):
    season = Season.query.get_or_404(season_id)
    db.session.delete(season)
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/season/<int:season_id>/episode/new', methods=['GET', 'POST'])
@basic_auth.required
def add_episode(season_id):
    season = Season.query.get_or_404(season_id)
    if request.method == 'POST':
        data = request.form
        episode = Episode(
            season_id=season_id,
            episode_number=data.get('episode_number'),
            episode_title=data.get('episode_title'),
            video_720p=data.get('video_720p')
        )
        db.session.add(episode)
        db.session.commit()
        return redirect(url_for('edit_episode', episode_id=episode.id))
    
    return render_template('edit_episode.html', season=season)

@app.route('/admin/episode/edit/<int:episode_id>', methods=['GET', 'POST'])
@basic_auth.required
def edit_episode(episode_id):
    episode = Episode.query.get_or_404(episode_id)
    if request.method == 'POST':
        data = request.form
        episode.episode_number = data.get('episode_number', episode.episode_number)
        episode.episode_title = data.get('episode_title', episode.episode_title)
        episode.video_720p = data.get('video_720p', episode.video_720p)
        db.session.commit()
        return redirect(url_for('admin_panel'))
    
    return render_template('edit_episode.html', episode=episode)

@app.route('/admin/episode/delete/<int:episode_id>', methods=['POST'])
@basic_auth.required
def delete_episode(episode_id):
    episode = Episode.query.get_or_404(episode_id)
    db.session.delete(episode)
    db.session.commit()
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
