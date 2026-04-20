import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
FINE_TUNED_MODEL = os.getenv(
    "FINE_TUNED_MODEL",
    "ft:gpt-3.5-turbo-0613:your-org:travel-bot:abcd1234",
)

app = Flask(__name__)
CORS(app)


def extract_details(query):
    if not query.strip():
        return {
            "city": "Unspecified",
            "duration": "Unspecified",
            "budget": "Unspecified",
            "trip_type": "Unspecified",
            "interest": "Unspecified",
        }

    city = None
    match_city = re.search(r"\bto\s+([A-Za-z &\-\']+)", query)
    if match_city:
        city = match_city.group(1).split(",")[0].strip()

    match_duration = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:-?\s*(\d+(?:\.\d+)?))?\s*days?",
        query.lower(),
    )
    duration = match_duration.group(1) if match_duration else "Unspecified"

    match_budget = re.search(r"(?:rs\s*[\d,]+(?:\s*-\s*[\d,]+)?)", query.lower())
    budget = match_budget.group(0) if match_budget else "Unspecified"

    interests_found = [
        keyword
        for keyword in [
            "ski",
            "spa",
            "trek",
            "hike",
            "temple",
            "beach",
            "adventure",
            "nature",
            "shopping",
            "food",
            "family",
            "honeymoon",
            "eco",
            "wildlife",
            "museum",
        ]
        if keyword in query.lower()
    ]
    interest = ", ".join(interests_found) if interests_found else "Unspecified"

    trip_type = "Unspecified"
    match_trip = re.search(
        r"((?:luxur(?:y|ious)|honeymoon|eco[- ]?friendly|backpack(?:ing)?|family|budget|business|romantic|solo)[^\.,;]*)",
        query.lower(),
    )
    if match_trip:
        trip_type = match_trip.group(1).strip()

    return {
        "city": city or "Unspecified",
        "duration": duration,
        "budget": budget,
        "trip_type": trip_type,
        "interest": interest,
    }


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(force=True, silent=True) or {}
    user_query = (payload.get("query") or "").strip()
    if not user_query:
        return jsonify(
            {
                "trip_plan": "No query provided. Example: 'Plan me a 3-day nature trip to Manali with Rs 10000'."
            }
        )

    details = extract_details(user_query)

    prompt = f"""
User query:
{user_query}

Extracted fields:
City: {details['city']}
Duration: {details['duration']}
Budget: {details['budget']}
Trip Type: {details['trip_type']}
Interests: {details['interest']}

Instructions:
- Generate a full structured itinerary.
- Include Title, Summary, Day-wise (Arrival, Departure, Morning, Afternoon, Evening).
- Include Tips and daily budget estimate.
- Reflect free-text trip_type & interest. Do NOT map to fixed categories.
"""

    response = openai.ChatCompletion.create(
        model=FINE_TUNED_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a travel assistant trained to output structured itineraries.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=900,
    )

    answer = response.choices[0].message["content"].strip()
    return jsonify({"trip_plan": answer})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
