CREATE TABLE movie (
    id SERIAL PRIMARY KEY,
    tmdb_id INTEGER,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    poster_url VARCHAR(500),
    release_date DATE,
    language VARCHAR(50),
    dubbed_language VARCHAR(50),
    video_720p VARCHAR(500),
    video_1080p VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tv_series (
    id SERIAL PRIMARY KEY,
    tmdb_id INTEGER,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    poster_url VARCHAR(500),
    release_date DATE,
    language VARCHAR(50),
    dubbed_language VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE season (
    id SERIAL PRIMARY KEY,
    tv_series_id INTEGER REFERENCES tv_series(id) ON DELETE CASCADE,
    season_number INTEGER NOT NULL
);

CREATE TABLE episode (
    id SERIAL PRIMARY KEY,
    season_id INTEGER REFERENCES season(id) ON DELETE CASCADE,
    episode_number INTEGER NOT NULL,
    episode_title VARCHAR(255),
    video_720p VARCHAR(500)
);
