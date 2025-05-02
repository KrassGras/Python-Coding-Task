# Vehicle Data Enricher

This project is part of a coding task for a working student position in Python development.

It consists of:
- A FastAPI server that enriches vehicle data from a CSV file using the BauBuddy API and then returns the filtered, enriched csv_data as jsonstring
- A Python client that sends the CSV to the Server-API via POST-call, processes the response, and exports it as a formatted Excel file

## Usage

1. Start the server:
   ```bash
   uvicorn server:app --reload
   ```

2. Run the client:
   ```bash
   python client.py vehicles.csv -k kurzname gruppe hu -c
   ```

Options:
- `-k`: additional columns to include
- `-c`: enable color formatting based on HU age

## Structure

- `server.py` – FastAPI backend
- `client.py` – CLI tool to send CSV and create Excel


---


  
 
