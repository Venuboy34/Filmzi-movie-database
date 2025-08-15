import os
import logging
from flask import Flask, jsonify, request, render_template, redirect, url_for
from . import app, db, basic_auth
from .models import Movie, TVSeries, Season, Episode
from .tmdb import fetch_movie_details, fetch_tv_details
from flask_cors import CORS

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 5,
    'max_overflow': 10,
    'pool_timeout': 30,
    'pool_recycle': 300
}
app.config['BASIC_AUTH_USERNAME'] = 'venura'
app.config['BASIC_AUTH_PASSWORD'] = 'venura'
app.config['TMDB_API_KEY'] = os.getenv('TMDB_API_KEY')

# Initialize extensions
CORS(app)
db.init_app(app)
basic_auth.init_app(app)

# Error handling
@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Server Error: {str(error)}")
    return jsonify({"error": "Internal server error", "message": str(error)}), 500

@app.route('/test')
def test():
    try:
        db.session.execute('SELECT 1')
        return jsonify({"status": "OK", "database": "connected"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check endpoint
@app.route('/health')
def health_check():
    try:
        db.session.execute('SELECT 1')
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        logging.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

# ... [Keep all your existing routes from previous version] ...

# Database initialization
@app.before_first_request
def initialize_database():
    try:
        db.create_all()
        logging.info("Database tables created")
    except Exception as e:
        logging.error(f"Database initialization failed: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
