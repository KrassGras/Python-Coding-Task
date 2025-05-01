import csv
import io
import json
from http.client import HTTPException, responses
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.openapi.utils import status_code_ranges
app = FastAPI()

#URLs for the external API for the vehicle data
VEHICLE_URL = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
AUTH_URL = "https://api.baubuddy.de/index.php/login"
LABEL_API_URL = "https://api.baubuddy.de/dev/index.php/v1/labels/"


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
    returns: accesstoken (str)
    """
    response = requests.post(AUTH_URL, json=AUTH_payload, headers=AUTH_headers)

    if response.status_code == 200:
        return response.json()["oauth"]["access_token"]
    else:
        raise HTTPException("Autentification Failed")

def get_vehicle_data(token: str) -> list[dict]:
    """
    Expects a token to request the vehicle data
    returns: the vehicle data content as a list of dictonaries
    """

    headers = {
        "Authorization" : f"Bearer {token}"
    }

    response = requests.get(VEHICLE_URL, headers=headers)

    if response.status_code == 200:
       return response.json()
    else:
        raise HTTPException(f"Failed to fetch vehicle data {response.text}")


def get_label_data(token, csv_data) -> list[dict]:
    """
    Enriches each row of the given csv data with the color of the first assigned label.
    args: token (str)
          csv_data (list[dict])
    returns: enriched csv_data with the added ColorCode (list[dict])
    """

    headers = {
        "Authorization": f"Bearer {token}"
    }
    for row in csv_data:
        labelid = row.get("labelIds")
        if labelid:
            firstlabelId = labelid.split(",")[0]
            response = requests.get(f"{LABEL_API_URL}{firstlabelId}", headers=headers)
            if response.status_code == 200:
                data = response.json()

                color_code = data[0].get("colorCode")
                row["ColorCode"] = color_code
            else:
                row["ColorCode"] = "none"

    return csv_data

@app.post("/upload.csv/")
async def upload_csv(file: UploadFile = File(...)) -> list[dict]:
    """
    Receives a CSV-file, read the content and returns the data as a list of dictonaries
    arguments: file: the uploaded CSV-file
    returns: filtered_data as a list of dictionaries where each dictionary represents a row of the csv file
    """
    content = await file.read()
    decoded_content = content.decode("utf-8")
    csv_file = io.StringIO(decoded_content)
    reader = csv.DictReader(csv_file, delimiter=";")
    csv_data = list(reader)
    csv_data = enrich_with_vehicle_data(csv_data, get_vehicle_data(get_acces_token()))
    filtered_data = [d for d in csv_data if d.get("hu") is not None]


    return filtered_data

def enrich_with_vehicle_data(csv_data: list, api_data: list) -> list[dict]:
    """
    Expects csv_data and api_data both as a list of dictonaries, merges them together based on
    the column kurzname and then returns it as a list of dictonaries
    arguments: csv_data, api_data (list of dictionaries)
    returns: csv_data (list of dictionaries) as the merged product
    """

    api_lookup = {item["kurzname"] : item for item in api_data}

    for row in csv_data:
        kurzname = row.get("kurzname")
        if kurzname in api_lookup:
            row.update(api_lookup[kurzname])

    csv_data = get_label_data(get_acces_token(), csv_data)

    return csv_data





