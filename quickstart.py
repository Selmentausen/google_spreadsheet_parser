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

credentials = service_account.Credentials.from_service_account_file('service_client_secret.json', scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open('test_data').sheet1


def update_currency_file():
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    with open('currency_exchange.xml', 'wb') as f:
        f.write(response.content)


def get_usd_to_rub_exchange(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    item = root.find("./Valute/[@ID='R01235']/Value")
    return float(item.text.replace(',', '.'))


def update_db():
    usd_to_rub_exchange = get_usd_to_rub_exchange('currency_exchange.xml')
    for (p_id, order_id, usd_cost, delivery_date) in sheet.get("A2:D"):
        rub_cost = float(usd_cost) * usd_to_rub_exchange
        cursor.execute(
            f"""INSERT INTO orders
            VALUES ({p_id}, {order_id}, {usd_cost}, {rub_cost},
            TO_DATE('{delivery_date}', 'DD.MM.YYYY'))""")
    conn.commit()


cursor.execute("SELECT * FROM orders")
data = cursor.fetchall()

conn.close()
