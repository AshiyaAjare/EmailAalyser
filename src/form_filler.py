import requests
import os
from dotenv import load_dotenv

load_dotenv()
FORM_ID = os.getenv("GOOGLE_FORM_ID")


def submit_google_form(data):
    url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSdwEaNonHSBaXgj3S-q2jI2lAMy0zisLM5FmMQb2UAB6M5PHg/formResponse"
    
    try:
        year, month, day = data["Date"].split("-")
        hour, minute = data["Time"].replace("AM", "").replace("PM", "").strip().split(":")
        hour = hour.strip()
        minute = minute.strip()
    except Exception as e:
        print("Failed to parse date/time:", e)
        return

    payload = {
        "entry.728978152": data["Trainer Name"],
        "entry.1009152001": data["Session Topic"],
        "entry.1244989651_year": year,
        "entry.1244989651_month": month,
        "entry.1244989651_day": day,
        "entry.1664988921_hour": hour,
        "entry.1664988921_minute": minute,
        "entry.270111561": data["Duration"],
        "entry.46448066": data["Mode"]
    }

    response = requests.post(url, data=payload)
    print("Submitting payload:", payload)
    print("Status:", response.status_code)
    print("Response text:", response.text)