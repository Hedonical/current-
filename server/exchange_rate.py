import pyodide.http
from bs4 import BeautifulSoup as BS
import pandas
import re


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
    value = str(soup.find("table", {"id": "table1-history"}))

    # create a dictionary to store the dataframe
    table = {"Date": [], "Price": []}

    table["Date"] = re.findall(r'(?<!<span class="d-lg-none")\d{2}/\d{2}/\d{4}(?=</span>)',
                               value)

    table["Price"] = re.findall(r'(?<!<td class="exchange-rate text-truncate text-right")\d+\.\d+(?=\s*[A-Z]{3})',
                                value)

    table["Price"] = [float(ele) for ele in table["Price"]]

    if len(table["Date"]) > len(table["Price"]):
        table["Date"] = table["Date"][0:len(table["Price"])]
    elif len(table["Date"]) < len(table["Price"]):
        table["Price"] = table["Price"][0:len(table["Date"])]

    table = pandas.DataFrame.from_dict(table)

    table["Price"] = table["Price"].apply(lambda x: x*amount)
    table['Date'] = pandas.to_datetime(table['Date'], dayfirst=True)

    return table
