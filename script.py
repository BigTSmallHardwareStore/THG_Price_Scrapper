#!/usr/bin/env python
import requests
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, inspect
import json
import time
import os


db_path = os.getenv("PATH_TO_DB", "verivox_thg.db")

# Create an engine that connects to the SQLite database
engine = create_engine(f'sqlite:///{db_path}')

# Initialize metadata
metadata = MetaData()


thg = Table(
    'thg', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('Datum', Text),
    Column('Uhrzeit', Text),
    Column('Provider_id', Integer),
    Column('Provider', Text),
    Column('Preis', Integer),
    Column('Bezahlmodel', Text),
    Column('Eigenschaft', Text),
    Column('raw_data', Text)
)


inspector = inspect(engine)
if not inspector.has_table(thg.name):
    # Create the table
    metadata.create_all(engine, tables=[thg])


url = "https://service.verivox.de/applications/thg/api/products"

while True:
    try:
        response = requests.get(url)
        data = response.json()
        break
    except:
        time.sleep(300)


Datum = datetime.now().strftime("%Y-%m-%d")
Uhrzeit = datetime.now().strftime("%H:%M")


with engine.connect() as connection:
    for i in data:

        provider = i["provider"]["name"]
        provider_id = i["provider"]["id"]
        payoutmodel = i["apiData"]["payoutModel"]
        price = i.get("payout", 0)

        raw_data = json.dumps(i)

        feature = ', '.join(
            [i['value'] for i in data[0]['keyMetrics'] if "Auszahlung " in i['value']])

        json_data = {
            "Datum": Datum,
            "Uhrzeit": Uhrzeit,
            "Provider_id": provider_id,
            "Provider": provider,
            "Preis": price,
            "Bezahlmodel": payoutmodel,
            "Eigenschaft": feature,
            "raw_data": raw_data,
        }

        insert_statement = thg.insert().values(**json_data)
        connection.execute(insert_statement)

    connection.commit()
