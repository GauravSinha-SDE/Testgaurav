import pandas as pd
import json
import math

dataframe = pd.read_csv("merged_travel_dataset.csv")
dataframe.columns = [column.strip() for column in dataframe.columns]


def normalize_value(value, fallback=None):
    if pd.notna(value):
        string_value = str(value).strip()
        if string_value:
            return string_value
    return fallback


def normalize_duration(duration_value):
    try:
        return float(duration_value)
    except Exception:
        return 3.0


def build_itinerary_example(city, budget, duration_days, trip_type, interest):
    total_days = max(1, min(int(math.ceil(duration_days)), 10))
    title = f"{total_days}-Day {trip_type or 'Trip'} plan to {city or 'destination'} (Budget: {budget or 'Unspecified'})"
    summary = (
        f"This is a {trip_type or 'general'} itinerary for {city or 'destination'}. "
        f"Focus: {interest or 'General activities'}. Duration: {duration_days} day(s)."
    )

    day_entries = []
    for day_index in range(1, total_days + 1):
        arrival_text = (
            "Arrive morning; local transfer suggestions." if day_index == 1 else "Arrive morning (start of day)."
        )
        departure_text = (
            "Depart late evening or as per user's schedule." if day_index == total_days else "Overnight stay; no long-distance departure."
        )
        morning_text = f"Morning: Activity aligned with {interest or 'local highlights'} (~Rs 100-500)."
        afternoon_text = "Afternoon: Continue attractions or local experiences; consider transit time."
        evening_text = "Evening: Dine or relax; suggest local cuisine/markets."
        day_entries.append(
            {
                "day": day_index,
                "arrival": arrival_text,
                "departure": departure_text,
                "morning": morning_text,
                "afternoon": afternoon_text,
                "evening": evening_text,
            }
        )

    tips = [
        "Use public transport or shared transfers for budget-friendly options.",
        "Book tickets or slots in advance where possible.",
        "Adjust start times for local sunrise/sunset for viewpoint visits.",
    ]
    daily_budget_estimate = (
        "Daily budget estimate: depends on tier; ballpark Rs ~2000/day for budget."
    )

    text_output = title + "\n\n" + summary + "\n\n"
    for itinerary in day_entries:
        text_output += (
            f"Day {itinerary['day']}:\n"
            f"- Arrival: {itinerary['arrival']}\n"
            f"- Departure: {itinerary['departure']}\n"
            f"- Morning: {itinerary['morning']}\n"
            f"- Afternoon: {itinerary['afternoon']}\n"
            f"- Evening: {itinerary['evening']}\n\n"
        )

    text_output += "Tips:\n" + "\n".join([f"- {tip}" for tip in tips]) + f"\n\n{daily_budget_estimate}\n"
    return text_output


jsonl_records = []
for _, row in dataframe.iterrows():
    user_query = normalize_value(row.get("query"), fallback="Example travel query")
    city = normalize_value(row.get("City"), fallback="Unknown destination")
    trip_type = normalize_value(row.get("Trip_type"), fallback="General")
    interest = normalize_value(row.get("interest"), fallback="General activities")
    budget = normalize_value(row.get("Budget"), fallback="Unspecified")
    duration = normalize_duration(row.get("Duration"))

    assistant_response = build_itinerary_example(city, budget, duration, trip_type, interest)

    record = {
        "messages": [
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": assistant_response},
        ]
    }
    jsonl_records.append(record)

with open("travel_dataset.jsonl", "w", encoding="utf-8") as file_handle:
    for record in jsonl_records:
        file_handle.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Wrote {len(jsonl_records)} records to travel_dataset.jsonl")
