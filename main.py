import requests
import selectorlib
from mailing import Email
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


class Event:
    def scrape(self, url):
        response = requests.get(URL, headers=HEADERS)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Database:
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def store(self, extracted_data):
        new_row = [item.strip() for item in extracted_data.split(",")]
        print(f"New row -> {new_row}")
        # band, city, date = new_row
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", new_row)
        self.connection.commit()

    def read(self, extracted_data):
        cursor = self.connection.cursor()
        row = [item.strip() for item in extracted_data.split(",")]
        print(row)
        band, city, date = row
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = cursor.fetchall()
        print(f"print {rows}")
        return rows


if __name__ == "__main__":
    event = Event()
    scraped = event.scrape(URL)
    extracted = event.extract(scraped)
    print(extracted)
    if extracted != "No upcoming tours":
        database = Database(database_path="data.db")
        row = database.read(extracted)
        if not row:
            database.store(extracted)
            email = Email()
            email.send(extracted)
            print("Email was sent")
