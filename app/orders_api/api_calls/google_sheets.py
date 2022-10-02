import os
import gspread
import datetime
# noinspection PyPackageRequirements
from google.oauth2 import service_account
from pathlib import Path
from django.conf import settings


def get_sheet_data():
    """Собираем данные с Google Sheets, проверяем и возвращаем в виде словаря"""
    # Подключаемся к Google Service Client
    secrets_path = os.path.join(Path(__file__).resolve().parent, 'some_random_file.json')
    credentials = service_account.Credentials.from_service_account_file(secrets_path, scopes=settings.SCOPES)
    client = gspread.authorize(credentials)

    sheet = client.open(settings.SPREADSHEET_NAME).sheet1
    data = {}
    for items in sheet.get("A2:D"):
        try:  # Если не хватает данных или не получилось конвертировать в нужный формат, то пропускаем
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

