# Multi-Agent-AI-Travel-Planner
# 🌍 Multi-Agent AI Travel Planner Web App

An intelligent, personalized travel planner powered by LangChain, Ollama (LLaMA), and multiple real-time APIs. This project dynamically generates full travel itineraries—including flights, weather, activities, and hotels—based on user preferences using a multi-agent architecture.

---

## ✨ Features

- Multi-Agent System: Each agent specializes in planning weather, flights, hotels, or activities.
- Dynamic Location-Based Activities: Suggested by the LLaMA model running on Ollama, replacing hardcoded data.
- Weather Integration: Real-time weather reports for travel dates using **OpenWeather API**.
- Live Flights: Fetches flights (airlines, timings, prices) using **Amadeus API**.
- Hotel Booking Suggestions: Shows real-time, budget-friendly options using hotel APIs.
- Web Interface: Simple UI built with **HTML, JavaScript, and Flask** backend.

---

## Tech Stack

| Layer         | Tools Used                                |
|---------------|--------------------------------------------|
| Frontend      | HTML, JavaScript                          |
| Backend       | Python, Flask                             |
| AI Agent      | LangChain, LangGraph, Ollama (LLaMA model)|
| APIs Used     | OpenWeather API, Amadeus API, Hotel APIs  |

---

##  Project Structure

travel_planner/
├── static/
│ └── style.css (optional)
├── templates/
│ └── index.html
├── app.py # Flask backend
├── agents/
│ ├── flight_agent.py
│ ├── hotel_agent.py
│ ├── activity_agent.py
│ └── weather_agent.py
├── utils/
│ └── api_helpers.py
├── requirements.txt
└── README.md
