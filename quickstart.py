import gspread
import psycopg2
import xml.etree.ElementTree as ET
import requests
import schedule
import time

# noinspection PyPackageRequirements
from google.oauth2 import service_account


def update_currency_exchange():
    global USD_TO_RUB_EXCHANGE_RATE
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    if not response:
        return
    with open(CURRENCY_EXCHANGE_FILE_PATH, 'wb') as f:
        f.write(response.content)
    USD_TO_RUB_EXCHANGE_RATE = get_usd_to_rub_exchange()


def get_usd_to_rub_exchange():
    tree = ET.parse(CURRENCY_EXCHANGE_FILE_PATH)
    root = tree.getroot()
    item = root.find("./Valute/[@ID='R01235']/Value")
    return float(item.text.replace(',', '.'))


def get_data_from_google_sheets(sheet):
    return {int(item_id): {'order_id': int(order_id), 'usd_cost': int(usd_cost), 'delivery_date': delivery_date}
            for item_id, order_id, usd_cost, delivery_date in sheet.get("A2:D")}


def get_data_from_db(cursor):
    cursor.execute("SELECT * FROM orders")
    return {item_id: {'order_id': order_id, 'usd_cost': usd_cost, 'rub_cost': rub_cost,
                      'delivery_date': delivery_date.strftime('%d.%m.%Y')}
            for item_id, order_id, usd_cost, rub_cost, delivery_date in cursor.fetchall()}


def convert_usd_to_rub(usd):
    return float(usd) * USD_TO_RUB_EXCHANGE_RATE


def update_db():
    conn = psycopg2.connect(database='test_case_db', user='postgres', password='admin123', host='127.0.0.1',
                            port='5432')
    cursor = conn.cursor()
    sheet = client.open('test_data').sheet1
    google_sheets_data = get_data_from_google_sheets(sheet)
    db_data = get_data_from_db(cursor)
    for item_id, values in google_sheets_data.items():
        if item_id in db_data:
            # google data is not subset of db data, then update data
            if not set(google_sheets_data[item_id].values()) <= set(db_data[item_id].values()):
                cursor.execute(f"""UPDATE orders 
SET order_id={values['order_id']},
usd_cost={values['usd_cost']},
rub_cost={convert_usd_to_rub(values['usd_cost'])}, 
delivery_date=TO_DATE('{values['delivery_date']}', 'DD.MM.YYYY')
WHERE id={item_id}""")
                print(f'changed order {values["order_id"]}')
            del db_data[item_id]
        else:
            cursor.execute(
                f"""INSERT INTO orders
VALUES ({item_id}, {values['order_id']}, {values['usd_cost']}, {convert_usd_to_rub(values['usd_cost'])},
TO_DATE('{values['delivery_date']}', 'DD.MM.YYYY'))""")
            print(f'added order {values["order_id"]}')
    if db_data:
        cursor.execute(f"""DELETE FROM orders WHERE id IN ({', '.join(map(str, db_data.keys()))})""")
        print(f'deleted next orders {", ".join(map(lambda v: str(v["order_id"]), db_data.values()))}')
    conn.commit()
    conn.close()
    print('database update finished!')


if __name__ == '__main__':
    SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file",
              "https://www.googleapis.com/auth/spreadsheets"]
    CURRENCY_EXCHANGE_FILE_PATH = 'currency_exchange.xml'
    USD_TO_RUB_EXCHANGE_RATE = get_usd_to_rub_exchange()
    credentials = service_account.Credentials.from_service_account_file('service_client_secret.json', scopes=SCOPES)
    client = gspread.authorize(credentials)

    schedule.every().day.at('00:00').do(update_currency_exchange)
    schedule.every(5).minutes.do(update_db)

    running = True
    while running:
        schedule.run_pending()
        time.sleep(1)
