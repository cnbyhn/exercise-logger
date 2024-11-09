
import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants from environment variables
APP_ID = os.getenv("NUTRITIONIX_APP_ID")
API_KEY = os.getenv("NUTRITIONIX_API_KEY")
SHEETY_ENDPOINT = os.getenv("SHEETY_WORKOUT_URL")

# Collect user input for exercise data
GENDER = input("Your gender: ")
WEIGHT_KG = input("Your weight (kg): ")
HEIGHT_CM = input("Your height (cm): ")
AGE = input("Your age: ")
EXERCISE = input("What exercise did you do today? ")
Time = input("When did you start? ")

today = time.localtime()
current_date_time = time.strftime("%d/%m/%Y", today)

# Nutritionix API request
params = {
    "query": EXERCISE,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
headers = {
    'Content-Type': 'application/json',
    'x-app-id': APP_ID,
    'x-app-key': API_KEY
}

try:
    response = requests.post(
        'https://trackapi.nutritionix.com/v2/natural/exercise',
        json=params,
        headers=headers
    )
    response.raise_for_status()
    details = response.json()

    # Loop through exercises and log each to Sheety
    for exercise in details["exercises"]:
        ex_params = {
            "workout": {
                "exercise": exercise["user_input"].title(),
                "date": current_date_time,
                "time": Time,
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
        }
        response2 = requests.post(SHEETY_ENDPOINT, json=ex_params)
        response2.raise_for_status()
        print(response2.text)

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
