# GameBuddy 🎮

![GameBuddy Banner](frontend/public/images/logo_banner.png)

## 📋 Project Overview

GameBuddy is a comprehensive platform for gamers, offering game recommendations, information search, wishlist management, review sharing, and more. Users can also access personalized game recommendations through our AI-powered chatbot.

This project is a full-stack web application built with a React frontend and Django backend.

### 💡 Motivation

Modern gamers struggle to find suitable games among vast libraries. GameBuddy was developed to solve this challenge by providing a personalized game recommendation system and a user-friendly interface to enhance gamers' exploration experience.

### 🔍 Key Features

- **Game Exploration & Search**: Find games through various filtering options
- **AI Chatbot**: Get personalized game recommendations
- **User Profiles**: Customizable profiles with image upload capability
- **Wishlist System**: Save and manage games of interest
- **Review System**: Write and share game reviews
- **Responsive Design**: Optimized for all devices from mobile to desktop

## 🛠️ Technology Stack

### Frontend
- **React**: Building user interfaces
- **React Router**: Client-side routing
- **Context API**: State management
- **CSS**: Styling (responsive design)
- **Lucide React**: Icons

### Backend
- **Django**: Web framework
- **Django REST Framework**: RESTful API development
- **PostgreSQL**: Database
- **Token Authentication**: Security and user authentication

### Deployment & Other Tools
- **Git/GitHub**: Version control
- **NGINX**: Web server
- **AWS/Heroku**: Cloud hosting (planned)

## 📸 Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Game Detail Page
![Game Detail](screenshots/game_detail.png)

### Profile Page
![Profile](screenshots/profile.png)

### AI Chatbot
![Chatbot](screenshots/chatbot.png)

## ⚙️ Installation & Setup

### Prerequisites
- Node.js and npm
- Python 3.8+
- pip
- PostgreSQL

### Backend Setup
```bash
# Clone repository
git clone https://github.com/yourusername/GameBuddy.git
cd GameBuddy

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Frontend Setup
```bash
# From project root directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 📊 Data Collection

GameBuddy uses the [RAWG Video Games Database API](https://rawg.io/apidocs) to populate its database with game information. Follow these steps to collect game data:

### Getting an API Key

1. Create an account on [RAWG](https://rawg.io)
2. Navigate to your dashboard and get your API key
3. Create a `.env` file in the backend directory with the following content:
   ```
   RAWG_API_KEY=your_api_key_here
   ```

### Running the Data Collection Command

The project includes a custom Django management command for efficient data collection:

```bash
# Activate your virtual environment if not already active
cd backend

# Basic usage
python manage.py fetch_game_data

# Advanced usage with parameters
python manage.py fetch_game_data --max-pages=50 --workers=8 --batch-size=100 --start-page=1
```

### Command Parameters

- `--max-pages`: Maximum number of pages to fetch (default: 1000)
- `--workers`: Number of worker threads for parallel processing (default: 10)
- `--batch-size`: Number of games to save in one database transaction (default: 100)
- `--start-page`: Starting page number for API requests (default: 1)

### Data Collection Process

The command uses multi-threading to speed up the data collection process:

1. Creates multiple worker threads to fetch game data in parallel
2. Processes the raw API data into structured format
3. Batches database operations for improved performance
4. Logs detailed progress information during the collection process

Data collection speed will vary based on your internet connection and system resources. The entire RAWG database contains thousands of games, so consider starting with a smaller number of pages for testing.

## 🗂️ Project Structure

```
GameBuddy/
├── backend/
│   ├── accounts/          # User account management
│   ├── games/             # Game information management
│   ├── reviews/           # Review system
│   ├── wishlist/          # Wishlist functionality
│   ├── chatbot/           # AI chatbot service
│   └── requirements.txt   # Backend dependencies
│
├── frontend/
│   ├── public/            # Static files
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── contexts/      # Context API
│   │   ├── pages/         # Page components
│   │   ├── styles/        # CSS styles
│   │   └── App.js         # Main app component
│   └── package.json       # Frontend dependencies
│
└── README.md              # Project documentation
```

## 🚀 Development Process & Challenges

### Challenge 1: User Authentication System
- **Problem**: Implementing a secure token-based authentication system
- **Solution**: Built a secure authentication system using Django REST Framework and Token authentication

### Challenge 2: Profile Image Upload
- **Problem**: Implementing user profile image upload and management
- **Solution**: 
  - Backend: Implemented Django's file handling system with image optimization logic
  - Frontend: Used FormData API for multipart request handling

### Challenge 3: AI Chatbot Integration
- **Problem**: Developing a personalized game recommendation system
- **Solution**: Integrated external AI API and implemented user preference data analysis algorithms

## 🔮 Future Plans

- **Social Login**: Integration with Google, Facebook, and other social login providers
- **Multilingual Support**: Support for languages beyond English
- **Gaming Community**: Community features for user interaction
- **Mobile App**: Developing a mobile app using React Native

## 📝 License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Developer**: [Your Name]
- **Email**: [Your Email]
- **GitHub**: [Your GitHub Profile Link]
- **Portfolio**: [Your Portfolio Website]

---

⭐ If you like this project, please give it a star on GitHub! 