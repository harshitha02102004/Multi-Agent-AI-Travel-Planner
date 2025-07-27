from flask import Flask, request, jsonify, send_from_directory
import os
import requests
import random
from datetime import datetime, timedelta
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

# Initialize Flask
app = Flask(__name__, static_folder="static")

# Initialize LLM
llm = Ollama(model="llama3")

# ================= Configuration ===================
WEATHER_API_KEY = "281d069733d868936261f0d380df87bd"
AMADEUS_API_KEY = "9NYcXig6IF3Le2g5A3l9QkOsIdwTJYc7"
AMADEUS_API_SECRET = "GtreXeeAXoG4xBhv"

# IATA City Mapping
iata_mapping = {
    "Hyderabad": "HYD", "Goa": "GOI", "Delhi": "DEL", "Mumbai": "BOM", "Bangalore": "BLR",
    "Chennai": "MAA", "Kolkata": "CCU", "Ahmedabad": "AMD", "Jaipur": "JAI", "Pune": "PNQ"
}

# ============ Travel Logic Functions ==============

def fetch_weather_forecast(city, start_date, end_date, api_key):
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        forecast = {}
        cur = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        while cur <= end:
            date_str = cur.strftime("%Y-%m-%d")
            daily = [entry for entry in data["list"] if entry["dt_txt"].startswith(date_str)]
            if daily:
                avg_temp = round(sum(d["main"]["temp"] for d in daily) / len(daily), 1)
                desc = daily[0]["weather"][0]["description"]
                forecast[date_str] = f"{desc.title()}, {avg_temp}°C"
            else:
                forecast[date_str] = "No data"
            cur += timedelta(days=1)
        return "\n".join([f"{d}: {f}" for d, f in forecast.items()])
    except:
        return "❌ Could not fetch weather."

def get_amadeus_token():
    try:
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": AMADEUS_API_KEY,
            "client_secret": AMADEUS_API_SECRET
        }
        response = requests.post(url, data=data)
        return response.json()["access_token"]
    except:
        return None

def fetch_flights(source, destination, date, access_token):
    try:
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "originLocationCode": iata_mapping.get(source, source[:3].upper()),
            "destinationLocationCode": iata_mapping.get(destination, destination[:3].upper()),
            "departureDate": date,
            "adults": 1,
            "currencyCode": "INR",
            "max": 3
        }
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        results = []
        for offer in data.get("data", []):
            seg = offer["itineraries"][0]["segments"][0]
            airline = seg["carrierCode"]
            dep = seg["departure"]["at"]
            arr = seg["arrival"]["at"]
            price = offer["price"]["total"]
            results.append(f"✈ Airline: {airline}, Dep: {dep}, Arr: {arr}, Price: ₹{price}")
        return "\n".join(results) if results else "No flights found."
    except Exception as e:
        return f"❌ Could not fetch flights. Error: {str(e)}"

def suggest_itinerary(destination, days):
    prompt = PromptTemplate(
        input_variables=["destination", "days"],
        template="Create a detailed {days}-day travel itinerary for {destination}, India. One activity per day with short description."
    )
    chain = prompt | llm
    return chain.invoke({"destination": destination, "days": days})

def recommend_hotel(destination, nights, budget):
    per_night = budget // nights
    if per_night >= 6000:
        tier = "Luxury Hotel"
    elif per_night >= 3000:
        tier = "Mid-range Hotel"
    else:
        tier = "Budget Hotel"
    return f"🏨 {tier} in {destination} (~₹{per_night}/night)"

def budget_summary(flight, hotel, total):
    extras = total - flight - hotel
    return f"💸 Budget Summary:\n- Flight: ₹{flight}\n- Hotel: ₹{hotel}\n- Remaining for Food & Activities: ₹{extras}"

# =============== Flask Routes ===================

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/<path:filename>")
def serve_static_files(filename):
    return send_from_directory("static", filename)

@app.route("/plan", methods=["POST"])
def plan_trip():
    data = request.get_json()
    source = data.get("source")
    destination = data.get("destination")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    budget = int(data.get("budget"))

    nights = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
    flight_cost = int(0.4 * budget)
    hotel_cost = int(0.35 * budget)

    weather = fetch_weather_forecast(destination, start_date, end_date, WEATHER_API_KEY)
    access_token = get_amadeus_token()
    flight_data = fetch_flights(source, destination, start_date, access_token) if access_token else "Token fetch failed."
    itinerary = suggest_itinerary(destination, nights)
    hotel = recommend_hotel(destination, nights, hotel_cost)
    summary = budget_summary(flight_cost, hotel_cost, budget)

    return jsonify({
        "weather": weather,
        "flights": flight_data,
        "itinerary": itinerary,
        "hotel": hotel,
        "summary": summary
    })

if __name__ == "__main__":
    app.run(debug=True)



