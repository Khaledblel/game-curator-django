# 🎮 Game Curator - AI-Powered Game Recommendation Platform

![Game Curator Banner](recommender/static/recommender/assets/logo.png)

Game Curator is a sophisticated web application built with Django that leverages AI to provide personalized video game recommendations. Users can describe their gaming preferences in natural language, and the system will suggest relevant games they might enjoy.

## ✨ Features

- **AI-Powered Recommendations**: Natural language processing to understand user preferences
- **Detailed Game Information**: Comprehensive details including ratings, genres, platforms, screenshots, and more
- **Favorites System**: Save games to your personal favorites list
- **Franchise Timeline View**: Explore game franchises with an interactive timeline
- **DLC & Expansion Tracking**: View downloadable content and expansions for recommended games
- **Responsive Design**: Fully optimized for both desktop and mobile devices


## 🛠️ Technologies Used

- **Backend**: Django 5.2, Python 3.x
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS 
- **Database**: MySQL (Azure Database for MySQL)
- **Authentication**: Django Authentication System
- **API Integration**: IGDB (Internet Game Database) API
- **Deployment**: Azure Web App Service

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python Package Installer)
- MySQL database
- IGDB API credentials

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/game-curator-django.git
cd game-curator-django
```

2. **Set up a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install required dependencies**

```bash
pip install -r requirements.txt
```

4. **Create a .env file in the project root with the following variables**

```
SECRET_KEY=your_django_secret_key
AZURE_MYSQL_NAME=your_mysql_db_name
AZURE_MYSQL_USER=your_mysql_username
AZURE_MYSQL_PASSWORD=your_mysql_password
AZURE_MYSQL_HOST=your_mysql_host
AZURE_MYSQL_PORT=3306
IGDB_CLIENT_ID=your_igdb_client_id
IGDB_CLIENT_SECRET=your_igdb_client_secret
```

5. **Run migrations**

```bash
python manage.py migrate
```

6. **Start development server**

```bash
python manage.py runserver
```

7. **Access the application at http://127.0.0.1:8000/**

## 📊 Project Structure

```
game-curator-django/
├── game_curator/             # Main Django project
│   ├── settings.py           # Project settings 
│   ├── urls.py               # Project URL configuration
│   └── wsgi.py               # WSGI configuration 
├── recommender/              # Game recommendation app
│   ├── models.py             # Data models
│   ├── views.py              # View functions
│   ├── templates/            # HTML templates
│   └── static/               # Static assets
├── authentication/           # User authentication app
│   └── ...                   # Auth-related files
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in version control)
└── README.md                 # Project documentation
```

## 🌟 Key Features Explained

### AI Game Recommendation Engine

The core feature of Game Curator is its intelligent recommendation system. Users can describe what they're looking for in natural language (e.g., "An open-world RPG with dragons and deep lore"), and the system will:

1. Process the request using NLP techniques
2. Query the IGDB database with relevant parameters
3. Rank and filter results based on relevance
4. Return a main recommendation and similar alternatives

### Detailed Game Information

For each recommended game, we display comprehensive information:

- Basic details (title, release date, developer, publisher)
- Media (cover art, screenshots)
- Genres, themes, and game modes
- Platform availability
- Age ratings (ESRB, PEGI)
- Storyline and summary
- DLC and expansion information
- Time to beat estimates
- Language support details

### Franchise Timeline

For games that are part of a larger franchise, users can explore an interactive timeline showing:

- All games in chronological order
- Release years
- Game types (main entries, expansions, DLC)
- Ratings and cover art

### User Authentication and Favorites

- Users can create accounts to save their preferences
- "Favorite" games are stored in the user's profile
- Browse and manage favorite games from a dedicated page

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📬 Contact

Project Link: [https://github.com/yourusername/game-curator-django](https://github.com/yourusername/game-curator-django)

---

<div align="center">
  <p>Built with ❤️ by <a href="https://github.com/yourusername">Your Name</a></p>
</div>
