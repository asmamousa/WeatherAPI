# WeatherAPI

A **Django-based Weather API Wrapper Service** that fetches weather data from a third-party provider, caches responses, and exposes a clean API for clients.

This project is built as a solution for the **Weather API Wrapper Service** assignment from **roadmap.sh**:  
https://roadmap.sh/projects/weather-api-wrapper-service

---

## ✨ Features

- 🌍 Get weather data by city name
- 🔐 Uses environment variables for API keys and secrets
- ⚡ Caching to improve performance and reduce external API usage
- 🛑 Proper error handling for invalid input and API failures
- 🧩 Clean and extensible Django project structure

---
## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/asmamousa/WeatherAPI.git
cd WeatherAPI
```

### 2. Create & activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment variables

Create a `.env` file in the project root:

```env
WEATHER_API_KEY=your_weather_api_key
```

---

## ▶️ Run the Project

```bash
python manage.py migrate
python manage.py runserver
```

---

## 📡 API Usage

### Get Weather by City

```
GET /weather/?city=London
```

---

## 🧪 Caching

- Weather data is cached per city
- Improves performance and limits API calls

