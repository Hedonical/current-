import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta
import pandas


def scrape_currency_conversion(curr_from, curr_to, date, amount):
    # curr_from: three letter string representing the currency to convert from
    # curr_to: three letter string representing the currency to convert to
    # date: string in YYYY-MM-DD format
    # amount: string representing the starting amount of currency

    # make the url to scrape from the input
    scrape_url = f"https://fx-rate.net/calculator/?c_input={curr_from}&cp_input={curr_to}&amount_from={amount}&amount_to=1000.00&date_input={date}&interbank_input=0"

    # keep on requesting until the response code is 200 (i.e. a valid response)
    response = 0

    while response != 200:
        # request the info from the page
        page = requests.get(scrape_url)
        response = page.status_code

    # parse the page with beautifulsoup
    soup = BS(page.text, "html.parser")

    # find the resulting conversion value
    value = float(soup.find('input', {'name': 'amount_to'}).get('value'))

    return value


def scrape_currency_table(curr_from, curr_to, date, amount, span="week"):
    data = {"year": [], "month": [], "day": [], "amount": []}

    # convert the date to a datetime object
    date = datetime.strptime(date, '%Y-%m-%d')

    # create a dictionary to later convert to a pandas
    if span == "week":
        for i in range(7):
            adjusted_date = date - timedelta(days=i)
            # save the date to the data
            data["year"].append(adjusted_date.year)
            data["month"].append(adjusted_date.month)
            data["day"].append(adjusted_date.day)
            data["amount"].append(scrape_currency_conversion(curr_from,
                                                             curr_to,
                                                             adjusted_date.strftime(
                                                                 "%Y-%m-%d"),
                                                             amount))

    elif span == "month":
        for i in range(30):
            adjusted_date = date - timedelta(days=i)
            # save the date to the data
            data["year"].append(adjusted_date.year)
            data["month"].append(adjusted_date.month)
            data["day"].append(adjusted_date.day)
            data["amount"].append(scrape_currency_conversion(curr_from,
                                                             curr_to,
                                                             adjusted_date.strftime(
                                                                 "%Y-%m-%d"),
                                                             amount))

    # turn the dictionary into a dataframe
    table = pandas.DataFrame.from_dict(data)
    return table
