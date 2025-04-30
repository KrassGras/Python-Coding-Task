
import json
import requests
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("csv_file", help="CSV-Datei mit Fahrzeugdaten")
parser.add_argument("-k", "--keys",  nargs="*", help="Zusätzliche Spalten")
parser.add_argument("-c", "--colored", action="store_true", help="aktiviere farbliche Markierung")

args = parser.parse_args()

url = "http://localhost:8000/upload.csv/"

print("CSV-Datei wird verarbeitet...")

with open(args.csv_file, "rb") as f:
    files = {"file": (args.csv_file, f, "text/csv")}
    response = requests.post(url, files=files)

dingen = json.dumps(response.json())






