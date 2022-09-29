import gspread
import psycopg2
import xml.etree.ElementTree as ET
import requests

# noinspection PyPackageRequirements
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file",
          "https://www.googleapis.com/auth/spreadsheets"]

conn = psycopg2.connect(database='test_case_db', user='postgres', password='admin123', host='127.0.0.1', port='5432')
cursor = conn.cursor()


def update_currency_file():
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    with open('currency_exchange.xml', 'wb') as f:
        f.write(response.content)


def get_usd_to_rub_exchange(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    item = root.find("./Valute/[@ID='R01235']/Value")
    return float(item.text.replace(',', '.'))


def get_data_from_google_sheets(sheet):
    return {int(order_id): {'usd_cost': int(usd_cost), 'delivery_date': delivery_date}
            for _, order_id, usd_cost, delivery_date in sheet.get("A2:D")}


def get_data_from_db():
    cursor.execute("SELECT * FROM orders")
    return {order_id: {'usd_cost': usd_cost, 'rub_cost': rub_cost, 'delivery_date': delivery_date}
            for _, order_id, usd_cost, rub_cost, delivery_date in cursor.fetchall()}


def convert_usd_to_rub(usd):
    return float(usd) * usd_to_rub_exchange


def update_db(sheet):
    google_sheets_data = get_data_from_google_sheets(sheet)
    db_data = get_data_from_db()
    for order_id, values in google_sheets_data.items():
        if order_id in db_data:
            cursor.execute(f"""UPDATE orders 
SET usd_cost={values['usd_cost']},
rub_cost={convert_usd_to_rub(values['usd_cost'])}, 
delivery_date=TO_DATE('{values['delivery_date']}', 'DD.MM.YYYY')
WHERE order_id={order_id}""")
            del db_data[order_id]
        else:
            cursor.execute(
                f"""INSERT INTO orders (order_id, usd_cost, rub_cost, delivery_date)
VALUES ({order_id}, {values['usd_cost']}, {convert_usd_to_rub(values['usd_cost'])},
TO_DATE('{values['delivery_date']}', 'DD.MM.YYYY'))""")
            print(f'added order {order_id}')
    if db_data:
        cursor.execute(f"""DELETE FROM orders WHERE order_id IN ({', '.join(map(str, db_data.keys()))})""")
        print(f'deleted next orders {", ".join(map(str, db_data.keys()))}')
    conn.commit()


# update_currency_file()
credentials = service_account.Credentials.from_service_account_file('service_client_secret.json', scopes=SCOPES)
client = gspread.authorize(credentials)
data_sheet = client.open('test_data').sheet1
usd_to_rub_exchange = get_usd_to_rub_exchange('currency_exchange.xml')
update_db(data_sheet)

cursor.execute("SELECT * FROM orders")
data = cursor.fetchall()

conn.close()
