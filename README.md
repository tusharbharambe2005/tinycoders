# 🌍 Disaster Prediction Web App

This project is a Flask-based web application that predicts the risk of natural disasters (flood, earthquake, wildfire) based on live weather data, simulated seismic and satellite data. It includes user authentication and token-based API access.

🔗 **GitHub Repository**: [tinycoders](https://github.com/tusharbharambe2005/tinycoders.git)

---

## 🚀 Features

- 🌦 Fetches real-time **weather data** from OpenWeatherMap API
- 🌋 Simulates **seismic** and **satellite** data
- 🔍 Uses **Machine Learning (Random Forest Classifier)** to predict:
  - Flood
  - Earthquake
  - Wildfire
- 🛡 User registration and login using **JWT Authentication**
- 📄 Webpages: Home, Login, Register, About, Feedback

---

## 📁 Project Structure

tinycoders/ │ ├── templates/ 
                  # HTML files (index.html, login.html, sign.html, etc.) 
              ├── app.py # Main Flask application 
              ├── users.db # SQLite database (auto-created) 
              ├── requirements.txt # Python dependencies 
              └── README.md # Project documentation

---

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tusharbharambe2005/tinycoders.git
   cd tinycoders
2. **Create a virtual environment (optional but recommended):**
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies: //comming soon file...
   ```bash
   pip install -r requirements.txt
4. Run the app:
   ```bash
   python app.py

🔑 API Endpoints
Endpoint	          Method	      Description
/register	          POST	        Register a new user
/login	            POST        	Login and get JWT token
/get_disaster_data	POST	        Send lat/lon and get disaster prediction

🧠 Machine Learning
+ A dummy dataset is created using random values to train a Random Forest model.
+ Predictions are made on incoming data from OpenWeather and simulated sensors.
+ Output includes disaster risks and advice.

🔒 User Authentication
+ Users can register and login.
+ Passwords are hashed using Bcrypt.
+ JWT tokens are generated for secure access to protected routes.

🌐 Pages
/ - Home
/login - Login Page
/sign - Signup Page
/about - About Project
/feedback - Feedback Form

📬 Contact
Created by Tushar Bharambe
GitHub: @tusharbharambe2005
