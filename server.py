import io
from http.client import HTTPException
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.openapi.utils import status_code_ranges

app = FastAPI()

#URLs for the external API for the vehicle data
VEHICLE_URL = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
AUTH_URL = "https://api.baubuddy.de/index.php/login"
LABEL_API_URL = "https://api.baubuddy.de/dev/index.php/v1/labels"


#Authentificationdata
AUTH_payload = {
    "username": "365",
    "password": "1"
}
AUTH_headers = {
    "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
    "Content-Type": "application/json"
}

def get_acces_token() -> str:
    """
    Sends a request to get the token
    returns: accessstoken (str)
    """
    response = requests.post(AUTH_URL, json=AUTH_payload, headers=AUTH_headers)

    if response.status_code == 200:
        return response.json()["oauth"]["access_token"]
    else:
        raise HTTPException("Autentification Failed")

def get_vehicle_data(token: str) -> dict:
    """
    Expects a token to request the vehicle data
    returns: dicts: The vehicle data in a Python dictionary format (parsed JSON response)
    """

    headers = {
        "Authorization" : f"Bearer {token}"
    }

    response = requests.get(VEHICLE_URL, headers=headers)

    if response.status_code == 200:
       return response.json()
    else:
        raise HTTPException(f"Failed to fetch vehicle data {response.text}")


@app.post("/upload.csv/")
async def upload_csv(file: UploadFile = File(...)):
    pass










