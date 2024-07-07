#!/usr/local/bin/python3


from pandas import DataFrame
import requests
from datetime import datetime
import os

import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename


def scrap_verivox() -> str:
    url = "https://service.verivox.de/applications/thg/api/products"

    r = requests.get(url)
    data = r.json()

    df = DataFrame(columns=["Datum", "Uhrzeit", "Provider_id", "Provider", "Preis", "Bezahlmodel", "raw_data"])

    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    Datum = datetime.now().strftime("%Y/%m/%d")
    Uhrzeit = datetime.now().strftime("%H:%M")

    for i in data:

        provider = i["provider"]["name"]
        provider_id = i["provider"]["id"]
        payoutmodel = i["apiData"]["payoutModel"]
        try:
            price = i["payout"]
        except:
            price = 0
        raw_data = i

        x = len(df)

        df.loc[x, :] = [Datum, Uhrzeit, provider_id, provider, price, payoutmodel, raw_data]

    if not os.path.exists(os.path.join(os.getcwd(), 'files_to_db')):
        os.mkdir(os.path.join(os.getcwd(), 'files_to_db'))

    filepath = os.path.join(os.getcwd(), 'files_to_db', f"{now}_THG-Quote-Verivox.csv")
    df.to_csv(filepath, index=False, encoding='UTF-8')

    return filepath


def send_mail(receiver_email, filename):
    smtp_server = "securesmtp.t-online.de"
    port = 465
    sender_email = None # here mail address
    password = None # here password

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = '; '.join(receiver_email)
    message["Subject"] = "Verivox Preise"

    # Add body to email
    body = """Here's your daily Verivox data
    """

    message.attach(MIMEText(body, "plain"))

    with open(filename, "r") as f:
        attachment = MIMEApplication(f.read(), Name=basename(filename))
        attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
    message.attach(attachment)

    try:
        # Create a secure SSL context
        context = ssl.create_default_context()

        server = smtplib.SMTP_SSL(smtp_server, port, context=context)
        server.login(sender_email, password)
        server.send_message(message, sender_email, receiver_email)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()


if __name__ == '__main__':
    receiver_email = [''] # here all receiver mail addresses

    filename = scrap_verivox()

    send_mail(receiver_email=receiver_email, filename=filename)
    os.remove(filename)
