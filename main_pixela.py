
import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants from environment variables
TOKEN = os.getenv("PIXELA_TOKEN")
USERNAME = os.getenv("PIXELA_USERNAME")
GRAPH_ID = os.getenv("PIXELA_GRAPH_ID")

# Current date in the required format
today = time.localtime()
current_date_time = time.strftime("%Y%m%d", today)

pixelea_endpoint = "https://pixe.la/v1/users"

# User account creation parameters (only needed once)
user_params = {
  "token": TOKEN,
  "username": USERNAME,
  "agreeTermsOfService": "yes",
  "notMinor": "yes",
}

# Graph creation parameters (only needed once)
graph_params = {
  "id": GRAPH_ID,
  "name": "Python Study",
  "unit": "hour",
  "type": "float",
  "color": "sora",
  "timezone": "Asia/Istanbul"
}
headers = {
  "X-USER-TOKEN": TOKEN
}

graph_endpoint = f"{pixelea_endpoint}/{USERNAME}/graphs"

# Input study hours and convert minutes to hours
try:
    study_hours = str(float(input("How long did you study? (Minutes) ")) / 60)
    graph_update = {
        "date": current_date_time,
        "quantity": study_hours
    }

    graph_update_endpoint = f"{pixelea_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
    response = requests.post(url=graph_update_endpoint, json=graph_update, headers=headers)
    response.raise_for_status()
    print(response.text)

except ValueError:
    print("Error: Please enter a valid number of minutes.")
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
