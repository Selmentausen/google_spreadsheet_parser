# noinspection PyPackageRequirements
from google.oauth2 import service_account
import gspread

SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file",
          "https://www.googleapis.com/auth/spreadsheets"]

credentials = service_account.Credentials.from_service_account_file('service_client_secret.json', scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open('test_data').sheet1
print(sheet.get("A2:D"))
