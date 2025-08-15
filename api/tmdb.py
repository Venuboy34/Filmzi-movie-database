import requests
from datetime import datetime
from flask import current_app

def fetch_movie_details(tmdb_id):
    api_key = current_app.config['TMDB_API_KEY']
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            return None
        
        return {
            'tmdb_id': tmdb_id,
            'title': data.get('title'),
            'description': data.get('overview'),
            'poster_url': f"https://image.tmdb.org/t/p/original{data.get('poster_path')}" if data.get('poster_path') else '',
            'release_date': datetime.strptime(data.get('release_date'), '%Y-%m-%d') if data.get('release_date') else None,
            'language': data.get('original_language')
        }
    except Exception as e:
        print(f"TMDB Error: {str(e)}")
        return None

def fetch_tv_details(tmdb_id):
    api_key = current_app.config['TMDB_API_KEY']
    url = f'https://api.themoviedb.org/3/tv/{tmdb_id}?api_key={api_key}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            return None
        
        return {
            'tmdb_id': tmdb_id,
            'title': data.get('name'),
            'description': data.get('overview'),
            'poster_url': f"https://image.tmdb.org/t/p/original{data.get('poster_path')}" if data.get('poster_path') else '',
            'release_date': datetime.strptime(data.get('first_air_date'), '%Y-%m-%d') if data.get('first_air_date') else None,
            'language': data.get('original_language')
        }
    except Exception as e:
        print(f"TMDB TV Error: {str(e)}")
        return None

def fetch_tv_season_details(tmdb_id, season_number):
    api_key = current_app.config['TMDB_API_KEY']
    url = f'https://api.themoviedb.org/3/tv/{tmdb_id}/season/{season_number}?api_key={api_key}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            return None
        
        return data.get('episodes', [])
    except Exception as e:
        print(f"TMDB Season Error: {str(e)}")
        return None
