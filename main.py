import requests
import selectorlib
from mailing import send_email
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

connection = sqlite3.connect("data.db")


def scrape(url):
    response = requests.get(URL, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted_data):
    new_row = [item.strip() for item in extracted_data.split(",")]
    print(f"New row -> {new_row}")
    # band, city, date = new_row
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", new_row)
    connection.commit()


def read(extracted_data):
    cursor = connection.cursor()
    row = [item.strip() for item in extracted_data.split(",")]
    print(row)
    band, city, date = row
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(f"print {rows}")
    return rows


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    if extracted != "No upcoming tours":
        row = read(extracted)
        if not row:
            store(extracted)
            send_email(extracted)
            print("Email was sent")
