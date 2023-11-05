import pyodide.http
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta
import pandas


async def scrape_currency_conversion(curr_from, curr_to, amount):
    # curr_from: three letter string representing the currency to convert from
    # curr_to: three letter string representing the currency to convert to
    # date: string in YYYY-MM-DD format
    # amount: string representing the starting amount of currency

    # make the url to scrape from the input
    scrape_url = f"https://currencyconvert.online/{curr_from}/{curr_to}/table"

    # keep on requesting until the response code is 200 (i.e. a valid response)
    response = 0

    while response != 200:
        # request the info from the page
        page = await pyodide.http.pyfetch(scrape_url)
        response = page.status

    # parse the page with beautifulsoup
    soup = BS(await page.string(), "html.parser")

    # find the resulting conversion value
    value = soup.find("table", {"id": "table1-history"})

    # read the data into a data table
    table = pandas.read_html(io=str(value))[0]

    table["Price"] = table["Price"].str.extract(
        r'(\d+\.*\d+)').astype(float).apply(lambda x: x*amount)
    table["Date"] = table["Date"].str.extract(r'(\d+/\d+/\d+)')
    table['Date'] = pandas.to_datetime(table['Date'], dayfirst=True)

    return table
