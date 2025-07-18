# Agricure: AI-Powered Plant Disease Diagnosis and Recommendation System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Agricure is a comprehensive web application designed to assist farmers and agronomists in diagnosing plant diseases through image analysis. It leverages a deep learning model for accurate disease identification and integrates with the Google Gemini API to provide tailored treatment and prevention recommendations based on local weather conditions.

## 🌟 Key Features

-   **Multi-User Roles:** Separate interfaces and functionalities for Farmers, Agronomists, and Administrators.
-   **AI-Powered Diagnosis:** Upload or capture a plant leaf image to get an instant diagnosis using a pre-trained TensorFlow/Keras model (EfficientNet).
-   **Dynamic AI Recommendations:** Generates actionable treatment and prevention advice using Google's Gemini API, enhanced with live weather data from OpenWeatherMap.
-   **Personalized Dashboards:**
    -   **Farmers:** View diagnosis history, crop health scores, and urgent alerts.
    -   **Agronomists:** Access farmer data, upload datasets, and monitor agricultural activities.
    -   **Admin:** System-wide analytics and user management.
-   **Interactive Chat:** Enables direct communication between farmers and agronomists for expert consultation.
-   **Diagnosis & Upload History:** Track all past diagnoses and file uploads.
-   **Reporting:** Agronomists can generate and email summary reports.

## 🛠️ Technology Stack

-   **Backend:** Python, Django
-   **Frontend:** HTML, CSS, JavaScript, Bootstrap
-   **Database:** PostgreSQL
-   **AI & Machine Learning:**
    -   TensorFlow & Keras for the disease classification model.
    -   Google Gemini API for generating recommendations.
-   **APIs:** OpenWeatherMap API for real-time weather data.
-   **Deployment:** (Assumed) Docker, Gunicorn, Nginx.

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python 3.9+
-   PostgreSQL
-   Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Agricure-2.git
    cd Agricure-2/Agricure
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    *(Note: A `requirements.txt` file is recommended. Create one using `pip freeze > requirements.txt`)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the `Agricure/` directory (where `settings.py` is located) and add the following variables:
    ```env
    # Django
    SECRET_KEY='your-django-secret-key'
    DEBUG=True

    # Database (PostgreSQL)
    DB_ENGINE='django.db.backends.postgresql'
    DB_NAME='postgres'
    DB_USER='your_db_user'
    DB_PASSWORD='your_db_password'
    DB_HOST='localhost'
    DB_PORT='5432'

    # Google Gemini API
    GEMINI_API_KEY='your-gemini-api-key'

    # OpenWeatherMap API
    OPENWEATHER_API_KEY='your-openweathermap-api-key' # (Assuming this is needed for WeatherClient)

    # Email (for password reset, etc.)
    EMAIL_HOST_USER='your-email@gmail.com'
    EMAIL_HOST_PASSWORD='your-gmail-app-password'
    ```

5.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000`.

## 📂 Project Structure

The project is organized into several Django apps:

-   `/users`: Manages user accounts, authentication, roles (Farmer, Agronomist, Admin), and profiles.
-   `/diagnosis`: Handles image uploads, camera captures, and the core AI model prediction logic.
-   `/recommendations`: Integrates with the Gemini API and OpenWeatherMap to generate and store agricultural advice.
-   `/agronomist`: Contains views and templates for the agronomist-specific dashboard and tools.
-   `/chat`: Implements the real-time chat functionality between users.
-   `/analytics`: Powers the admin dashboard with system-wide statistics.
-   `/administrator`: Manages admin-specific tasks like dataset uploads.

## 🤝 Contributors

Based on the project's source code, the key contributors are:

-   **sseluyindaeva** (Lead Developer)
-   **ayanhilwa** (Contributor)

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.