from datetime import datetime as dt
import datetime
from exchange_rate import scrape_currency_conversion, scrape_currency_table
import itertools

currencies = ["USD", "VND", "EUR"]
pairings = itertools.permutations(currencies, 2)
date = (dt.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
print(date)
amount = 1
span = "month"
#format list(dict{from,to,conversion rate,mean,sd})
conversion_rates = []

for pair in pairings:
    curr_from = pair[0]
    curr_to = pair[1]
    df = scrape_currency_table(curr_from, curr_to, date, amount, span)
    conversion_rates.append(
        {
            'from':curr_from,
            'to':curr_to,
            'conversion rate': scrape_currency_conversion(),
            'mean': df['amount'].sum()/df['amount'].count(),
            'sd':df['amount'].std()
        }
    )

print(conversion_rates)