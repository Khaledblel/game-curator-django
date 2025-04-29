# 🎮 Game Curator

![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-Azure-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

> A personalized game recommendation web application built with Django, powered by AI

## 📖 Overview

Game Curator is an intelligent web application that recommends video games based on user preferences. Leveraging Google's Gemini AI for natural language understanding and IGDB's extensive game database, it offers personalized game suggestions tailored to each user's unique tastes and requirements.


## ✨ Features

- **🤖 AI-Powered Recommendations**: Natural language input processing using Google Gemini API
- **🎯 Personalized Suggestions**: Get games tailored to your specific preferences
- **💾 Favorites System**: Save and manage your favorite game recommendations
- **🔒 User Authentication**: Secure login and registration system
- **📱 Responsive Design**: Enjoy a seamless experience across devices

## 🛠️ Technologies Used

- **Backend**: Django 5.2, Python
- **Database**: MySQL (Azure)
- **APIs**: 
  - IGDB API for game data 
  - Google Gemini API for AI recommendations
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Django built-in auth system

## 🎮 IGDB API Endpoints

The application currently uses the following IGDB API endpoints:

- **/games**: Fetches basic game information and metadata
- **/covers**: Retrieves game cover images
- **/genres**: Gets genre information for categorization
- **/platforms**: Obtains platform availability data
- **/companies**: Retrieves publisher and developer information

API documentation: [IGDB API Docs](https://api-docs.igdb.com/)

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- pip
- MySQL database
- IGDB API credentials
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/game-curator-django.git
   cd game-curator-django
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   
   Create a `.env` file in the project root with the following variables:
   ```
   # Database Configuration
   AZURE_MYSQL_NAME=your_db_name
   AZURE_MYSQL_USER=your_db_username
   AZURE_MYSQL_PASSWORD=your_db_password
   AZURE_MYSQL_HOST=your_db_host
   AZURE_MYSQL_PORT=3306
   
   # API Keys
   IGDB_CLIENT_ID=your_igdb_client_id
   IGDB_CLIENT_SECRET=your_igdb_client_secret
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   
   Open your browser and navigate to `http://127.0.0.1:8000`

## 🧰 Project Structure

```
game_curator/
├── authentication/        # User authentication app
├── recommender/           # Main recommendation app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── utils/             # Utility functions
│   │   ├── gemini_api.py  # Google Gemini API integration
│   │   └── igdb_api.py    # IGDB API integration
│   └── templates/         # HTML templates
├── game_curator/          # Project settings
└── static/                # Static files (CSS, JS, images)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Django](https://www.djangoproject.com/) - The web framework used
- [IGDB API](https://www.igdb.com/api) - For providing the game data
- [Google Gemini](https://ai.google/discover/gemini/) - For AI-powered recommendations

---

Made with ❤️ by Khaled
