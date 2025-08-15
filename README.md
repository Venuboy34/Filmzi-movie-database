# Movie & TV Series Database

A full-stack Flask application for managing movies and TV series with PostgreSQL backend, TMDB API integration, and admin panel.

![Admin Panel Screenshot](https://via.placeholder.com/800x400?text=Admin+Panel+Screenshot)

## Features

- **Full CRUD Operations** for movies, TV series, seasons, and episodes
- **TMDB API Integration** for auto-filling media details
- **Admin Panel** with basic authentication
- **Public API Endpoints** for frontend/mobile apps
- **PostgreSQL Database** with Neon compatibility
- **Vercel Deployment Ready**

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL (Neon)
- **Frontend**: Bootstrap templates
- **API**: TMDB integration
- **Hosting**: Vercel

## Database Schema

![Database Schema](https://via.placeholder.com/600x400?text=Database+Schema)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/media` | GET | Get all movies and TV series |
| `/media/<id>` | GET | Get specific movie/TV series details |
| `/search?q=query` | GET | Search media by title/description/language |
| `/health` | GET | Database health check |
| `/api/stats` | GET | Database statistics |

## Admin Panel Features

- Add/edit/delete movies with TMDB integration
- Manage TV series with seasons and episodes
- Search and filter content
- Basic authentication (username: venura, password: venura)

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL database (Neon recommended)
- TMDB API key

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/movie-database.git
cd movie-database
