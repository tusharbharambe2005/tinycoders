from flask import Flask, render_template, request, jsonify
import requests
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

OPENWEATHER_API_KEY = "8f21e65afed27942abb1bd163b173483"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}&units=metric"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)


def get_weather_data(lat, lon):
    try:
        url = WEATHER_API_URL.format(lat=lat, lon=lon, appid=OPENWEATHER_API_KEY)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        rainfall = data.get('rain', {}).get('1h', 0)  # Default to 0 if no rain data
        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'rainfall': rainfall
        }
    except requests.RequestException as e:
        return {'error': f"Failed to fetch weather data: {str(e)}"}


def get_seismic_data(lat, lon):
    seismic_activity = np.random.randint(0, 5)
    max_magnitude = np.random.uniform(0, 6) if seismic_activity > 0 else 0
    return {
        'seismic_activity': seismic_activity,
        'max_magnitude': max_magnitude
    }


def get_satellite_data(lat, lon):
    cloud_cover = np.random.uniform(0, 100)
    ndvi = np.random.uniform(-1, 1)
    return {
        'cloud_cover': cloud_cover,
        'ndvi': ndvi
    }


def train_model(features, labels):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model


def predict_disaster(features, model):
    features_array = features.values.reshape(1, -1)
    probabilities = model.predict_proba(features_array)
    predictions = model.predict(features_array)[0]

    advice = []
    if predictions[0]:  # Flood
        advice.append("Consider installing drainage systems and elevating crop beds.")
    if len(predictions) > 1 and predictions[1]:  # Earthquake
        advice.append("Secure farm equipment and buildings against seismic activity.")
    if len(predictions) > 2 and predictions[2]:  # Wildfire
        advice.append("Create firebreaks and maintain irrigation systems.")
    if not any(predictions):
        advice.append("Maintain regular farming practices; no immediate risks detected.")

    return {
        'flood': {'risk': bool(predictions[0]),
                  'probability': float(probabilities[0][0][1]) if len(probabilities[0][0]) > 1 else 0},
        'earthquake': {'risk': bool(predictions[1]) if len(predictions) > 1 else False,
                       'probability': float(probabilities[1][0][1]) if len(probabilities) > 1 and len(
                           probabilities[1][0]) > 1 else 0},
        'wildfire': {'risk': bool(predictions[2]) if len(predictions) > 2 else False,
                     'probability': float(probabilities[2][0][1]) if len(probabilities) > 2 and len(
                         probabilities[2][0]) > 1 else 0},
        'advice': advice
    }


# Global model variable
model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    return render_template('sign.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    return render_template('feedback.html')
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token}), 200
        
        return jsonify({'error': 'Invalid credentials'}), 400


@app.route('/get_disaster_data', methods=['POST'])
def get_disaster_data():
    global model
    try:
        data = request.get_json()
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({'error': 'Invalid request: latitude and longitude required'}), 400

        lat, lon = float(data['latitude']), float(data['longitude'])

        weather_data = get_weather_data(lat, lon)
        if 'error' in weather_data:
            return jsonify({'error': weather_data['error']}), 500

        seismic_data = get_seismic_data(lat, lon)
        satellite_data = get_satellite_data(lat, lon)

        features_dict = {**weather_data, **seismic_data, **satellite_data}
        features = pd.DataFrame([features_dict])

        if model is None:
            return jsonify({'error': 'Model not initialized'}), 500

        prediction = predict_disaster(features, model)

        return jsonify({
            'weather': weather_data,
            'seismic': seismic_data,
            'satellite': satellite_data,
            'prediction': prediction
        })
    except Exception as e:
        return jsonify({'error': f"Server error: {str(e)}"}), 500


if __name__ == '__main__':
    dummy_features = pd.DataFrame({
        'temperature': np.random.uniform(10, 40, 100),
        'humidity': np.random.uniform(20, 90, 100),
        'pressure': np.random.uniform(950, 1050, 100),
        'wind_speed': np.random.uniform(0, 20, 100),
        'rainfall': np.random.uniform(0, 50, 100),
        'seismic_activity': np.random.randint(0, 10, 100),
        'max_magnitude': np.random.uniform(0, 6, 100),
        'cloud_cover': np.random.uniform(0, 100, 100),
        'ndvi': np.random.uniform(-1, 1, 100)
    })
    dummy_labels = np.random.randint(0, 2, size=(100, 3))

    model = train_model(dummy_features, dummy_labels)

    app.run(debug=True, host='0.0.0.0', port=5001)