from http.client import responses
import pandas as pd
import json
import requests
import argparse
from datetime import datetime, timedelta
import openpyxl
from dateutil import relativedelta
from openpyxl.workbook import Workbook
from openpyxl.styles import PatternFill


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("csv_file", help="CSV-Datei mit Fahrzeugdaten")
    parser.add_argument("-k", "--keys", nargs="*", help="Zusätzliche Spalten")
    parser.add_argument("-c", "--colored", action="store_true", help="aktiviere farbliche Markierung")

    return parser.parse_args()


def send_csv_to_server(path: str) -> list[dict]:
    url = "http://localhost:8000/upload.csv/"
    with open(args.csv_file, "rb") as f:
        files = {"file": (path, f, "text/csv")}
        response = requests.post(url, files=files)

        return response.json()


def calculate_hu_age(hu: str) -> int:
   hu_datelist =  hu.split("-")
   hu_date = datetime(int(hu_datelist[0]), int(hu_datelist[1]), int(hu_datelist[2]))
   today = datetime.now()



def create_excel(additional_columns: list, tinted: bool, csv_data: list[dict]):
    wb = Workbook()
    ws = wb.active
    ws.title = "vehicles"
    column_names = ["rnr"]
    if additional_columns:
        column_names.extend(additional_columns)
    ws.append(column_names)

   # if tinted:
    #    red = PatternFill(start_color="#b30000", fill_type="solid")
     #   orange = PatternFill(start_color="#FFA500", fill_type="solid")
      #  green = PatternFill(start_color="#007500", fill_type="solid")

    for row in csv_data:
        row_data = [row.get("rnr")] + [row.get(col) for col in additional_columns]
        ws.append(row_data)

    wb.save(f"vehicles_{datetime.now().date().isoformat()}.xlsx")


if __name__ == "__main__":
    args = parse_args()

    print("CSV-Datei wird verarbeitet...")
    response = send_csv_to_server(args.csv_file)
    #dingen = json.dumps(response)


    df = pd.DataFrame(response)
    df = df.sort_values(by="gruppe")
    sorted_data = json.loads(df.to_json(orient="records", indent=2))
    test = json.dumps(sorted_data)


    create_excel(list(args.keys), args.colored, sorted_data)
    print(args.keys, args.colored)