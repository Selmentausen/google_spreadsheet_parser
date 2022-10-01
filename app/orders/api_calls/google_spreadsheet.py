import os
import gspread
import datetime
# noinspection PyPackageRequirements
from google.oauth2 import service_account
from pathlib import Path


def get_spreadsheet_data():
    scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file",
              "https://www.googleapis.com/auth/spreadsheets"]
    secrets_path = os.path.join(Path(__file__).resolve().parent, 'service_client_secret.json')
    credentials = service_account.Credentials.from_service_account_file(secrets_path, scopes=scopes)
    client = gspread.authorize(credentials)
    sheet = client.open(os.environ.get('SPREADSHEET_NAME', 'test_data')).sheet1

    data = {}
    for items in sheet.get("A2:D"):
        try:  # if fail to gather and convert data from a line then skip the line
            item_id, order_id, usd_cost, delivery_date = items
            item_id = int(item_id)
            usd_cost = float(usd_cost)
            delivery_date = datetime.date(*reversed(list(map(int, delivery_date.split('.')))))
        except ValueError:
            continue
        except TypeError:
            continue
        data[item_id] = {'order_id': order_id, 'usd_cost': usd_cost, 'delivery_date': delivery_date}
    return data

