import requests
from xml.etree import ElementTree


def get_usd_to_rub_exchange_rate():
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    if not response:
        return
    tree = ElementTree.ElementTree(ElementTree.fromstring(response.content))
    root = tree.getroot()
    item = root.find("./Valute/[@ID='R01235']/Value")
    return float(item.text.replace(',', '.'))
